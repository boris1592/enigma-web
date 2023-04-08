from django.views.generic import FormView
from .forms import EnigmaConfigForm


class EnigmaConfigView(FormView):
    template_name = 'form.html'
    form_class = EnigmaConfigForm
