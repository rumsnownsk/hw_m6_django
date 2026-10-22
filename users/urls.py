from django.urls import path
from users.apps import UsersConfig
from .views import RegisterView, UserLoginView
from django.contrib.auth.views import LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:products_list'), name='logout'),
]