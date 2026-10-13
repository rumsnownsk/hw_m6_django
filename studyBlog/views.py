from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import F
from .models import Post

# Список постов (только опубликованные)
class PostListView(ListView):
    model = Post
    template_name = 'studyBlog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        # Показываем только опубликованные посты
        return Post.objects.filter(is_published=True)

# Один пост (с увеличением просмотров)
class PostDetailView(DetailView):
    model = Post
    template_name = 'studyBlog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Атомарно увеличиваем счётчик просмотров
        Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return Post.objects.get(pk=obj.pk)

# Создание поста
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'studyBlog/post_form.html'
    success_url = reverse_lazy('studyBlog:post_list')

# Редактирование поста
class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'studyBlog/post_form.html'
    success_url = reverse_lazy('studyBlog:post_list')

# Удаление поста
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'studyBlog/post_confirm_delete.html'
    success_url = reverse_lazy('studyBlog:post_list')


