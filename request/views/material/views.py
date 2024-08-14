from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from request.models import *
from request.forms import *
from django.urls import reverse_lazy

class MaterialListView(LoginRequiredMixin,ListView):
  model = Material
  template_name = "material/index.html"

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Materiales'
    context["minventory"] = 'menu-open'
    context["material"] = 'active'
    return context
  
class MaterialCreateView(CreateView):
  model = Material
  form_class = MaterialForm
  template_name = "material/create.html"

  def get_success_url(self):
    messages.success(self.request, '¡Material agregado con éxito!')
    return reverse_lazy('request:material')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Nuevo material'
    return context

class MaterialSelectView(LoginRequiredMixin,View):
  def get(self, request, *args, **kwargs):
    data = list()
    action = request.GET.get('action')
    if action == 'search':
      term=request.GET.get('q')
      materials=Material.objects.filter(Q(code__icontains=term) | Q(name__icontains=term) | Q(description__icontains=term))
      lots=Lot.objects.filter(Q(entry_detail__material__code__icontains=term) | Q(entry_detail__material__name__icontains=term) | 
        Q(entry_detail__material__description__icontains=term)).filter(stock__gt=0)
      for item in materials:
        lot = next(filter(lambda material:material.entry_detail.material.id == int(item.pk), lots), None)
        print(lot)
        if lot is None:
          datos={
            'type':'list',
            'id':item.id,
            'code':item.code,
            'name':item.name,
            'description':item.description,
          }
          data.append(datos)
        else:
          lotsearch = Lot.objects.filter(entry_detail__material__id=item.pk)
          for lot in lotsearch:
            datos={
              'type':'stock',
              'id':lot.id,
              'code':lot.entry_detail.material.code,
              'name':lot.entry_detail.material.name,
              'description':lot.entry_detail.material.description,
              'stock':lot.stock,
              'house':lot.entry_detail.entry.house.id,
              'mhouse': "{} - {}".format(lot.entry_detail.entry.house.nit,lot.entry_detail.entry.house.name)
            }  
            data.append(datos)
    elif action == 'select':
      lot_id = 0
      type_model = request.GET.get('type')
      if type_model == 'stock':
        lot = Lot.objects.get(pk=request.GET.get('id'))
        data.append({
          'type':'stock',
          'id':lot.id,
          'code':lot.entry_detail.material.code,
          'name':lot.entry_detail.material.name,
          'description':lot.entry_detail.material.description,
          'stock':lot.stock,
          'house':lot.entry_detail.entry.house.id,
          'mhouse': "{} - {}".format(lot.entry_detail.entry.house.nit,lot.entry_detail.entry.house.name)
        })
      else:
        material = Material.objects.get(pk = request.GET.get('id'))
        data.append({
          'id' : material.id,
          'code' : material.code,
          'name':material.name,
          'description' : material.description,
        })
    elif action == 'search_entry':
      term=request.GET.get('q')
      materials=Material.objects.filter(Q(code__icontains=term) | Q(name__icontains=term) | Q(description__icontains=term))
      for item in materials:
        datos={
          'type':'list',
          'id':item.id,
          'code':item.code,
          'name':item.name,
          'description':item.description,
        }
        data.append(datos)
    return JsonResponse(data,safe=False)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Material'
    return context

class MaterialUpdateView(LoginRequiredMixin,UpdateView):
  model = Material
  form_class = MaterialForm
  template_name = "material/edit.html"

  def get_success_url(self):
    messages.success(self.request, '¡Material editado con éxito!')
    return reverse_lazy('request:material')
  
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title"] = 'Editar material'
    return context