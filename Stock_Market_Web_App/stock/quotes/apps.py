from django.apps import AppConfig
from django.db.models import BigAutoField

class QuotesConfig(AppConfig):
    default_auto_field = BigAutoField
    name = 'quotes'