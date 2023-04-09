from django.urls import path

from .views import EnigmaConfigView, EnigmaEmulatorView


app_name = 'emulator'

urlpatterns = [
    path('config/', EnigmaConfigView.as_view(), name='config'),
    path('<config>/', EnigmaEmulatorView.as_view(), name='emulator'),
]
