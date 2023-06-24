from django import forms


class RegistrationForm(forms.Form):
    fullName = forms.CharField(widget=forms.TextInput({'placeholder':'Full Name', 'autocomplete':'off'}))
    email = forms.EmailField(widget=forms.EmailInput({'placeholder':'email', 'autocomplte':'off'}))
    department = forms.CharField(widget=forms.TextInput({'placeholder':'Department', 'autocomplete':'off'}))
    empId = forms.IntegerField(widget=forms.NumberInput({'placeholder':'EmployeeId', 'autocomplete':'off'}))
    officeName = forms.CharField(widget=forms.TextInput({'placeholder':'Office Name', 'autocomplete':'off'}))
    officeCode = forms.IntegerField(widget=forms.NumberInput({'placeholder':'Office Code', 'autocomplete':'off'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput({'placeholder':'email', 'autocomplte':'off'}))
    passcode = forms.CharField(widget=forms.PasswordInput({'placeholder':'********', 'autocomplete':'off'}))

class ChangePassword(forms.Form):
    pwd = forms.CharField(widget=forms.PasswordInput({'placeholder':'enter strong password'}), label='Password')
    pwd_rpt = forms.CharField(widget=forms.PasswordInput({'placeholder':'confirm password'}), label='Confirm Password')
