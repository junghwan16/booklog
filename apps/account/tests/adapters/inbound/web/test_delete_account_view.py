import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.account.adapters.outbound.persistence.models import AccountModel

User = get_user_model()


class DeleteAccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AccountModel.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            is_email_verified=True,
        )
        self.delete_url = reverse("delete_account")

    def test_delete_account_page_requires_login(self):
        """로그인하지 않은 사용자는 탈퇴 페이지에 접근할 수 없어야 함"""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_delete_account_page_loads_for_authenticated_user(self):
        """로그인한 사용자는 탈퇴 페이지에 접근할 수 있어야 함"""
        self.client.force_login(self.user)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "회원 탈퇴")
        self.assertContains(response, "주의사항")

    def test_delete_account_with_correct_password(self):
        """올바른 비밀번호로 계정 삭제가 성공해야 함"""
        self.client.force_login(self.user)

        response = self.client.post(
            self.delete_url, {"password": "testpassword", "confirm_deletion": True}
        )

        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

        # User should be deleted from database
        self.assertFalse(AccountModel.objects.filter(id=self.user.id).exists())

    def test_delete_account_with_wrong_password(self):
        """잘못된 비밀번호로는 계정 삭제가 실패해야 함"""
        self.client.force_login(self.user)

        response = self.client.post(
            self.delete_url, {"password": "wrongpassword", "confirm_deletion": True}
        )

        # Should stay on the same page with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "비밀번호가 올바르지 않습니다")

        # User should still exist
        self.assertTrue(AccountModel.objects.filter(id=self.user.id).exists())

    def test_delete_account_without_confirmation(self):
        """확인 체크박스 없이는 계정 삭제가 실패해야 함"""
        self.client.force_login(self.user)

        response = self.client.post(
            self.delete_url,
            {
                "password": "testpassword",
                # confirm_deletion is missing
            },
        )

        # Should stay on the same page with form error
        self.assertEqual(response.status_code, 200)

        # User should still exist
        self.assertTrue(AccountModel.objects.filter(id=self.user.id).exists())

    def test_delete_account_logs_out_user(self):
        """계정 삭제 후 사용자가 로그아웃되어야 함"""
        self.client.force_login(self.user)

        # Verify user is logged in
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

        # Delete account
        response = self.client.post(
            self.delete_url, {"password": "testpassword", "confirm_deletion": True}
        )

        # Try to access profile page - should redirect to login
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login
