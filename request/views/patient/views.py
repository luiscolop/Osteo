from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from request.forms import *
from request.models import *
from django.urls import reverse_lazy

class PatientListView(LoginRequiredMixin,ListView):
  model = Patient
  template_name = "patient/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_queryset(self):
    return Patient.objects.all().order_by('-pk')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Pacientes'
    context["madmins"] = 'menu-open'
    context["patient"] = 'active'
    return context

class PatientCreateView(LoginRequiredMixin,CreateView):
  model = Patient
  form_class = PatientForm
  template_name = "patient/create.html"
  
  def get_success_url(self):
    messages.success(self.request, '¡Paciente agregado con éxito!')
    return reverse_lazy('request:patient')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Nuev@ paciente'
    return context

class PatientUpdateView(UpdateView):
  model = Patient
  form_class = PatientForm
  template_name = "patient/edit.html"

  def get_success_url(self):
    messages.success(self.request, '¡Registro editado con éxito!')
    return reverse_lazy('request:patient')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Editar registro de paciente'
    return context