from typing import Dict, List, Tuple

from rest_framework import exceptions

import unsmile_filtering
from board.models import Board as BoardModel
from board.models import BoardComment as BoardCommentModel
from board.models import BoardLike as BoardLikeModel
from board.serializers import BoardCommentSerializer, BoardSerializer, UserProfileSerializer
from my_page.services.letter_review_service import update_mongle_grade
from user.models import User as UserModel


def check_is_it_clean_text(check_content: dict[str, str]):
    """
    작성하는 데이터에 욕설이 있는지 검증하는 service
    """
    filtering_sys = unsmile_filtering.post_filtering
    result = filtering_sys.unsmile_filter(check_content)
    if result["label"] == "clean":
        return True
    return False


def get_paginated_board_data(page_num: int, author: UserModel, is_mine: str) -> Tuple[List, int]:
    """
    page_num을 통해서 board 데이터를 가져오는 service
    """

    if is_mine == "True":
        my_paginated_board_data = (
            BoardModel.objects.select_related("author")
            .prefetch_related("boardcomment_set__author")
            .prefetch_related("boardlike_set")
            .filter(author=author)
            .order_by("-create_date")[10 * (page_num - 1) : 10 + 10 * (page_num - 1)]
        )
        paginated_boards = BoardSerializer(my_paginated_board_data, many=True, context={"author": author}).data
        total_count = BoardModel.objects.filter(author=author).count()

    else:
        paginated_board_data = (
            BoardModel.objects.select_related("author")
            .prefetch_related("boardcomment_set__author")
            .prefetch_related("boardlike_set")
            .all()
            .order_by("-create_date")[10 * (page_num - 1) : 10 + 10 * (page_num - 1)]
        )

        paginated_boards = BoardSerializer(paginated_board_data, many=True, context={"author": author}).data
        total_count = BoardModel.objects.count()

    return paginated_boards, total_count


def create_board_data(board_data: Dict[str, str], author: UserModel) -> None:
    """
    board 데이터를 작성하는 service
    """
    create_board_serializer = BoardSerializer(data=board_data)
    create_board_serializer.is_valid(raise_exception=True)

    update_mongle_grade(user=author, grade=1, rate_type="board")
    create_board_serializer.save(author=author)


def update_board_data(board_id: int, update_data: Dict[str, str], author: UserModel) -> None:
    """
    board 데이터를 업데이트 하는 service
    """
    update_board = BoardModel.objects.get(id=board_id)
    if author != update_board.author:
        raise exceptions.PermissionDenied
    update_board_serializer = BoardSerializer(update_board, data=update_data, partial=True)
    update_board_serializer.is_valid(raise_exception=True)
    update_board_serializer.save()


def delete_board_data(board_id: int, author: UserModel) -> None:
    """
    board 데이터를 삭제하는 service
    """
    delete_model = BoardModel.objects.get(id=board_id)
    if author != delete_model.author:
        raise exceptions.PermissionDenied
    delete_model.delete()


def make_like_data(author: UserModel, board_id: int) -> None:
    """
    like 데이터를 만드는 service
    """
    target_board = BoardModel.objects.get(id=board_id)
    BoardLikeModel.objects.create(author=author, board=target_board)


def delete_like_data(author: UserModel, board_id: int) -> None:
    """
    like 데이터를 삭제하는 service
    """
    target_board = BoardModel.objects.get(id=board_id)
    liked_board = BoardLikeModel.objects.get(author=author, board=target_board)
    liked_board.delete()


def get_board_comment_data(board_id: int, author: UserModel) -> List:
    """
    해당 board의 comment 데이터의 댓글을 불러오는 service
    """

    board_comment_data = (
        BoardModel.objects.prefetch_related("boardcomment_set")
        .prefetch_related("boardlike_set")
        .select_related("author")
        .filter(id=board_id)
    )
    board_comments = BoardSerializer(board_comment_data, many=True, context={"author": author}).data
    return board_comments


def create_board_comment_data(author: UserModel, board_id: int, create_data: Dict) -> None:
    """
    해당 board의 comment 데이터를 만드는 service
    """

    board = BoardModel.objects.get(id=board_id)
    create_board_comment_serializer = BoardCommentSerializer(data=create_data)
    create_board_comment_serializer.is_valid(raise_exception=True)
    create_board_comment_serializer.save(author=author, board=board)


def update_board_comment_data(update_data: Dict, comment_id: int) -> None:
    """
    해당 board의 comment 데이터를 수정하는 service
    """
    update_comment = BoardCommentModel.objects.get(id=comment_id)
    update_comment_serializer = BoardCommentSerializer(update_comment, data=update_data, partial=True)
    update_comment_serializer.is_valid(raise_exception=True)
    update_comment_serializer.save()


def delete_board_comment_data(comment_id: int, author: UserModel) -> None:
    """
    해당 board의 comment 데이터를 삭제하는 service
    """
    delete_comment = BoardCommentModel.objects.get(id=comment_id, author=author)
    delete_comment.delete()


def get_user_profile_data(author: UserModel):
    """
    유저프로필의 데이터를 가져오는 service
    """
    return UserProfileSerializer(author.userprofile).data


def get_paginated_my_board_data(page_num: int, author: UserModel) -> Tuple[List, int]:
    """
    page_num을 통해서 나의 board 데이터를 가져오는 service
    """

    paginated_board_data = (
        BoardModel.objects.select_related("author")
        .prefetch_related("boardlike_set")
        .prefetch_related("boardcomment_set__author")
        .filter(author=author)
        .order_by("-create_date")[10 * (page_num - 1) : 10 + 10 * (page_num - 1)]
    )
    paginated_boards = BoardSerializer(paginated_board_data, many=True, context={"author": author}).data
    total_count = BoardModel.objects.count()
    return paginated_boards, total_count
