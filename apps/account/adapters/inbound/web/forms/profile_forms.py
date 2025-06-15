from django import forms


class ProfileForm(forms.Form):
    nickname = forms.CharField(max_length=32, label="닉네임", required=False)


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="현재 비밀번호",
        help_text="계정 삭제를 위해 현재 비밀번호를 입력해주세요.",
    )
    confirm_deletion = forms.BooleanField(
        label="계정 삭제에 동의합니다",
        help_text="이 작업은 되돌릴 수 없습니다. 모든 데이터가 영구적으로 삭제됩니다.",
        required=True,
    )
