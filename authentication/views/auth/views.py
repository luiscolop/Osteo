from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
import misitio.settings as setting

class LoginFormView(LoginView):
  template_name = 'auth/login.html'
  
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(setting.LOGIN_REDIRECT_URL)
    return super().dispatch(request, *args, **kwargs)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Inicio de sesión'
    return context