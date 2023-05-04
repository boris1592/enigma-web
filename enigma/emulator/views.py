from django.views.generic import FormView
from django.urls.base import reverse
from django.shortcuts import redirect, render

from .forms import EnigmaConfigForm, EnigmaEmulatorForm
from .config import EnigmaConfig
from .emulator import EnigmaEmulator


class EnigmaConfigView(FormView):
    template_name = 'config.html'
    form_class = EnigmaConfigForm

    def form_valid(self, form):
        return redirect(
            reverse(
                'emulator:emulator',
                kwargs={'config': form.config.encode()},
            )
        )


class EnigmaEmulatorView(FormView):
    template_name = 'emulator.html'
    form_class = EnigmaEmulatorForm

    def get(self, request, config):
        return render(
            request,
            self.template_name,
            {
                'form': self.get_form(),
                'config': EnigmaConfig.decode(config),
            },
        )

    def form_valid(self, form):
        message = form.cleaned_data.get('message')

        if form.cleaned_data.get('file') is not None:
            message = (
                form.cleaned_data.get('file').read().decode('utf-8').strip()
            )

        try:
            config = EnigmaConfig.decode(self.kwargs['config'])
            config.validate()
            assert all(
                [letter in config.alphabet for letter in message]
            ), 'All letters from message should be in alphabet'
        except AssertionError as error:
            form.add_error(None, f'{str(error)}')
            return render(self.request, self.template_name, {'form': form})

        emulator = EnigmaEmulator(config)
        processed = emulator.process(message)
        return render(
            self.request,
            self.template_name,
            {
                'processed': processed,
                'form': form,
                'config': emulator.get_current_config(),
            },
        )
