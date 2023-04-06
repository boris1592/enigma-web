from django.views.generic import TemplateView
from django.urls import path

app_name = 'home'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='index.html'),
        name='home'
    )
]
