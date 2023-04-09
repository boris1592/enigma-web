from django.views.generic import FormView
from .forms import EnigmaConfigForm


class EnigmaConfigView(FormView):
    template_name = 'form.html'
    form_class = EnigmaConfigForm

    def form_valid(self, form):
        print(str(form.config))
        return super().form_valid(form)


class EnigmaEmulatorView(FormView):
    pass
