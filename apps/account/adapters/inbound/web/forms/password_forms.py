from django import forms


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="현재 비밀번호")
    new_password = forms.CharField(widget=forms.PasswordInput, label="새 비밀번호")
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="새 비밀번호 확인"
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password") != cleaned.get("new_password_confirm"):
            self.add_error("new_password_confirm", "새 비밀번호가 일치하지 않습니다.")
        return cleaned


class ResetPasswordRequestForm(forms.Form):
    email = forms.EmailField(label="가입 이메일")


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="새 비밀번호")
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="새 비밀번호 확인"
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password") != cleaned.get("new_password_confirm"):
            self.add_error("new_password_confirm", "비밀번호가 일치하지 않습니다.")
        return cleaned
