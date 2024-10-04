from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Type(models.Model):
  name=models.CharField(max_length=45,verbose_name='Nombre')
  def __str__(self) -> str:
    return self.name
  
  class Meta:
    db_table = 'type'
    managed = True
    verbose_name = 'Tipo de estado'
    verbose_name_plural = 'Tipos de estado'

class Status(models.Model):
  name=models.CharField(max_length=45,verbose_name='Nombre')
  description=models.CharField(max_length=60,verbose_name='Descripción')
  color=models.CharField(max_length=25,blank=True,null=True,verbose_name='Color')
  type=models.ForeignKey(Type,on_delete=models.PROTECT,verbose_name='Tipo')

  def __str__(self) -> str:
    return self.name
  
  class Meta:
    db_table = 'status'
    managed = True
    verbose_name = 'Estado'
    verbose_name_plural = 'Estados'

class Patient(models.Model):
  membership=models.CharField(max_length=20,unique=True,verbose_name='Afiliación')
  first_name=models.CharField(max_length=100,verbose_name='Nombres')
  last_name=models.CharField(max_length=100,verbose_name='Apellidos')
  history = HistoricalRecords()

  def __str__(self) -> str:
    return "{} - {},{}".format(self.membership,self.last_name,self.first_name)
  
  class Meta:
    db_table = 'patient'
    managed = True
    verbose_name = 'Paciente'
    verbose_name_plural = 'Pacientes'

class Unit(models.Model):
  name = models.CharField(max_length=15,unique=True,verbose_name='Unidad')

  def __str__(self) -> str:
    return self.name
  
  class Meta:
    db_table = 'unit'
    managed = True
    verbose_name = 'Unidad'
    verbose_name_plural = 'Unidades'

class Material(models.Model):
  code=models.CharField(max_length=45,unique=True,verbose_name='Código')
  name=models.CharField(max_length=300,verbose_name='Nombre')
  description=models.CharField(max_length=1000,verbose_name='Descripción')
  stock=models.FloatField(default=0,verbose_name="Existencia")
  unit=models.ForeignKey(Unit,default=1,on_delete=models.PROTECT,verbose_name='Unidad')
  status=models.ForeignKey(Status,default=6,on_delete=models.PROTECT,verbose_name='Estado')
  history = HistoricalRecords()
  def __str__(self) -> str:
    return self.code
  
  class Meta:
    db_table = 'material'
    managed = True
    verbose_name = 'Material'
    verbose_name_plural = 'Materiales'

class MedicalHouse(models.Model):
  nit=models.CharField(max_length=10,unique=True,verbose_name='NIT')
  name=models.CharField(max_length=75,verbose_name='Nombre')

  def __str__(self) -> str:
    return "{} / {}".format(self.nit,self.name)
  
  class Meta:
    db_table = 'medical_house'
    managed = True
    verbose_name = 'Casa médica'
    verbose_name_plural = 'Casas médicas'

class Entry(models.Model):
  code=models.CharField(max_length=10,verbose_name='Código')
  date=models.DateField(default=timezone.now,verbose_name='Fecha')
  date_award=models.DateField(default=timezone.now,verbose_name='Fecha de adjudicación')
  nog=models.CharField(max_length=15,verbose_name='NOG')
  house=models.ForeignKey(MedicalHouse,on_delete=models.PROTECT,verbose_name='Casa médica')
  siaf=models.CharField(max_length=12,verbose_name='SIAF')
  ppr=models.CharField(max_length=15,verbose_name='PPR')
  comment=models.CharField(max_length=150,null=True,blank=True,verbose_name='Observaciones')
  total=models.FloatField(default=0,verbose_name='Total')
  user=models.ForeignKey(User,default=1,on_delete=models.PROTECT,verbose_name='Usuario')
  status=models.ForeignKey(Status,default=16,on_delete=models.PROTECT,verbose_name='Estado')
  history = HistoricalRecords()

  def __str__(self) -> str:
    return str(self.date)
  
  class Meta:
    db_table = 'entry'
    managed = True
    verbose_name = 'Ingreso'
    verbose_name_plural = 'Ingresos'

class EntryDetail(models.Model):
  ammount=models.CharField(max_length=4,verbose_name='Cantidad')
  price_purchase=models.FloatField(verbose_name='Precio compra')
  subtotal=models.FloatField(verbose_name='Subtotal')
  entry=models.ForeignKey(Entry,on_delete=models.PROTECT,verbose_name='Ingreso')
  material=models.ForeignKey(Material,on_delete=models.PROTECT,verbose_name='Material')

  def __str__(self) -> str:
    return str(self.material.name)
  
  class Meta:
    db_table = 'detail_entry'
    managed = True
    verbose_name = 'Detalle de ingreso'
    verbose_name_plural = 'Detalles de ingresos'

class Lot(models.Model):
  date=models.DateField(default=timezone.now,verbose_name='Fecha')
  stock=models.FloatField(default=0,verbose_name='Existencia')
  entry_detail=models.ForeignKey(EntryDetail,on_delete=models.PROTECT,verbose_name='Detalle ingreso')
  status=models.ForeignKey(Status,on_delete=models.PROTECT,default=19,verbose_name='Estado')

  def __str__(self):
    return str(self.entry_detail.material.name)

  class Meta:
    db_table = 'lot'
    managed = True
    verbose_name = 'Lote'
    verbose_name_plural = 'Lotes'

class PreRequest(models.Model):
  number=models.CharField(max_length=15,verbose_name='Número',unique=True)
  date=models.DateField(default=timezone.now,verbose_name='Fecha')
  diagnosis=models.CharField(max_length=150,verbose_name='Diagnóstico')
  procedure=models.CharField(max_length=150,verbose_name='Procedimiento quirúrgico')
  service=models.CharField(max_length=20,verbose_name='Servicio o sala')
  bed=models.CharField(max_length=10,verbose_name='No. de cama')
  operation=models.DateField(verbose_name='Fecha de operación')
  comment=models.CharField(max_length=100,blank=True,null=True,verbose_name='Observaciones')
  number_siaf=models.CharField(max_length=20,blank=True,null=True,verbose_name='SIAF')
  abort_comment=models.CharField(max_length=100,blank=True,null=True,verbose_name='Justificación')
  abort_user=models.CharField(max_length=25,blank=True,null=True,verbose_name='Usuario quien anula')
  decline_comment=models.CharField(max_length=100,blank=True,null=True,verbose_name='Justificación')
  stock=models.BooleanField(default=False,verbose_name='De stock')
  patient=models.ForeignKey(Patient,on_delete=models.PROTECT,verbose_name='Paciente')
  house=models.ForeignKey(MedicalHouse,on_delete=models.PROTECT,null=True,blank=True,verbose_name='Casa médica')
  user=models.ForeignKey(User,on_delete=models.PROTECT,verbose_name='Usuario')
  status=models.ForeignKey(Status,default=1,on_delete=models.PROTECT,verbose_name='Estado')
  history = HistoricalRecords()
  
  def decline(self):
    new_status = Status.objects.get(pk=1)
    self.status = new_status
    self.save()

  def store(self):
    new_status = Status.objects.get(pk=2)
    self.decline_comment = None
    self.status = new_status
    self.save()
  
  def shopping(self):
    new_status = Status.objects.get(pk=3)
    self.status = new_status
    self.save()
    
  def receive(self):
    new_status = Status.objects.get(pk=12)
    self.status = new_status
    self.save()

  def taking(self):
    new_status = Status.objects.get(pk=13)
    self.status = new_status
    self.save()
  
  def hcstore(self):
    new_status = Status.objects.get(pk=14)
    self.status = new_status
    self.save()
  
  def hcshoppig(self):
    new_status = Status.objects.get(pk=15)
    self.status = new_status
    self.save()
  
  def paid(self):
    new_status = Status.objects.get(pk=4)
    self.status = new_status
    self.save()
  
  def abort(self):
    new_status = Status.objects.get(pk=5)
    self.status = new_status
    self.save()

  def __str__(self) -> str:
    return self.number
  
  class Meta:
    db_table = 'pre_request'
    managed = True
    verbose_name = 'Pre solicitud'
    verbose_name_plural = 'Pre solicitudes'

class PreRequestDetail(models.Model):
  amount=models.IntegerField(verbose_name='Cantidad')
  material=models.ForeignKey(Material,null=True,blank=True,on_delete=models.PROTECT,verbose_name='Material')
  lot=models.ForeignKey(Lot,null=True,blank=True,on_delete=models.PROTECT,verbose_name='Lote')
  pre_request=models.ForeignKey(PreRequest,on_delete=models.PROTECT,verbose_name='Pre solicitud')

  def __str__(self) -> str:
    return self.material.code
  
  class Meta:
    db_table = 'pre_request_detail'
    managed = True
    verbose_name = 'Detalle de pre solicitud'
    verbose_name_plural = 'Detalles de pre solicitud'

class Uptake(models.Model):
  number=models.CharField(max_length=15,verbose_name='Número',unique=True)
  operating_room=models.CharField(max_length=3,verbose_name='No. de quirófano')
  date=models.DateField(default=timezone.now,verbose_name='Fecha')
  surgeon=models.CharField(max_length=45,verbose_name='Cirujano')
  instrumentalist=models.CharField(max_length=45,verbose_name='Instrumentista')
  circulating=models.CharField(max_length=45,verbose_name='Circulante')
  pre_request=models.ForeignKey(PreRequest,on_delete=models.PROTECT,verbose_name='Pre solicitud')
  house=models.ForeignKey(MedicalHouse,on_delete=models.PROTECT,verbose_name='Casa médica')
  user=models.ForeignKey(User,on_delete=models.PROTECT,verbose_name='Usuario')
  status=models.ForeignKey(Status,default=9,on_delete=models.PROTECT,verbose_name='Estado')
  history = HistoricalRecords()

  def __str__(self) -> str:
    return self.number
  
  class Meta:
    db_table = 'uptake'
    managed = True
    verbose_name = 'Hoja de consumo'
    verbose_name_plural = 'Hojas de consumo'

class UptakeDetail(models.Model):
  amount=models.IntegerField(verbose_name='Cantidad')
  material=models.ForeignKey(Material,on_delete=models.PROTECT,verbose_name='Material')
  uptake=models.ForeignKey(Uptake,on_delete=models.PROTECT,verbose_name='Hoja de consumo')

  def __str__(self) -> str:
    return self.material.code
  
  class Meta:
    db_table = 'uptake_detail'
    managed = True
    verbose_name = 'Detalle de hoja deconsumo'
    verbose_name_plural = 'Detalles de hoja de consumo'