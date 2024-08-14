from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from request.models import *

class DashboardTemplateView(LoginRequiredMixin,TemplateView):
  template_name = "dashboard/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
    
  def get_context_data(self, **kwargs):
    materials = Material.objects.count()
    prequests = PreRequest.objects.filter(status__id=4).count()
    patients = Patient.objects.count()
    mhouses = MedicalHouse.objects.count()
    context = super().get_context_data(**kwargs)
    context["title"] = 'Dashboard'
    context["dashboard"] = 'active'
    context["materials"] = materials
    context["prequests"] = prequests
    context["patients"] = patients
    context["mhouses"] = mhouses
    return context