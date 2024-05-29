from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class BlogPost(models.Model):
    thumbnail = models.ImageField(upload_to="thumbnails/")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    content = models.TextField(default=None)
    tags = models.ManyToManyField('Tag', related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title != self._old_title or not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_title = self.title

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by @{self.author.username}'


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class Paragraph(models.Model):
#     post = models.ForeignKey(
#         BlogPost, on_delete=models.CASCADE, related_name='paragraphs')
#     order = models.PositiveIntegerField()
#     content = models.TextField()


# class Image(models.Model):
#     post = models.ForeignKey(
#         BlogPost, on_delete=models.CASCADE, related_name='images')
#     position = models.PositiveIntegerField()
#     image = models.ImageField(upload_to='blog_images/')
