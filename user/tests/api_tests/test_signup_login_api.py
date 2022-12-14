from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import CertificationQuestion as CertificationQuestionModel
from user.models import MongleLevel
from user.models import User as UserModel


class TestUserRegistrationAPI(APITestCase):
    """
    회원가입 API 테스트 코드
    """

    @classmethod
    def setUpTestData(cls):
        MongleLevel.objects.create(
            id=1,
        )

    def test_signup(self) -> None:
        url = reverse("user_view")
        certification_question = CertificationQuestionModel.objects.create(certification_question="질문")
        user_data = {
            "username": "won1",
            "password": "qwer1234%",
            "check_password": "qwer1234%",
            "nickname": "won1122",
            "certification_question": certification_question.id,
            "certification_answer": "답변",
        }
        response = self.client.post(url, user_data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["detail"], "회원가입을 성공하였습니다")


class LoginTestCase(APITestCase):
    """
    로그인 테스트코드
    """

    def setUp(self) -> None:
        self.data = {"username": "won1234", "password": "qwer1234%"}
        self.user = UserModel.objects.create(username="won1234", nickname="won1122")
        self.user.set_password("qwer1234%")
        self.user.save()

    def test_login(self):
        response = self.client.post(reverse("token_obtain_pair"), self.data)
        self.assertEqual(response.status_code, 200)
