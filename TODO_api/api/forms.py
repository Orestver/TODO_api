from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Login", max_length=150)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
