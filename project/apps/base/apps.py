from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

app_name = 'base'

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    verbose_name = _('Основное')
    verbose_name_plural = _('Основные')
