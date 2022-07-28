from django.test import TestCase
from rest_framework.exceptions import ValidationError

from main_page.models import WorryCategory
from user.models import User as UserModel
from worry_board.models import RequestMessage as RequestMessageModel
from worry_board.models import WorryBoard as WorryBoardModel
from worry_board.services.worry_board_request_message_service import (
    create_request_message_data,
    delete_request_message_data,
    get_paginated_request_message_data,
    update_request_message_data,
)
from worry_board.services.worry_board_service import check_is_it_clean_text


class TestWorryBoardRequestMessageService(TestCase):
    """
    Worry_Board의 Request_Message 서비스 함수들을 검증하는 클래스
    """

    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(username="Ko", nickname="Ko")
        category = WorryCategory.objects.create(cate_name="일상")
        WorryBoardModel.objects.create(
            author=user, category=category, content="더미object"
        )

    def test_when_success_get_paginated_request_message_data(self) -> None:
        """
        pagenation을 통하여 내가 보내거나 받은
        request_message를 가져오는 함수에 대한 검증
        """
        page_num = 1
        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        case = "sended"
        RequestMessageModel.objects.create(author=user, worry_board=worry_board)
        paginated_request_message, total_count = get_paginated_request_message_data(
            page_num, case, user
        )

        self.assertEqual(1, total_count)
        self.assertEqual(
            WorryBoardModel.objects.all()[0].id,
            WorryBoardModel.objects.get(author=user).id,
        )
        self.assertEqual(
            paginated_request_message[0],
            RequestMessageModel.objects.filter(author=user)[0],
        )

    def test_when_success_create_request_message_data(self) -> None:
        """
        request_message_data를 생성하는 함수가 정상적으로 작동되었을 때에 대한 검증
        """
        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        request_message_data = {"request_message": "request_message 생성중"}
        if check_is_it_clean_text(request_message_data["request_message"]):
            create_request_message_data(user, worry_board.id, request_message_data)

        self.assertEqual(
            RequestMessageModel.objects.all()[0].id,
            RequestMessageModel.objects.get(author=user).id,
        )

    def test_when_success_update_request_message_data(self) -> None:
        """
        request_message_data를 수정하는 함수가 정상적으로 작동되었을 때에 대한 검증
        """

        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        create_request_message = RequestMessageModel.objects.create(
            author=user, worry_board=worry_board, request_message="test"
        )

        request_message_data = {"request_message": "request_message 생성중"}

        if check_is_it_clean_text(request_message_data["request_message"]):
            update_request_message_data(
                for_updata_date=request_message_data,
                request_message_id=create_request_message.id,
            )

        self.assertEqual(
            create_request_message.id, RequestMessageModel.objects.get(author=user).id
        )
        self.assertEqual(
            RequestMessageModel.objects.all()[0].request_message,
            RequestMessageModel.objects.get(author=user).request_message,
        )

    def test_when_success_delete_request_message_data(self) -> None:
        """
        request_message_data를 삭제하는 함수가 정상적으로 작동 되었을 때에 대한 검증
        """
        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        create_request_message = RequestMessageModel.objects.create(
            author=user, worry_board=worry_board, request_message="test"
        )

        delete_request_message_data(request_message_id=create_request_message.id)

        self.assertEqual(0, RequestMessageModel.objects.count())

    def test_when_post_including_swear_word_in_create_request_message_data(
        self,
    ) -> None:
        """
        request_message를 작성할 때 욕설이 포함되어 있을 때에 대한 검증
        """
        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        request_message_data = {"request_message": "바보같은놈"}
        if check_is_it_clean_text(request_message_data["request_message"]):
            create_request_message_data(
                author=user,
                worry_board_id=worry_board.id,
                request_message=request_message_data,
            )

        with self.assertRaises(RequestMessageModel.DoesNotExist):
            RequestMessageModel.objects.get(author=user).id

    def test_when_worry_board_does_not_exist_in_create_request_message_data(
        self,
    ) -> None:
        """
        request_message를 작성할 때 worry_baord가 없을 경우에 대한 검증
        """
        user = UserModel.objects.get(id=1)
        request_message_data = {"request_message": "worry_board_none"}
        if check_is_it_clean_text(request_message_data["request_message"]):
            with self.assertRaises(ValidationError):
                create_request_message_data(
                    author=user, worry_board_id=10, request_message=request_message_data
                )

        with self.assertRaises(RequestMessageModel.DoesNotExist):
            RequestMessageModel.objects.get(author=user).id

    def test_when_request_message_does_not_exist_in_update_request_message_data(
        self,
    ) -> None:
        """
        request_message를 수정할 때 request_message 없는 경우에 대한 검증
        """
        update_data = {"request_message": "수정함"}

        with self.assertRaises(RequestMessageModel.DoesNotExist):
            update_request_message_data(update_data, request_message_id=10)

    def test_when_over_request_message_lengths_120_in_create_request_message_data(
        self,
    ) -> None:
        """
        request_message를 생성하는 함수가
        request_message의 제한수인 120을 넘겼을 경우에 대한 검증
        """
        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        create_data = {
            "request_message": "120자를 넘기는지에 대한 검증입니다. 조금 길더라도 양해 바랍니다. 120자를 넘기는지에 대한 검증입니다. 조금 길더라도 양해 바랍니다.  120자를 넘기는지에 대한 검증입니다. 조금 길더라도 양해 바랍니다. 120자를 넘기는지에 대한 검증입니다. 조금 길더라도 양해 바랍니다. 120자를 넘기는지에 대한 검증입니다. 조금 길더라도 양해 바랍니다."
        }

        with self.assertRaises(ValidationError):
            if check_is_it_clean_text(create_data["request_message"]):
                create_request_message_data(
                    author=user,
                    worry_board_id=worry_board.id,
                    request_message=create_data,
                )

    def test_when_post_including_swear_word_in_update_request_message_data(
        self,
    ) -> None:
        """
        request_message를 수정하는 함수가
        욕설을 포함하였을 경우에 대한 검증
        """

        user = UserModel.objects.get(id=1)
        worry_board = WorryBoardModel.objects.get(id=1)
        create_request_message = RequestMessageModel.objects.create(
            author=user, worry_board=worry_board, request_message="test"
        )

        request_message_data = {"request_message": "바보같은놈"}

        if check_is_it_clean_text(request_message_data["request_message"]):
            update_request_message_data(
                for_updata_date=request_message_data,
                request_message_id=create_request_message.id,
            )

        with self.assertRaises(RequestMessageModel.DoesNotExist):
            RequestMessageModel.objects.get(request_message="바보같은놈")
