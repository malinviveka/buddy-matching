from django.db import models
from django.utils.translation import gettext_lazy as _


class HomepageText(models.Model):
    content_de = models.TextField(
        _("Content in German"), default="Willkommen auf der Seite!"
    )
    content_en = models.TextField(
        _("Content in English"), default="Welcome to the page!"
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Homepage Text (aktualisiert am {self.last_updated})"
