from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChannelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = _("ArtD Channel")
    name = 'channels'

    def ready(self):
        from channels import signals  # noqa: F401
