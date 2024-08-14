from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from request.forms import *
from request.models import *
from django.urls import reverse_lazy

class MedicalHouseListView(ListView):
  model = MedicalHouse
  template_name = "mhouse/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_queryset(self):
    return MedicalHouse.objects.all().order_by('-pk')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Casa médica'
    context["madmins"] = 'menu-open'
    context["mhouse"] = 'active'
    return context

class MedicalHouseCreateView(CreateView):
  model = MedicalHouse
  form_class = MedicalHouseForm
  template_name = "mhouse/create.html"
  
  def get_success_url(self):
    messages.success(self.request, '¡Casa médica agregada con éxito!')
    return reverse_lazy('request:mhouse')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Nueva casa médica'
    return context

class MedicalHouseUpdateView(UpdateView):
  model = MedicalHouse
  form_class = MedicalHouseForm
  template_name = "mhouse/edit.html"

  def get_success_url(self):
    messages.success(self.request, '¡Registro editado con éxito!')
    return reverse_lazy('request:mhouse')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Editar registro de casa médica'
    return context