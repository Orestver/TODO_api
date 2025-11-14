from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Login", 
                               max_length=150,
                               widget=forms.TextInput(attrs={'class': "input-field"}))
    password = forms.CharField(label="password", 
                               widget=forms.PasswordInput(attrs={'class': "input-field"}))
