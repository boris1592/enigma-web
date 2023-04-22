from django import forms
from string import ascii_uppercase

from emulator.config import EnigmaConfig


class EnigmaConfigForm(forms.Form):
    alphabet = forms.CharField(initial=ascii_uppercase)
    rotors = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        initial=f'{ascii_uppercase}\n{ascii_uppercase}\n{ascii_uppercase}',
    )
    reflector = forms.CharField(initial=ascii_uppercase)
    plugs = forms.CharField(initial='AB DC')
    positions = forms.CharField(initial='1 2 3')

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


class EnigmaEmulatorForm(forms.Form):
    message = forms.CharField()
