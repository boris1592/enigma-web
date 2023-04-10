from django.views.generic import FormView
from django.urls.base import reverse
from django.shortcuts import redirect, render

from .forms import EnigmaConfigForm, EnigmaEmulatorForm
from .config import encode_config, decode_config
from .emulator import EnigmaEmulator


class EnigmaConfigView(FormView):
    template_name = 'config.html'
    form_class = EnigmaConfigForm

    def form_valid(self, form):
        return redirect(
            reverse(
                'emulator:emulator',
                kwargs={'config': encode_config(form.config)},
            )
        )


class EnigmaEmulatorView(FormView):
    template_name = 'emulator.html'
    form_class = EnigmaEmulatorForm

    def form_valid(self, form):
        message = form.cleaned_data.get('message')

        try:
            config = decode_config(self.kwargs['config'])
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
            {'processed': processed, 'form': form},
        )
