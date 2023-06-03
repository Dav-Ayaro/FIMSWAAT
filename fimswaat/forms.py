from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'placeholder':'username', 'autocomplete':'off'}))
    email = forms.EmailField(widget=forms.EmailInput({'placeholder':'email', 'autocomplte':'off'}))
    passwd1 = forms.CharField(widget=forms.PasswordInput({'placeholder':'********', 'autocomplete':'off'}))
    passwd2 = forms.CharField(widget=forms.PasswordInput({'placeholder':'********', 'autocomplete':'off'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput({'placeholder':'email', 'autocomplte':'off'}))
    passcode = forms.CharField(widget=forms.PasswordInput({'placeholder':'********', 'autocomplete':'off'}))