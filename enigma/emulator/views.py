from django.views.generic import FormView
from django.urls.base import reverse
from django.shortcuts import HttpResponse, redirect, render

from .forms import EnigmaConfigForm, EnigmaEmulatorForm, EnigmaFileConfigForm
from .config import EnigmaConfig
from .emulator import EnigmaEmulator


def response_file(data, filename):
    response = HttpResponse(
        data.encode('utf-8'),
        content_type='text/plaing',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


class EnigmaConfigView(FormView):
    template_name = 'config.html'
    form_class = EnigmaConfigForm

    def form_valid(self, form):
        if 'export_file' in self.request.POST:
            return response_file(form.config.dump_yaml(), 'config.yml')

        return redirect(
            reverse(
                'emulator:emulator',
                kwargs={'config': form.config.encode()},
            )
        )


class EnigmaFileConfigView(FormView):
    template_name = 'file_config.html'
    form_class = EnigmaFileConfigForm

    def form_valid(self, form):
        yaml = form.cleaned_data.get('file').read().decode('utf-8').strip()

        try:
            config = EnigmaConfig.load_yaml(yaml)
        except Exception:
            form.add_error('Unable to parse file')
            return render(self.request, self.template_name, {'form': form})

        return redirect(
            reverse('emulator:emulator', kwargs={'config': config.encode()})
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

        if 'export_file' in self.request.POST:
            return response_file(processed, 'output.txt')

        return render(
            self.request,
            self.template_name,
            {
                'processed': processed,
                'form': form,
                'config': emulator.get_current_config(),
            },
        )
