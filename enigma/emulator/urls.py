from django.urls import path

from .views import EnigmaConfigView, EnigmaFileConfigView, EnigmaEmulatorView


app_name = 'emulator'

urlpatterns = [
    path('config/', EnigmaConfigView.as_view(), name='config'),
    path('file_config/', EnigmaFileConfigView.as_view(), name='file_config'),
    path('<config>/', EnigmaEmulatorView.as_view(), name='emulator'),
]
