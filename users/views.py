from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

# Create your views here.

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:products_list')



class UserLoginView(LoginView):
    template_name = 'users/login.html'  # <-- путь к твоему шаблону login.html
    form_class = CustomUserLoginForm
    redirect_authenticated_user = True  # если залогинен, не пускать на страницу логина
    # success_url = reverse_lazy('catalog:products_list')

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     return redirect('catalog:products_list')


