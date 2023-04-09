from django import forms
from emulator.config import EnigmaConfig
from string import ascii_uppercase


class EnigmaConfigForm(forms.Form):
    alphabet = forms.CharField(initial=ascii_uppercase)
    rotors = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        initial=f'{ascii_uppercase}\n{ascii_uppercase}\n{ascii_uppercase}',
    )
    reflector = forms.CharField(initial=ascii_uppercase)

    def clean(self):
        cleaned_data = super().clean()
        alphabet = cleaned_data.get('alphabet')
        rotors = cleaned_data.get('rotors')
        reflector = cleaned_data.get('reflector')

        self.config = EnigmaConfig(
            rotors.replace('\r', '').split('\n'),
            reflector,
            None,
            None,
            alphabet,
        )

        try:
            self.config.validate()
        except AssertionError as error:
            raise forms.ValidationError(str(error))
