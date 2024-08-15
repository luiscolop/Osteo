from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, View, TemplateView, DeleteView, UpdateView
from request.forms import *
from request.models import *
from django.db import transaction
from django.urls import reverse_lazy
from datetime import date, datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class PreRequestListView(LoginRequiredMixin,ListView):
  model = PreRequest
  template_name = "prequest/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_queryset(self):
    return PreRequest.objects.all().order_by('-id')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Pre solicitudes'
    context["mprequest"] = 'menu-open'
    context["prequest"] = 'active'
    return context

class PreRequestCreateView(CreateView):
  model = PreRequest
  form_class = PreRequestForm
  template_name = "prequest/create.html"

  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud ingresada con éxito!')
    return reverse_lazy('request:prerequest')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def generate_number(self):
    year = datetime.now()
    if PreRequest.objects.count() > 0:
      next_code = PreRequest.objects.latest('id').id + 1
      next_code = str(next_code)
      next_code.zfill(3)
    else:
      next_code = '1'
      next_code.zfill(3)
    return "{}/{}".format(next_code,year.strftime("%Y"))
  
  def post(self, request, *args, **kwargs):
    prqid=0
    try:
      with transaction.atomic():
        get_patient = Patient.objects.get(pk=request.POST['patient'])
        if 'house_id[]' in request.POST:
          house = request.POST.getlist('house_id[]')
          get_house = MedicalHouse.objects.get(pk=int(house[0]))
          new_prerequest = PreRequest.objects.create(
            number = self.generate_number(),
            diagnosis = request.POST['diagnosis'],
            procedure = request.POST['procedure'],
            service = request.POST['service'],
            bed = request.POST['bed'],
            operation = request.POST['operation'],
            comment = request.POST['comment'],
            stock = True,
            house = get_house,
            patient = get_patient,
            user = self.request.user,
          )
          new_prerequest.save()
          # add detail pre request
          lots= request.POST.getlist('lot_id[]')
          amounts = request.POST.getlist('amount[]')
          i = 0
          for item in lots:
            get_lot = Lot.objects.get(pk=item)
            new_detail = PreRequestDetail.objects.create(
              amount = amounts[i],
              lot = get_lot,
              pre_request = new_prerequest
            )
            new_detail.save()
            new_detail.lot.stock -= float(amounts[i])
            new_detail.lot.save()
            i += 1
          prqid=new_prerequest.pk
        else:# add new pre request
          get_house = MedicalHouse.objects.get(pk=request.POST['house'])
          new_prerequest = PreRequest.objects.create(
            number = self.generate_number(),
            diagnosis = request.POST['diagnosis'],
            procedure = request.POST['procedure'],
            service = request.POST['service'],
            bed = request.POST['bed'],
            operation = request.POST['operation'],
            comment = request.POST['comment'],
            patient = get_patient,
            house = get_house, 
            user = self.request.user,
          )
          new_prerequest.save()

          # add detail pre request
          materials = request.POST.getlist('material_id[]')
          amounts = request.POST.getlist('amount[]')
          i = 0
          for item in materials:
            get_material = Material.objects.get(pk=item)
            new_detail = PreRequestDetail.objects.create(
              amount = amounts[i],
              material = get_material,
              pre_request = new_prerequest
            )
            new_detail.save()
            i += 1
          prqid=new_prerequest.pk

    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest_create')
    return HttpResponseRedirect(self.get_success_url())
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Nueva presolicitud'
    context["mprequest"] = 'menu-open'
    context["prequest"] = 'active'
    return context


class PreRequestUpdateView(LoginRequiredMixin,UpdateView):
  model = PreRequest
  form_class = PreRequestForm
  template_name = "prequest/edit.html"

  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud editada con éxito!')
    return reverse_lazy('request:prerequest')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    prqid=0
    try:
      with transaction.atomic():
        prequest = self.get_object()
        prqid=prequest.pk
        operation_str = str(request.POST['operation'])
        if 'house_id[]' in request.POST:
          house = request.POST.getlist('house_id[]')
          prequest.diagnosis = request.POST['diagnosis']
          prequest.bed = request.POST['bed']
          prequest.operation = datetime.fromisoformat(operation_str)
          prequest.comment = request.POST['comment']
          prequest.stock = True
          prequest.house.id = house[0]
          prequest.patient.id = request.POST['patient']
          prequest.user.id = self.request.user.pk
          prequest.save()
          # add detail pre request
          details=PreRequestDetail.objects.filter(pre_request__id=prequest.pk)
          details.delete()

          lots= request.POST.getlist('lot_id[]')
          amounts = request.POST.getlist('amount[]')
          i = 0
          for item in lots:
            get_lot = Lot.objects.get(pk=item)
            new_detail = PreRequestDetail.objects.create(
              amount = amounts[i],
              lot = get_lot,
              pre_request = prequest
            )
            new_detail.save()
            new_detail.lot.save()
            i += 1
        else:# add new pre request
          prequest.diagnosis = request.POST['diagnosis']
          prequest.bed = request.POST['bed']
          prequest.operation = prequest.operation = datetime.fromisoformat(operation_str)
          prequest.comment = request.POST['comment']
          prequest.patient.id = request.POST['patient']
          prequest.house.id = request.POST['house']
          prequest.user.id = self.request.user.pk
          prequest.save()
          
          # add detail pre request
          details=PreRequestDetail.objects.filter(pre_request__id=prequest.pk)
          details.delete()
          materials = request.POST.getlist('material_id[]')
          house = request.POST.getlist('house_id[]')
          amounts = request.POST.getlist('amount[]')
          i = 0
          for item in materials:
            get_material = Material.objects.get(pk=item)
            new_detail = PreRequestDetail.objects.create(
              amount = amounts[i],
              material = get_material,
              pre_request = prequest
            )
            new_detail.save()
            i += 1
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect("/prerequest/{}/edit/".format(prqid))
    return HttpResponseRedirect(self.get_success_url())
  
  def get_context_data(self, **kwargs):
    details=PreRequestDetail.objects.filter(pre_request__id=self.kwargs['pk'])
    total=0
    for item in details:
      total += item.amount
    context = super().get_context_data(**kwargs)
    context["title"] = 'Editar presolicitud'
    context["mprequest"] = 'menu-open'
    context["prequest"] = 'active'
    context["details"] = details
    context["totals"] = total
    return context

class PreRequestValidateView(LoginRequiredMixin,TemplateView):
  template_name = "prequest/validate.html"

  def get_context_data(self, **kwargs):
    prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
    detail = PreRequestDetail.objects.filter(pre_request__id=prequest.pk)
    option = ""
    more = False
    if prequest.status.pk == 1:
      option = "/prerequest/{}/store/".format(prequest.pk)
    elif prequest.status.pk == 2:
      option = "/prerequest/{}/shopping/".format(prequest.pk)
      more = True
    elif prequest.status.pk == 3:
      option = "/prerequest/{}/receive/".format(prequest.pk)
    context = super().get_context_data(**kwargs)
    context["title"] = 'Validar pre solicitud'
    context["prequest"] = prequest
    context["detail"] = detail
    context["option"] = option
    context["more"] = more
    return context

class PreRequestStoreView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud de materiales enviada a bodega con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.store()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())

class PreRequestShoppingView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud enviada a compras con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.number_siaf = self.request.GET['number_siaf']
      prequest.shopping()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())
  
class PreRequestReceiveView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud de materiales recibida en compras con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.receive()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())

class PreRequestTakenStoreView(LoginRequiredMixin,View):
  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud de materiales consumida con éxito!')
    return reverse_lazy('request:prerequest')
  
  def get(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.store()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())
  
class PreRequestAbortingView(LoginRequiredMixin,DeleteView):
  model = PreRequest
  template_name = "prequest/delete.html"

  def get_success_url(self):
    messages.success(self.request, '¡Pre-solicitud anulada con éxito!')
    return reverse_lazy('request:prerequest')
  
  def post(self, request, *args, **kwargs):
    try:
      prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
      prequest.abort_comment = self.request.POST['abort_comment']
      prequest.abort()
    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest')
    return HttpResponseRedirect(self.get_success_url())
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Anular pre solicitud'
    return context
  
class PreRequestPdfView(LoginRequiredMixin,View):
  def get(self, request, *args, **kwargs):
    template = get_template('prequest/report.html')
    prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
    print(prequest.stock)
    context = {
      'prequest': prequest,
      'detail': PreRequestDetail.objects.filter(pre_request__id=self.kwargs['pk']),
    }
    html = template.render(context)
    response = HttpResponse(content_type = 'application/pdf')
    # response['Content-Disposition'] = 'attachment; filename=reportedeventas.pdf'
    pisaStatus = pisa.CreatePDF(html, dest = response)
    if pisaStatus.err:
      return HttpResponse('Ocurrieron algunos errores <pre>'+ html +'</pre>')
    return response