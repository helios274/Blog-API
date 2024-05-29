from django.contrib import admin
from .models import BlogPost, Comment, Tag


class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author',)
    search_fields = ('title', 'author', 'tags')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)
