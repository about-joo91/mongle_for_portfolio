from django.urls import path

from board import views

urlpatterns = [
    path("", views.BoardView.as_view()),
    path("<int:board_id>", views.BoardView.as_view()),
    path("like/<int:board_id>", views.BorderLikeView.as_view()),
    path("comment/", views.BorderCommentView.as_view()),
    path("comment/<int:comment_id>", views.BorderCommentView.as_view()),
    path("search", views.SearchView.as_view()),
]
