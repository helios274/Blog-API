from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BlogPostViewSet,
    GetUserPostsView,
    GetPostsByTagView,
    ListCreateCommentView,
    CreateListTagsViewSet,
    UpdateDeleteCommentView,
    CreateReplyView,
    UpdateDeleteReplyView
)

router = DefaultRouter()

router.register("", BlogPostViewSet, basename="blogs")
router.register("tags", CreateListTagsViewSet, basename="tags")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:post_id>/comments/",
         ListCreateCommentView.as_view(),
         name='get_post_comments'),
    path("comments/<int:pk>/",
         UpdateDeleteCommentView.as_view(),
         name='comment'),
    path("comments/<int:comment_id>/reply/",
         CreateReplyView.as_view(),
         name='reply'),
    path("comments/reply/<int:pk>/",
         UpdateDeleteReplyView.as_view(),
         name='reply'),
    path("user/<int:user_id>/",
         GetUserPostsView.as_view(),
         name='get_user_posts'),
    path("tag/<slug:slug>/",
         GetPostsByTagView.as_view(),
         name="get_posts_by_tag"),
]
