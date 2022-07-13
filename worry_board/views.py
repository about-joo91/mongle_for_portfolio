from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from worry_board.models import WorryBoard as WorryBoardModel
from worry_board.serializers import WorryBoardSerializer

# Create your views here.


class WorryBoardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        all_board_list = WorryBoardModel.objects.all().order_by("-create_date")
        return Response(
            {
                "boards": WorryBoardSerializer(
                    all_board_list, many=True, context={"request": request}
                ).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        request.data["author"] = request.user.id
        create_worry_board_serializer = WorryBoardSerializer(data=request.data)
        if create_worry_board_serializer.is_valid(raise_exception=True):
            create_worry_board_serializer.save()
            return Response({"message": "고민 게시글을 게시하였습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "게시에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, worry_board_id):
        update_worry_board = WorryBoardModel.objects.get(id=worry_board_id)
        update_worry_board_serializer = WorryBoardSerializer(
            update_worry_board, data=request.data, partial=True
        )
        update_worry_board_serializer.is_valid(raise_exception=True)
        update_worry_board_serializer.save()
        return Response({"message": "고민 게시글이 수정되었습니다."}, status=status.HTTP_200_OK)

    def delete(self, request, worry_board_id):
        delete_worry_board = WorryBoardModel.objects.get(id=worry_board_id)
        if delete_worry_board:
            delete_worry_board.delete()
            return Response({"message": "고민 게시글이 삭제되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "삭제에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)