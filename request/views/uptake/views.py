from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, View, TemplateView
from request.forms import *
from request.models import *
from django.db import transaction
from django.urls import reverse_lazy
from datetime import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class UptakeListView(LoginRequiredMixin,ListView):
  model = Uptake
  template_name = "uptake/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_queryset(self):
    return Uptake.objects.all().order_by('-id')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Hojas de consumo'
    context["mprequest"] = 'menu-open'
    context["uptake"] = 'active'
    return context
  
class UptakeCreateView(LoginRequiredMixin,CreateView):
  model = Uptake
  form_class = UptakeForm
  template_name = "uptake/create.html"

  def get_success_url(self):
    messages.success(self.request, '¡Hoja de consumo ingresado con éxito!')
    return reverse_lazy('request:prerequest')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def generate_number(self):
    year = datetime.now()
    if Uptake.objects.count() > 0:
      next_code = Uptake.objects.latest('id').id + 1
      next_code = str(next_code)
      next_code.zfill(3)
    else:
      next_code = '1'
      next_code.zfill(3)
    return "{}/{}".format(next_code,year.strftime("%Y"))
  
  def post(self, request, *args, **kwargs):
    utkid=0
    try:
      with transaction.atomic():
        get_house = MedicalHouse.objects.get(pk=request.POST['house'])
        get_prequest = PreRequest.objects.get(pk=request.POST['prequest_id']) 
        # add new pre request
        new_uptake = Uptake.objects.create(
          number = self.generate_number(),
          operating_room = request.POST['operating_room'],
          surgeon = request.POST['surgeon'],
          instrumentalist = request.POST['instrumentalist'],
          circulating = request.POST['circulating'],
          pre_request = get_prequest,
          house = get_house, 
          user = self.request.user,
        )
        new_uptake.save()

        # add detail pre request
        materials = request.POST.getlist('material_id[]')
        amounts = request.POST.getlist('amount[]')
        i = 0
        for item in materials:
          get_material = Material.objects.get(pk=item)
          new_detail = UptakeDetail.objects.create(
            amount = amounts[i],
            material = get_material,
            uptake = new_uptake
          )
          new_detail.save()
          i += 1
        utkid=new_uptake.pk

    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest_create')
    return HttpResponseRedirect("/uptake/{}/format/".format(utkid))
    
  def get_context_data(self, **kwargs):
    prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
    detail = PreRequestDetail.objects.filter(pre_request__id=prequest.pk)
    context = super().get_context_data(**kwargs)
    context["prerequest"] = prequest
    context["prdetail"] = detail
    context["title"] = 'Consumo de presolicitud'
    context["mprequest"] = 'menu-open'
    context["prequest"] = 'active'
    return context

class UptakeValidateView(LoginRequiredMixin,TemplateView):
  template_name = "uptake/validate.html"

  def get_context_data(self, **kwargs):
    prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
    uptake = Uptake.objects.get(pre_request__id=prequest.pk)
    detail = UptakeDetail.objects.filter(uptake__id=uptake.pk)
    option = ""
    more = False
    if prequest.status.pk == 13:
      option = "/uptake/{}/store/".format(prequest.pk)
    elif prequest.status.pk == 14:
      option = "/uptake/{}/shopping/".format(prequest.pk)
    elif prequest.status.pk == 15:
      option = "/uptake/{}/paid/".format(prequest.pk)

    context = super().get_context_data(**kwargs)
    context["title"] = 'Validar pre solicitud'
    context["prequest"] = prequest
    context["uptake"] = uptake
    context["detail"] = detail
    context["option"] = option
    return context

class UptakeStoreView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Hoja de consumo enviado a bodega con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.hcstore()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())

class UptakeShoppingView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Hoja de consumo enviado a compras con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.hcshoppig()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())

class UptakePaidView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud pagada con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.paid()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())
  
class UptakePdfView(LoginRequiredMixin,View):
  def get(self, request, *args, **kwargs):
    template = get_template('uptake/report.html')
    uptake = Uptake.objects.get(pk=self.kwargs['pk'])
    prequest = PreRequest.objects.get(pk=uptake.pre_request.pk)
    context = {
      'prequest': prequest,
      'uptake' : uptake,
      'detail': UptakeDetail.objects.filter(uptake__id=self.kwargs['pk']),
    }
    html = template.render(context)
    response = HttpResponse(content_type = 'application/pdf')
    prequest.taking()
    # response['Content-Disposition'] = 'attachment; filename=reportedeventas.pdf'
    pisaStatus = pisa.CreatePDF(html, dest = response)
    if pisaStatus.err:
      return HttpResponse('Ocurrieron algunos errores <pre>'+ html +'</pre>')
    return response
