from django import forms


class ResendVerificationEmailForm(forms.Form):
    email = forms.EmailField(label="E-mail")
