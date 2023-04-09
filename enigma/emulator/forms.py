from django import forms
from emulator.config import EnigmaConfig
from string import ascii_lowercase


class EnigmaConfigForm(forms.Form):
    alphabet = forms.CharField(initial=ascii_lowercase)
    rotors = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        alphabet = cleaned_data.get('alphabet')
        rotors = cleaned_data.get('rotors')
        self.config = EnigmaConfig(
            rotors.split('\n'), None, None, None, alphabet
        )

        try:
            self.config.validate()
        except AssertionError as error:
            raise forms.ValidationError(str(error))
