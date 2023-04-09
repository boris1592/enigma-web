from django.urls import path
from .views import EnigmaConfigView, EnigmaEmulatorView
from .converters import ConfigConverter
from django.urls.converters import register_converter

register_converter(ConfigConverter, 'config')


app_name = 'emulator'

urlpatterns = [
    path('config/', EnigmaConfigView.as_view(), name='config'),
    path('<config:config>/', EnigmaEmulatorView.as_view(), name='emulator'),
]
