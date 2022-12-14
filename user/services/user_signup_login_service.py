from typing import Dict

from django.db import transaction

from user.models import CertificationQuestion, User
from user.serializers import NewPasswordSerializer, UserSignupSerializer


def get_user_signup_data(user: User) -> Dict:
    """
    유저 정보를 get
    """
    return UserSignupSerializer(user).data


@transaction.atomic
def post_user_signup_data(user_data: Dict) -> None:
    """
    회원가입
    """
    user_data_serializer = UserSignupSerializer(data=user_data)
    user_data_serializer.is_valid(raise_exception=True)
    user_data_serializer.save()


def check_password_in_signup_data(password_data: Dict) -> bool:
    """
    회원가입시 비밀번호 대조
    """
    password = password_data["password"]
    check_password = password_data["check_password"]
    return password == check_password


def get_certification_question_list() -> list:
    """
    회원가입시 고르는 certification_question 목록 가져오기
    """
    certification_questions = CertificationQuestion.objects.all()
    certification_question_list = []
    for question in certification_questions:
        certification_question_list.append(question.certification_question)
    return certification_question_list


def check_is_user(username: str):
    """
    username을 기반으로 User모델에서 탐색
    """
    check_user = User.objects.get(username=username)
    return check_user


def check_certification_question(certification_data: Dict[str, str]):
    """
    유저의 본인확인 질문 매칭
    """
    author = User.objects.get(username=certification_data["username"])
    return author.certification_answer == certification_data["certification_answer"]


def update_user_certification_question(user_id: int, update_data: Dict[str, str]):
    """
    유저의 본인확인 질문 업데이트
    """
    user = User.objects.filter(id=user_id)
    certification_question_id = update_data["certification_question"]
    certification_answer = update_data["certification_answer"]
    user.update(certification_question=certification_question_id, certification_answer=certification_answer)


def check_certification_is_none(check_data: Dict[str, str]):
    """
    본인확인 질문이 비어있는지 체크
    """
    certification_question_id = check_data["certification_question"]
    certification_answer = check_data["certification_answer"]

    return bool(certification_question_id and certification_answer)


def update_user_new_password(update_data: Dict) -> None:
    """
    비밀번호 새로 설정
    """
    username = update_data.pop("username")
    user = User.objects.get(username=username)
    update_user_serializer = NewPasswordSerializer(user, data=update_data, partial=True)
    update_user_serializer.is_valid(raise_exception=True)
    update_user_serializer.save()
