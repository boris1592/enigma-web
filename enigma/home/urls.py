from django.views.generic import TemplateView
from django.urls import path
from .views import EnigmaConfigView

app_name = 'home'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('config/', EnigmaConfigView.as_view(), name='config'),
]
