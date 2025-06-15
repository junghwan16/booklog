from django import forms


class ProfileForm(forms.Form):
    nickname = forms.CharField(max_length=32, label="닉네임", required=False)
