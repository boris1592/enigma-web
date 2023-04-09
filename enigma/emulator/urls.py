from django.urls import path
from .views import EnigmaConfigView

app_name = 'emulator'

urlpatterns = [
    path('config/', EnigmaConfigView.as_view(), name='config'),
]
