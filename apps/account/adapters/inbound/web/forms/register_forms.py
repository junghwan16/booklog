from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    nickname = forms.CharField(max_length=32, label="닉네임")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="비밀번호 확인"
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password_confirm"):
            self.add_error("password_confirm", "비밀번호가 일치하지 않습니다.")
        return cleaned
