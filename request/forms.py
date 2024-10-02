from django.forms import *
from request.models import *

class PreRequestForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
  class Meta:
    model=PreRequest
    fields = '__all__'
    exclude= ('number','date','number_siaf','abort_comment','abort_user','decline_comment','stock','user','status',)
    widgets={
      'diagnosis': TextInput(
        attrs={
          'id':'diagnosis',
          'class':'form-control',
          'placeholder':'Ingrese el diagnóstico'
        }
      ),
      'procedure' : TextInput(
        attrs={
          'id':'procedure',
          'class':'form-control',
          'value':'Osteosíntesis',
          'placeholder':'Ingrese el procedimiento'
        }
      ),
      'service' : TextInput(
        attrs={
          'id':'service',
          'class':'form-control',
          'placeholder':'Ingrese el servicio'
        }
      ),
      'bed': TextInput(
        attrs={
          'id':'bed',
          'class':'form-control',
          'placeholder':'Ingrese el número de cama'
        }
      ),
      'operation': TextInput(
        attrs={
          'id':'operation',
          'class':'form-control',
          'type':'date'
        }
      ),
      'comment': TextInput(
        attrs={
          'id':'comment',
          'class':'form-control',
          'placeholder':'Agregue las observaciones correspondientes...'
        }
      ),
      'patient': Select(
        attrs={
          'id':'patient',
          'class':'form-control select2',
          'style':'width:100%'
        }
      ),
      'house' : Select(
        attrs={
          'id':'house',
          'class':'form-control select2',
          'style':'width:100%',
        }
      ),
    }

class MaterialForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
  class Meta:
    model=Material
    fields = '__all__'
    exclude= ('status','stock')
    widgets={
      'code': TextInput(
        attrs={
          'id':'code',
          'class':'form-control',
          'placeholder':'Ingrese el código del material'
        }
      ),
      'name': TextInput(
        attrs={
          'id':'name',
          'class':'form-control',
          'placeholder':'Ingrese el nombre del material'
        }
      ),
      'description' : TextInput(
        attrs={
          'id':'description',
          'class':'form-control',
          'placeholder':'Ingrese la descripción del material'
        }
      ),
      'unit' : Select(
        attrs={
          'id':'unit',
          'class':'form-control selectm2',
          'initial':'1',
          'style':'width:100%'
        }
      ),
    }


class PatientForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
  class Meta:
    model=Patient
    fields = '__all__'
    widgets={
      'membership': TextInput(
        attrs={
          'id':'membership',
          'class':'form-control',
          'placeholder':'Ingrese la afiliación del paciente'
        }
      ),
      'first_name' : TextInput(
        attrs={
          'id':'first_name',
          'class':'form-control',
          'placeholder':'Ingrese nombres del paciente'
        }
      ),
      'last_name' : TextInput(
        attrs={
          'id':'last_name',
          'class':'form-control',
          'placeholder':'Ingrese apellidos del paciente'
        }
      ),
    }

class MedicalHouseForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
  class Meta:
    model=MedicalHouse
    fields = '__all__'
    widgets={
      'nit': TextInput(
        attrs={
          'id':'nit',
          'class':'form-control',
          'placeholder':'Ingrese el nit de la casa médica'
        }
      ),
      'name' : TextInput(
        attrs={
          'id':'first_name',
          'class':'form-control',
          'placeholder':'Ingrese nombres de la casa médica'
        }
      ),
    }

class UptakeForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
  class Meta:
    model=Uptake
    fields = '__all__'
    exclude= ('number','date','pre_request','user','status',)
    widgets={
      'operating_room': TextInput(
        attrs={
          'id':'operating_room',
          'class':'form-control',
          'placeholder':'Ingrese el diagnóstico'
        }
      ),
      'surgeon' : TextInput(
        attrs={
          'id':'surgeon',
          'class':'form-control',
          'placeholder':'Ingrese el procedimiento'
        }
      ),
      'instrumentalist' : TextInput(
        attrs={
          'id':'instrumentalist',
          'class':'form-control',
          'placeholder':'Ingrese el servicio'
        }
      ),
      'circulating': TextInput(
        attrs={
          'id':'circulating',
          'class':'form-control',
          'placeholder':'Ingrese el número de cama'
        }
      ),
      'house' : Select(
        attrs={
          'id':'house',
          'class':'form-control select2',
          'readonly':True,
          'style':'width:100%',
        }
      )
    }

class EntryForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
  class Meta:
    model=Entry
    fields = '__all__'
    exclude= ('code','date','total','user','status',)
    widgets={
      'house' : Select(
        attrs={
          'id':'house',
          'class':'form-control select2',
          'style':'width:100%',
        }
      ),
      'date_award': TextInput(
        attrs={
          'id':'date_award',
          'type':'date',
          'class':'form-control',
        }
      ),
      'nog' : TextInput(
        attrs={
          'id':'nog',
          'class':'form-control',
          'placeholder':'Ingrese No. NOG'
        }
      ),  
      'siaf' : TextInput(
        attrs={
          'id':'siaf',
          'class':'form-control',
          'placeholder':'Ingrese No. SIAF'
        }
      ),
      'ppr': TextInput(
        attrs={
          'id':'ppr',
          'class':'form-control',
          'placeholder':'Ingrese el No. PPR'
        }
      ),
      'comment': TextInput(
        attrs={
          'id':'comment',
          'class':'form-control',
          'placeholder':'Campo para observaciones'
        }
      ),
    }