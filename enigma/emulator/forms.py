from django import forms
from string import ascii_uppercase

from emulator.config import EnigmaConfig, random_config


class EnigmaConfigForm(forms.Form):
    alphabet = forms.CharField()
    rotors = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
    )
    reflector = forms.CharField()
    plugs = forms.CharField()
    positions = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        config = random_config(3, ascii_uppercase)
        self.fields['alphabet'].initial = config.alphabet
        self.fields['rotors'].initial = '\n'.join(config.rotors)
        self.fields['reflector'].initial = config.reflector
        self.fields['plugs'].initial = ' '.join(config.plugs)
        self.fields['positions'].initial = ' '.join(map(str, config.positions))

    def clean(self):
        cleaned_data = super().clean()
        alphabet = cleaned_data.get('alphabet')
        rotors = cleaned_data.get('rotors')
        reflector = cleaned_data.get('reflector')
        plugs = cleaned_data.get('plugs')
        positions = cleaned_data.get('positions')

        if any([not p.isnumeric() for p in positions.split()]):
            raise forms.ValidationError('Positions should be numbers')

        self.config = EnigmaConfig(
            rotors.replace('\r', '').split('\n'),
            reflector,
            plugs.split(),
            [int(p) for p in positions.split()],
            alphabet,
        )

        try:
            self.config.validate()
        except AssertionError as error:
            raise forms.ValidationError(str(error))


class EnigmaFileConfigForm(forms.Form):
    file = forms.FileField()


class EnigmaEmulatorForm(forms.Form):
    message = forms.CharField(required=False)
    file = forms.FileField(required=False)
