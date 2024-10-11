from uuid import uuid4

from typing import Protocol, runtime_checkable, Callable, TypeAlias, Any

from django import forms
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, path, URLPattern
from django.utils.html import format_html

from ..models import Person


URLPatterns: TypeAlias = list[URLPattern]
FormClasses: TypeAlias = dict[str, type[forms.Form]]
ContextDict: TypeAlias = dict[str, Any]


@runtime_checkable
class Plugin(Protocol):
    name: str
    verbose_name: str
    form_classes: FormClasses

    def get_admin_urls(self, admin_view: Callable) -> URLPatterns:
        """Return a list of urls that are used to manage the plugin data in the Django admin interface."""
        ...  # pragma: no cover

    def get_admin_link(self, person_id: int) -> str:
        """Return a formatted html link to the main admin view for this plugin."""
        ...  # pragma: no cover

    def get_inline_urls(self) -> URLPatterns:
        """Return a list of urls that are used to manage the plugin data inline."""
        ...  # pragma: no cover

    def get_form_classes(self) -> FormClasses:
        """
        Return a dictionary of form classes that are used to manage the plugin data.
        Overwrite this method or set the form_classes attribute.
        """
        ...  # pragma: no cover

    def get_data(self, person: Person) -> dict:
        """Return the plugin data for a person."""
        ...  # pragma: no cover

    def get_context(
        self,
        request: HttpRequest,
        plugin_data: dict,
        person_pk: int,
        *,
        context: dict,
        edit: bool = False,
    ) -> object:
        """Return the object which is stored in context for the plugin."""
        ...  # pragma: no cover


class SimpleData:
    def __init__(self, *, plugin_name: str):
        self.plugin_name = plugin_name

    def get_data(self, person: Person) -> dict:
        return person.plugin_data.get(self.plugin_name, {})

    def set_data(self, person: Person, data: dict) -> Person:
        if not person.plugin_data:
            person.plugin_data = {}
        person.plugin_data[self.plugin_name] = data
        return person

    def create(self, person: Person, data: dict) -> Person:
        return self.set_data(person, data)

    def update(self, person: Person, data: dict) -> Person:
        return self.set_data(person, data)


class SimpleJsonForm(forms.Form):
    plugin_data = forms.JSONField(widget=forms.Textarea)


class SimpleAdmin:
    admin_template = "django_resume/admin/simple_plugin_admin_view.html"
    change_form = "django_resume/admin/simple_plugin_admin_form.html"

    def __init__(
        self,
        *,
        plugin_name: str,
        plugin_verbose_name,
        form_class: type[forms.Form],
        data: SimpleData,
    ):
        self.plugin_name = plugin_name
        self.plugin_verbose_name = plugin_verbose_name
        self.form_class = form_class
        self.data = data

    def get_change_url(self, person_id):
        return reverse(
            f"admin:{self.plugin_name}-admin-change", kwargs={"person_id": person_id}
        )

    def get_admin_link(self, person_id):
        url = self.get_change_url(person_id)
        return format_html(
            '<a href="{}">{}</a>', url, f"Edit {self.plugin_verbose_name}"
        )

    def get_change_post_url(self, person_id):
        return reverse(
            f"admin:{self.plugin_name}-admin-post", kwargs={"person_id": person_id}
        )

    def get_change_view(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        plugin_data = self.data.get_data(person)
        if self.form_class == SimpleJsonForm:
            # special case for the SimpleJsonForm which has a JSONField for the plugin data
            form = self.form_class(initial={"plugin_data": plugin_data})
        else:
            form = self.form_class(initial=plugin_data)
        form.post_url = self.get_change_post_url(person.pk)
        context = {
            "title": f"{self.plugin_verbose_name} for {person.name}",
            "person": person,
            "opts": Person._meta,
            "form": form,
            "form_template": self.change_form,
            # context for admin/change_form.html template
            "add": False,
            "change": True,
            "is_popup": False,
            "save_as": False,
            "has_add_permission": False,
            "has_view_permission": True,
            "has_change_permission": True,
            "has_delete_permission": False,
            "has_editable_inline_admin_formsets": False,
        }
        return render(request, self.admin_template, context)

    def post_view(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        form = self.form_class(request.POST)
        form.post_url = self.get_change_post_url(person.pk)
        context = {"form": form}
        if form.is_valid():
            if self.form_class == SimpleJsonForm:
                # special case for the SimpleJsonForm which has a JSONField for the plugin data
                plugin_data = form.cleaned_data["plugin_data"]
            else:
                plugin_data = form.cleaned_data
            person = self.data.update(person, plugin_data)
            person.save()
        response = render(request, self.change_form, context)
        return response

    def get_urls(self, admin_view: Callable) -> URLPatterns:
        """
        This method should return a list of urls that are used to manage the
        plugin data in the admin interface.
        """
        plugin_name = self.plugin_name
        urls = [
            path(
                f"<int:person_id>/plugin/{plugin_name}/change/",
                admin_view(self.get_change_view),
                name=f"{plugin_name}-admin-change",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/post/",
                admin_view(self.post_view),
                name=f"{plugin_name}-admin-post",
            ),
        ]
        return urls


class SimpleTemplates:
    def __init__(self, *, main: str, form: str):
        self.main = main
        self.form = form


class SimpleInline:
    def __init__(
        self,
        *,
        plugin_name: str,
        plugin_verbose_name: str,
        form_class: type[forms.Form],
        data: SimpleData,
        templates: SimpleTemplates,
        get_context: Callable,
    ):
        self.plugin_name = plugin_name
        self.plugin_verbose_name = plugin_verbose_name
        self.form_class = form_class
        self.data = data
        self.templates = templates
        self.get_context = get_context

    def get_edit_url(self, person_id):
        return reverse(
            f"django_resume:{self.plugin_name}-edit", kwargs={"person_id": person_id}
        )

    def get_post_url(self, person_id):
        return reverse(
            f"django_resume:{self.plugin_name}-post", kwargs={"person_id": person_id}
        )

    def get_edit_view(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        plugin_data = self.data.get_data(person)
        print("get edit view!")
        form = self.form_class(initial=plugin_data)
        form.post_url = self.get_post_url(person.pk)
        context = {"form": form}
        return render(request, self.templates.form, context)

    def post_view(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        plugin_data = self.data.get_data(person)
        form_class = self.form_class
        print("post view: ", request.POST, request.FILES)
        form = form_class(request.POST, request.FILES, initial=plugin_data)
        form.post_url = self.get_post_url(person.pk)
        context = {"form": form}
        if form.is_valid():
            # update the plugin data and render the main template
            person = self.data.update(person, form.cleaned_data)
            person.save()
            context[self.plugin_name] = self.get_context(
                request, form.cleaned_data, person.pk, context=context
            )
            context["show_edit_button"] = True
            context[self.plugin_name].update(form.cleaned_data)
            context[self.plugin_name]["edit_url"] = self.get_edit_url(person.pk)
            return render(request, self.templates.main, context)
        # render the form again with errors
        return render(request, self.templates.form, context)

    def get_urls(self) -> URLPatterns:
        plugin_name = self.plugin_name
        urls: URLPatterns = [
            # flat
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/",
                self.get_edit_view,
                name=f"{plugin_name}-edit",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/post/",
                self.post_view,
                name=f"{plugin_name}-post",
            ),
        ]
        return urls


class SimplePlugin:
    """
    A simple plugin that only stores a json serializable dict of data. It's simple,
    because there is only one form for the plugin data and no items with IDs or other
    complex logic.
    """

    name = "simple_plugin"
    verbose_name = "Simple Plugin"
    templates: SimpleTemplates = SimpleTemplates(
        # those two templates are just a dummies - overwrite them
        main="django_resume/plain/simple_plugin.html",
        form="django_resume/plain/simple_plugin_form.html",
    )

    def __init__(self):
        super().__init__()
        self.data = data = SimpleData(plugin_name=self.name)
        self.admin = SimpleAdmin(
            plugin_name=self.name,
            plugin_verbose_name=self.verbose_name,
            form_class=self.get_admin_form_class(),
            data=data,
        )
        self.inline = SimpleInline(
            plugin_name=self.name,
            plugin_verbose_name=self.verbose_name,
            form_class=self.get_inline_form_class(),
            data=data,
            templates=self.templates,
            get_context=self.get_context,
        )

    def get_context(
        self,
        _request: HttpRequest,
        plugin_data: dict,
        person_pk: int,
        *,
        context: ContextDict,
        edit: bool = False,
    ) -> ContextDict:
        """This method returns the context of the plugin for inline editing."""
        if plugin_data == {}:
            # no data yet, use initial data from inline form
            form = self.get_inline_form_class()()
            initial_values = {
                field_name: form.get_initial_for_field(field, field_name)
                for field_name, field in form.fields.items()
            }
            plugin_data = initial_values
        context.update(plugin_data)
        context["edit_url"] = self.inline.get_edit_url(person_pk)
        context["show_edit_button"] = edit
        context["templates"] = self.templates
        return context

    # plugin protocol methods

    def get_admin_form_class(self) -> type[forms.Form]:
        """Set admin_form_class attribute or overwrite this method."""
        if hasattr(self, "admin_form_class"):
            return self.admin_form_class
        return SimpleJsonForm  # default

    def get_inline_form_class(self) -> type[forms.Form]:
        """Set inline_form_class attribute or overwrite this method."""
        if hasattr(self, "inline_form_class"):
            return self.inline_form_class
        return SimpleJsonForm  # default

    def get_admin_urls(self, admin_view: Callable) -> URLPatterns:
        return self.admin.get_urls(admin_view)

    def get_admin_link(self, person_id: int | None) -> str:
        if person_id is None:
            return ""
        return self.admin.get_admin_link(person_id)

    def get_inline_urls(self) -> URLPatterns:
        return self.inline.get_urls()

    def get_data(self, person: Person) -> dict:
        return self.data.get_data(person)


class ListItemFormMixin(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop("person")
        self.existing_items = kwargs.pop("existing_items", [])
        super().__init__(*args, **kwargs)

    @property
    def is_new(self):
        """Used to determine if the form is for a new item or an existing one."""
        if self.is_bound:
            return False
        return not self.initial.get("id", False)

    @property
    def item_id(self):
        """
        Use an uuid for the item id if there is no id in the initial data. This is to
        allow the htmx delete button to work even when there are multiple new item
        forms on the page.
        """
        if self.is_bound:
            return self.cleaned_data.get("id", uuid4())
        if self.initial.get("id") is None:
            self.initial["id"] = uuid4()
        return self.initial["id"]


class ListTemplates:
    def __init__(
        self, *, main: str, flat: str, flat_form: str, item: str, item_form: str
    ):
        self.main = main
        self.flat = flat
        self.flat_form = flat_form
        self.item = item
        self.item_form = item_form


class ListData:
    """
    This class contains the logic of the list plugin concerned with the data handling.

    Simple crud operations are supported.
    """

    def __init__(self, *, plugin_name: str):
        self.plugin_name = plugin_name

    # read
    def get_data(self, person: Person):
        return person.plugin_data.get(self.plugin_name, {})

    def get_item_by_id(self, person: Person, item_id: str) -> dict | None:
        items = self.get_data(person).get("items", [])
        for item in items:
            if item["id"] == item_id:
                return item
        return None

    # write
    def set_data(self, person: Person, data: dict):
        if not person.plugin_data:
            person.plugin_data = {}
        person.plugin_data[self.plugin_name] = data
        return person

    def create(self, person: Person, data: dict):
        """Create an item in the items list of this plugin."""
        plugin_data = self.get_data(person)
        plugin_data.setdefault("items", []).append(data)
        person = self.set_data(person, plugin_data)
        return person

    def update(self, person: Person, data: dict):
        """Update an item in the items list of this plugin."""
        plugin_data = self.get_data(person)
        items = plugin_data.get("items", [])
        print(items, data)
        for item in items:
            if item["id"] == data["id"]:
                item.update(data)
                break
        plugin_data["items"] = items
        return self.set_data(person, plugin_data)

    def update_flat(self, person: Person, data: dict):
        """Update the flat data of this plugin."""
        plugin_data = self.get_data(person)
        plugin_data["flat"] = data
        return self.set_data(person, plugin_data)

    def delete(self, person: Person, data: dict):
        """Delete an item from the items list of this plugin."""
        plugin_data = self.get_data(person)
        items = plugin_data.get("items", [])
        for i, item in enumerate(items):
            if item["id"] == data["id"]:
                items.pop(i)
                break
        plugin_data["items"] = items
        return self.set_data(person, plugin_data)


class ListAdmin:
    """
    This class contains the logic of the list plugin concerned with the Django admin interface.

    Simple crud operations are supported. Each item in the list is a json serializable
    dict and should have an "id" field.

    Why have an own class for this? Because the admin interface is different from the
    inline editing on the website itself. For example: the admin interface has a change
    view where all forms are displayed at once. Which makes sense, because the admin is
    for editing.
    """

    admin_change_form_template = (
        "django_resume/admin/list_plugin_admin_change_form_htmx.html"
    )
    admin_item_change_form_template = (
        "django_resume/admin/list_plugin_admin_item_form.html"
    )
    admin_flat_form_template = "django_resume/admin/list_plugin_admin_flat_form.html"

    def __init__(
        self,
        *,
        plugin_name: str,
        plugin_verbose_name,
        form_classes: dict,
        data: ListData,
    ):
        self.plugin_name = plugin_name
        self.plugin_verbose_name = plugin_verbose_name
        self.form_classes = form_classes
        self.data = data

    def get_change_url(self, person_id):
        """
        Main admin view for this plugin. This view should display a list of item
        forms with update buttons for existing items and a button to get a form to
        add a new item. And a form to change the data for the plugin that is stored
        in a flat format.
        """
        return reverse(
            f"admin:{self.plugin_name}-admin-change", kwargs={"person_id": person_id}
        )

    def get_admin_link(self, person_id: int) -> str:
        """
        Return a link to the main admin view for this plugin. This is used to have the
        plugins show up as readonly fields in the person change view and to have a link
        to be able to edit the plugin data.
        """
        url = self.get_change_url(person_id)
        return format_html(
            '<a href="{}">{}</a>', url, f"Edit {self.plugin_verbose_name}"
        )

    def get_change_flat_post_url(self, person_id):
        """Used for create and update flat data."""
        return reverse(
            f"admin:{self.plugin_name}-admin-flat-post", kwargs={"person_id": person_id}
        )

    def get_change_item_post_url(self, person_id):
        """Used for create and update item."""
        return reverse(
            f"admin:{self.plugin_name}-admin-item-post", kwargs={"person_id": person_id}
        )

    def get_delete_item_url(self, person_id, item_id):
        """Used for delete item."""
        return reverse(
            f"admin:{self.plugin_name}-admin-item-delete",
            kwargs={"person_id": person_id, "item_id": item_id},
        )

    def get_item_add_form_url(self, person_id):
        """
        Returns the url of a view that returns a form to add a new item. The person_id
        is needed to be able to add the right post url to the form.
        """
        return reverse(
            f"admin:{self.plugin_name}-admin-item-add", kwargs={"person_id": person_id}
        )

    # crud views

    def get_add_item_form_view(self, request, person_id):
        """Return a single empty form to add a new item."""
        person = get_object_or_404(Person, pk=person_id)
        form_class = self.form_classes["item"]
        existing_items = self.data.get_data(person).get("items", [])
        form = form_class(initial={}, person=person, existing_items=existing_items)
        form.post_url = self.get_change_item_post_url(person.pk)
        context = {"form": form}
        return render(request, self.admin_item_change_form_template, context)

    def get_change_view(self, request, person_id):
        """Return the main admin view for this plugin."""
        person = get_object_or_404(Person, pk=person_id)
        context = {
            "title": f"{self.plugin_verbose_name} for {person.name}",
            "person": person,
            "opts": Person._meta,
            # context for admin/change_form.html template
            "add": False,
            "change": True,
            "is_popup": False,
            "save_as": False,
            "has_add_permission": False,
            "has_view_permission": True,
            "has_change_permission": True,
            "has_delete_permission": False,
            "has_editable_inline_admin_formsets": False,
        }
        plugin_data = self.data.get_data(person)
        form_classes = self.form_classes
        # flat form
        flat_form_class = form_classes["flat"]
        flat_form = flat_form_class(initial=plugin_data.get("flat", {}))
        flat_form.post_url = self.get_change_flat_post_url(person.pk)
        context["flat_form"] = flat_form
        # item forms
        item_form_class = form_classes["item"]
        initial_items_data = plugin_data.get("items", [])
        post_url = self.get_change_item_post_url(person.id)
        item_forms = []
        for initial_item_data in initial_items_data:
            form = item_form_class(
                initial=initial_item_data,
                person=person,
                existing_items=initial_items_data,
            )
            form.post_url = post_url
            form.delete_url = self.get_delete_item_url(
                person.id, initial_item_data["id"]
            )
            item_forms.append(form)
        context["add_item_form_url"] = self.get_item_add_form_url(person.id)
        context["item_forms"] = item_forms
        return render(request, self.admin_change_form_template, context)

    def post_item_view(self, request, person_id):
        """Handle post requests to create or update a single item."""
        person = get_object_or_404(Person, id=person_id)
        form_class = self.form_classes["item"]
        existing_items = self.data.get_data(person).get("items", [])
        form = form_class(request.POST, person=person, existing_items=existing_items)
        form.post_url = self.get_change_item_post_url(person.pk)
        context = {"form": form}
        if form.is_valid():
            # try to find out whether we are updating an existing item or creating a new one
            existing = True
            item_id = form.cleaned_data.get("id", None)
            if item_id is not None:
                item = self.data.get_item_by_id(person, item_id)
                if item is None:
                    existing = False
            else:
                # no item_id -> new item
                existing = False
            if existing:
                # update existing item
                item_id = form.cleaned_data["id"]
                person = self.data.update(person, form.cleaned_data)
            else:
                # create new item
                data = form.cleaned_data
                item_id = str(uuid4())
                data["id"] = item_id
                person = self.data.create(person, data)
                # weird hack to make the form look like it is for an existing item
                # if there's a better way to do this, please let me know FIXME
                form.data = form.data.copy()
                form.data["id"] = item_id
            person.save()
            form.delete_url = self.get_delete_item_url(person.id, item_id)
        return render(request, self.admin_item_change_form_template, context)

    def post_flat_view(self, request, person_id):
        """Handle post requests to update flat data."""
        person = get_object_or_404(Person, id=person_id)
        form_class = self.form_classes["flat"]
        form = form_class(request.POST)
        form.post_url = self.get_change_flat_post_url(person.pk)
        context = {"form": form}
        if form.is_valid():
            person = self.data.update_flat(person, form.cleaned_data)
            person.save()
        return render(request, self.admin_flat_form_template, context)

    def delete_item_view(self, _request, person_id, item_id):
        """Delete an item from the items list of this plugin."""
        person = get_object_or_404(Person, pk=person_id)
        person = self.data.delete(person, {"id": item_id})
        person.save()
        return HttpResponse(status=200)

    # urlpatterns

    def get_urls(self, admin_view: Callable) -> URLPatterns:
        """
        This method should return a list of urls that are used to manage the
        plugin data in the admin interface.
        """
        plugin_name = self.plugin_name
        urls = [
            path(
                f"<int:person_id>/plugin/{plugin_name}/change/",
                admin_view(self.get_change_view),
                name=f"{plugin_name}-admin-change",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/item/post/",
                admin_view(self.post_item_view),
                name=f"{plugin_name}-admin-item-post",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/add/",
                admin_view(self.get_add_item_form_view),
                name=f"{plugin_name}-admin-item-add",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/delete/<str:item_id>/",
                admin_view(self.delete_item_view),
                name=f"{plugin_name}-admin-item-delete",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/flat/post/",
                admin_view(self.post_flat_view),
                name=f"{plugin_name}-admin-flat-post",
            ),
        ]
        return urls


class ListInline:
    """
    This class contains the logic of the list plugin concerned with the inline editing
    of the plugin data on the website itself.
    """

    def __init__(
        self,
        *,
        plugin_name: str,
        plugin_verbose_name: str,
        form_classes: dict,
        data: ListData,
        templates: ListTemplates,
    ):
        self.plugin_name = plugin_name
        self.plugin_verbose_name = plugin_verbose_name
        self.form_classes = form_classes
        self.data = data
        self.templates = templates

    # urls

    def get_edit_flat_post_url(self, person_id):
        return reverse(
            f"django_resume:{self.plugin_name}-edit-flat-post",
            kwargs={"person_id": person_id},
        )

    def get_edit_flat_url(self, person_id):
        return reverse(
            f"django_resume:{self.plugin_name}-edit-flat",
            kwargs={"person_id": person_id},
        )

    def get_edit_item_url(self, person_id, item_id=None):
        if item_id is None:
            return reverse(
                f"django_resume:{self.plugin_name}-add-item",
                kwargs={"person_id": person_id},
            )
        else:
            return reverse(
                f"django_resume:{self.plugin_name}-edit-item",
                kwargs={"person_id": person_id, "item_id": item_id},
            )

    def get_post_item_url(self, person_id):
        return reverse(
            f"django_resume:{self.plugin_name}-item-post",
            kwargs={"person_id": person_id},
        )

    def get_delete_item_url(self, person_id, item_id):
        return reverse(
            f"django_resume:{self.plugin_name}-delete-item",
            kwargs={"person_id": person_id, "item_id": item_id},
        )

    # crud views

    def get_edit_flat_view(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        plugin_data = self.data.get_data(person)
        flat_form_class = self.form_classes["flat"]
        flat_form = flat_form_class(initial=plugin_data.get("flat", {}))
        flat_form.post_url = self.get_edit_flat_post_url(person.pk)
        context = {
            "form": flat_form,
            "edit_flat_post_url": self.get_edit_flat_post_url(person.pk),
        }
        return render(request, self.templates.flat_form, context=context)

    def post_edit_flat_view(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        flat_form_class = self.form_classes["flat"]
        plugin_data = self.data.get_data(person)
        flat_form = flat_form_class(request.POST, initial=plugin_data.get("flat", {}))
        context = {}
        if flat_form.is_valid():
            person = self.data.update_flat(person, flat_form.cleaned_data)
            person.save()
            person.refresh_from_db()
            plugin_data = self.data.get_data(person)
            context["edit_flat_url"] = self.get_edit_flat_url(person.pk)
            context = flat_form.set_context(plugin_data["flat"], context)
            context["show_edit_button"] = True
            return render(request, self.templates.flat, context=context)
        else:
            context["form"] = flat_form
            context["edit_flat_post_url"] = self.get_edit_flat_post_url(person.pk)
            response = render(request, self.templates.flat_form, context=context)
            return response

    def get_item_view(self, request, person_id, item_id=None):
        person = get_object_or_404(Person, id=person_id)
        plugin_data = self.data.get_data(person)
        existing_items = plugin_data.get("items", [])
        form_class = self.form_classes["item"]
        # get the item data if we are editing an existing item
        initial = form_class.get_initial()
        if item_id is not None:
            for item in existing_items:
                if item["id"] == item_id:
                    initial = item
        form = form_class(initial=initial, person=person, existing_items=existing_items)
        form.post_url = self.get_post_item_url(person.pk)
        context = {"form": form, "plugin_name": self.plugin_name}
        return render(request, self.templates.item_form, context=context)

    def post_item_view(self, request, person_id):
        print("in post item view!")
        person = get_object_or_404(Person, id=person_id)
        form_class = self.form_classes["item"]
        existing_items = self.data.get_data(person).get("items", [])
        form = form_class(request.POST, person=person, existing_items=existing_items)
        form.post_url = self.get_post_item_url(person.pk)
        context = {"form": form}
        if form.is_valid():
            # try to find out whether we are updating an existing item or creating a new one
            existing = True
            item_id = form.cleaned_data.get("id", None)
            if item_id is not None:
                item = self.data.get_item_by_id(person, item_id)
                if item is None:
                    existing = False
            else:
                # no item_id -> new item
                existing = False
            if existing:
                # update existing item
                item_id = form.cleaned_data["id"]
                person = self.data.update(person, form.cleaned_data)
            else:
                # create new item
                data = form.cleaned_data
                item_id = str(uuid4())
                data["id"] = item_id
                person = self.data.create(person, data)
                # weird hack to make the form look like it is for an existing item
                # if there's a better way to do this, please let me know FIXME
                form.data = form.data.copy()
                form.data["id"] = item_id
            person.save()
            item = self.data.get_item_by_id(person, item_id)
            # populate entry because it's used in the standard item template,
            # and we are no longer rendering a form when the form was valid
            context["edit_url"] = self.get_edit_item_url(person.id, item_id)
            context["delete_url"] = self.get_delete_item_url(person.id, item_id)
            form.set_context(item, context)
            context["show_edit_button"] = True
            context["plugin_name"] = self.plugin_name  # for javascript
            return render(request, self.templates.item, context)
        else:
            # form is invalid
            return render(request, self.templates.item_form, context)

    def delete_item_view(self, _request, person_id, item_id):
        """Delete an item from the items list of this plugin."""
        person = get_object_or_404(Person, pk=person_id)
        person = self.data.delete(person, {"id": item_id})
        person.save()
        return HttpResponse(status=200)

    # urlpatterns
    def get_urls(self):
        plugin_name = self.plugin_name
        urls = [
            # flat
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/flat/",
                self.get_edit_flat_view,
                name=f"{plugin_name}-edit-flat",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/flat/post/",
                self.post_edit_flat_view,
                name=f"{plugin_name}-edit-flat-post",
            ),
            # item
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/item/<str:item_id>",
                self.get_item_view,
                name=f"{plugin_name}-edit-item",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/item/",
                self.get_item_view,
                name=f"{plugin_name}-add-item",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/edit/item/post/",
                self.post_item_view,
                name=f"{plugin_name}-item-post",
            ),
            path(
                f"<int:person_id>/plugin/{plugin_name}/delete/<str:item_id>/",
                self.delete_item_view,
                name=f"{plugin_name}-delete-item",
            ),
        ]
        return urls


class ListPlugin:
    """
    A plugin that displays a list of items. Simple crud operations are supported.
    Each item in the list is a json serializable dict and should have an "id" field.

    Additional flat data can be stored in the plugin_data['flat'] field.
    """

    name = "list_plugin"
    verbose_name = "List Plugin"
    templates: ListTemplates = ListTemplates(
        main="", flat="", flat_form="", item="", item_form=""
    )  # overwrite this

    def __init__(self):
        super().__init__()
        self.data = data = ListData(plugin_name=self.name)
        form_classes = self.get_form_classes()
        self.admin = ListAdmin(
            plugin_name=self.name,
            plugin_verbose_name=self.verbose_name,
            form_classes=form_classes,
            data=data,
        )
        self.inline = ListInline(
            plugin_name=self.name,
            plugin_verbose_name=self.verbose_name,
            form_classes=form_classes,
            data=data,
            templates=self.templates,
        )

    # list logic

    def get_flat_form_class(self) -> type[forms.Form]:
        """Set inline_form_class attribute or overwrite this method."""
        if hasattr(self, "flat_form_class"):
            return self.flat_form_class
        return SimpleJsonForm  # default

    @staticmethod
    def items_ordered_by_position(items, reverse=False):
        return sorted(items, key=lambda item: item.get("position", 0), reverse=reverse)

    def get_context(
        self,
        _request: HttpRequest,
        plugin_data: dict,
        person_pk: int,
        *,
        context: ContextDict,
        edit: bool = False,
    ) -> ContextDict:
        if plugin_data.get("flat", {}) == {}:
            # no flat data yet, use initial data from inline form
            form = self.get_flat_form_class()()
            initial_values = {
                field_name: form.get_initial_for_field(field, field_name)
                for field_name, field in form.fields.items()
            }
            plugin_data["flat"] = initial_values
        # add flat data to context
        context.update(plugin_data["flat"])

        ordered_entries = self.items_ordered_by_position(
            plugin_data.get("items", []), reverse=True
        )
        if edit:
            # if there should be edit buttons, add the edit URLs to each entry
            context["show_edit_button"] = True
            for entry in ordered_entries:
                entry["edit_url"] = self.inline.get_edit_item_url(
                    person_pk, item_id=entry["id"]
                )
                entry["delete_url"] = self.inline.get_delete_item_url(
                    person_pk, item_id=entry["id"]
                )
        print("edit flat post: ", self.inline.get_edit_flat_post_url(person_pk))
        context.update(
            {
                "plugin_name": self.name,
                "templates": self.templates,
                "ordered_entries": ordered_entries,
                "add_item_url": self.inline.get_edit_item_url(person_pk),
                "edit_flat_url": self.inline.get_edit_flat_url(person_pk),
                "edit_flat_post_url": self.inline.get_edit_flat_post_url(person_pk),
            }
        )
        return context

    # plugin protocol methods

    def get_admin_urls(self, admin_view: Callable) -> URLPatterns:
        return self.admin.get_urls(admin_view)

    def get_admin_link(self, person_id: int | None) -> str:
        if person_id is None:
            return ""
        return self.admin.get_admin_link(person_id)

    def get_inline_urls(self) -> URLPatterns:
        return self.inline.get_urls()

    def get_form_classes(self) -> dict[str, type[forms.Form]]:
        """Please implement this method."""
        return {}

    def get_data(self, person: Person) -> dict:
        return self.data.get_data(person)
