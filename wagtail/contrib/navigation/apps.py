from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailNavigationAppConfig(AppConfig):
    name = 'wagtail.contrib.navigation'
    label = 'wagtailnavigation'
    verbose_name = _("Wagtail Navigation")
