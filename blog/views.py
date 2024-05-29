from rest_framework import viewsets, status, mixins, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from .models import BlogPost, Tag, Comment
from .serializers import (
    GetBlogPostSerializer,
    GetUserBlogPostSerializer,
    CreateUpdateBlogPostSerializer,
    ListCommentSerializer,
    CreateCommentSerializer,
    UpdateCommentSerializer,
    CreateReplySerializer,
    UpdateReplySerializer,
    TagSerializer
)
from utils.pagination import CustomPageNumPagination, CustomLimitOffsetPagination
from utils.responses import SuccessResponse
from utils.permissions import BlogPostPermission, CommentPermission
from utils import swagger_schemas

from drf_yasg.utils import swagger_auto_schema


class BlogPostViewSet(viewsets.ModelViewSet):

    queryset = BlogPost.objects.all()
    serializer_class = GetBlogPostSerializer
    pagination_class = CustomPageNumPagination
    permission_classes = [BlogPostPermission]
    lookup_field = 'slug'

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Get posts",
        operation_description="Get a list of posts with pagination"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Get a post",
        operation_description="Get a post",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Create a new post",
        operation_description="Create a new post",
        request_body=CreateUpdateBlogPostSerializer,
        responses={
            201: CreateUpdateBlogPostSerializer,
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateUpdateBlogPostSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Update a post",
        operation_description="Update a post",
        request_body=CreateUpdateBlogPostSerializer,
        responses={
            200: CreateUpdateBlogPostSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                "You do not have permission to update this post.")
        serializer = CreateUpdateBlogPostSerializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Update a post",
        operation_description="Update a post",
        request_body=CreateUpdateBlogPostSerializer,
        responses={
            200: CreateUpdateBlogPostSerializer,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Delete a post",
        operation_description="Delete a post",
        responses={
            200: swagger_schemas.SUCCESS_RES_BODY
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                "You do not have permission to delete this post.")
        self.perform_destroy(instance)
        return SuccessResponse("Post deleted successfully")


class GetUserPostsView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = GetUserBlogPostSerializer
    pagination_class = CustomPageNumPagination

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Get posts by user Id",
        operation_description="Get all posts of a user with pagination"
    )
    def get(self, request: Request, user_id=None) -> Response:
        queryset = self.queryset.filter(author=user_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetPostsByTagView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = GetUserBlogPostSerializer
    pagination_class = CustomPageNumPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        if slug:
            tag = get_object_or_404(Tag, slug=slug)
            queryset = queryset.filter(tags=tag)
        return queryset

    @swagger_auto_schema(
        tags=['Blog Post'],
        operation_summary="Get posts by a tag",
        operation_description="Get all posts with a specific tag"
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ListCreateCommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CreateCommentSerializer
    pagination_class = CustomLimitOffsetPagination

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Get comments",
        operation_description="Get a list of comments",
    )
    def get(self, request: Request, post_id=None):
        queryset = self.queryset.filter(post_id=post_id, parent=None)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListCommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ListCommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Create a new comment",
        operation_description="Create a new comment",
        request_body=CreateCommentSerializer,
    )
    def post(self, request: Request, post_id=None):
        serializer = CreateCommentSerializer(
            data=request.data, context={"user": request.user, "post_id": post_id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateDeleteCommentView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = UpdateCommentSerializer
    permission_classes = [CommentPermission]

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Update a comment",
        operation_description="Update a comment",
        request_body=UpdateCommentSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Update a comment",
        operation_description="Update a comment",
        request_body=UpdateCommentSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Delete a comment",
        operation_description="Delete a comment",
        responses={
            200: swagger_schemas.SUCCESS_RES_BODY
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse("Comment deleted successfully")


class CreateReplyView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateReplySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Create a new reply",
        operation_description="Create a new reply",
        request_body=CreateReplySerializer,
    )
    def post(self, request: Request, comment_id=None):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user, "comment_id": comment_id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateDeleteReplyView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = UpdateReplySerializer
    permission_classes = [CommentPermission]

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Update a reply",
        operation_description="Update a reply",
        request_body=UpdateReplySerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Update a reply",
        operation_description="Update a reply",
        request_body=UpdateReplySerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Comments and Replies'],
        operation_summary="Delete a reply",
        operation_description="Delete a reply",
        responses={
            200: swagger_schemas.SUCCESS_RES_BODY
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse("Reply deleted successfully.")


# Create and list tags
class CreateListTagsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = [CustomPagination]

    @swagger_auto_schema(
        tags=['Tags'],
        operation_summary="Get tags",
        operation_description="Get a list of tags",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Tags'],
        operation_summary="Create a new tag",
        operation_description="Create a new tag",
        request_body=TagSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
