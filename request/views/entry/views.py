from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.db import transaction
from request.forms import *
from request.models import *
from django.urls import reverse_lazy
from datetime import datetime

class EntryListView(LoginRequiredMixin,ListView):
  model = Entry
  template_name = "entry/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_queryset(self):
    return Entry.objects.all().order_by('-pk')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Ingresos'
    context["minventory"] = 'menu-open'
    context["entry"] = 'active'
    return context
  
class EntryCreateView(CreateView):
  model = Entry
  form_class = EntryForm
  template_name = "entry/create.html"

  def get_success_url(self):
    messages.success(self.request, '¡Ingreso creado con éxito!')
    return reverse_lazy('request:entry')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def generate_code(self):
    ident = 'IN'
    if Entry.objects.count() > 0:
      next_code = Entry.objects.latest('id').id + 1
      next_code = str(next_code)
      next_code.zfill(3)
    else:
      next_code = '1'
      next_code.zfill(3)
    return "{}-{}".format(ident,next_code)
  
  def post(self, request, *args, **kwargs):
    try:
      with transaction.atomic():
        get_house = MedicalHouse.objects.get(pk=request.POST['house'])
        # add new pre request
        new_entry = Entry.objects.create(
          code = self.generate_code(),
          house = get_house,
          date_award = request.POST['date_award'],
          nog = request.POST['nog'],
          siaf = request.POST['siaf'],
          ppr = request.POST['ppr'],
          comment = request.POST['comment'],
          user = self.request.user,
        )
        new_entry.save()
        
        get_material = request.POST.getlist('material_id[]')
        get_price_purchase = request.POST.getlist('price_purchase[]')
        get_ammount = request.POST.getlist('ammount[]')
        get_subtotal = request.POST.getlist('subtotal[]')
        
        total = 0
        it = 0
        for ref in get_material:
          product_price_purchase = get_price_purchase[it]
          temp_subtotal = float(product_price_purchase) * float(get_ammount[it])
          total += temp_subtotal
          it += 1
        new_entry.total=total
        new_entry.save()

        i = 0
        for item in get_material:
          material = Material.objects.get(pk=item)
          get_status_material_active = Status.objects.get(pk=6)
          new_detail = EntryDetail.objects.create(
            entry = new_entry,
            ammount = get_ammount[i],
            price_purchase = format(float(get_price_purchase[i]),'.2f'),
            subtotal = format(float(get_subtotal[i]),'.2f'),
            material = material
          )
          new_detail.save()
          new_detail.material.stock += float(new_detail.ammount)
          new_detail.material.status = get_status_material_active
          new_detail.material.save()
          new_lot = Lot.objects.create(
            stock = get_ammount[i],
            entry_detail = new_detail
          )
          new_lot.save()
          i += 1

    except Exception as e:
      messages.error(self.request,str(e))
      return HttpResponseRedirect('request:prerequest_create')
    return HttpResponseRedirect(self.get_success_url())
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Nuevo ingreso'
    context["minventory"] = 'menu-open'
    context["entry"] = 'active'
    return context