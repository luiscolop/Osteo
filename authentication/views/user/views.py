from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy

class UserListView(LoginRequiredMixin,ListView):
  model = User
  template_name = "user/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_queryset(self):
    return User.objects.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Usuarios'
    context["madmin"] = 'menu-open'
    context["user"] = 'active'
    return context

class UserCreateView(CreateView):
  model = User
  form_class = UserCreationForm
  template_name = 'user/create.html'

  def get_success_url(self):
    return reverse_lazy('authentication:user')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class UserUpdateView(LoginRequiredMixin,UpdateView):
  model = User
  form_class = UserChangeForm
  template_name = "user/edit.html"

  def get_success_url(self):
    messages.success(self.request, '¡Usuario editado con éxito!')
    return reverse_lazy('mark:user_list')

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context