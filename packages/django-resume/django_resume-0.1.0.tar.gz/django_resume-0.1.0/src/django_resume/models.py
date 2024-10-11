from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    plugin_data = models.JSONField(default=dict, blank=True, null=False)

    def __repr__(self):
        return f"<{self.name}>"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.plugin_data is None:
            self.plugin_data = {}
        super().save(*args, **kwargs)
