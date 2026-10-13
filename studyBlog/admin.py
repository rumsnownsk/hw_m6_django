from django.contrib import admin
from studyBlog.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'views')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')