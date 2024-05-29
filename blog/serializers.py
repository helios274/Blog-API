from rest_framework import serializers
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import BlogPost, Comment, Tag


User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_photo']


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ReplySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content']


class ListCommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content',
                  'created_at', 'updated_at', 'replies',]


class CreateCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['post']

    def create(self, validated_data):
        user = self.context.get('user')
        post_id = self.context.get('post_id')
        post = get_object_or_404(BlogPost, id=post_id)
        comment = Comment.objects.create(
            author=user, post=post, **validated_data)
        return comment


class UpdateCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context.get('user')
        post_id = self.context.get('post_id')
        print(post_id)
        post = get_object_or_404(BlogPost, id=post_id)
        comment = Comment.objects.create(
            author=user, post=post, **validated_data)
        return comment


class CreateReplySerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['parent']

    def create(self, validated_data):
        user = self.context.get('user')
        comment_id = self.context.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.parent:
            raise serializers.ValidationError("Cannot reply to a reply")
        reply = Comment.objects.create(
            author=user, parent=comment, **validated_data)
        return reply


class UpdateReplySerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['parent']


class GetBlogPostSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)
    slug = serializers.SlugField(read_only=True)
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id',  'thumbnail', 'title', 'slug', 'author', 'content', 'tags', 'created_at',
                  'updated_at']


class GetUserBlogPostSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)
    slug = serializers.SlugField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id',  'thumbnail', 'title', 'slug', 'content', 'tags', 'created_at',
                  'updated_at']


class CreateUpdateBlogPostSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)
    slug = serializers.SlugField(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id',  'thumbnail', 'title', 'slug', 'author', 'content', 'tags', 'created_at',
                  'updated_at']

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = BlogPost.objects.create(
            author=self.context["user"], **validated_data)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        instance.thumbnail = validated_data.get(
            'thumbnail', instance.thumbnail)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag in tags_data:
                instance.tags.add(tag)

        return instance
