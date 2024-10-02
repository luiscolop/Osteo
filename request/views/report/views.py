from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.db.models import Q
from request.models import *
from django.conf import settings

from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

class PreRequestPdfView(LoginRequiredMixin,View):
  template_name = 'prequest/report.html'
  
  def count_words_chars(self, pharse, limit):
    words = pharse.split()
    first_line = ''
    for word in words:
      temp = first_line
      temp += word + ' '
      if temp.__len__() > limit:
        return first_line
      else:
        first_line += word + ' '
    return first_line
  def get(self, request, *args, **kwargs):
    prequest = PreRequest.objects.get(pk=self.kwargs['pk'])
    details = PreRequestDetail.objects.filter(pre_request__id=self.kwargs['pk'])
    template = get_template(self.template_name)
    num = int(13) - int(details.count())
    range_num = range(num)
    diagnosis = prequest.diagnosis
    diagnosis_first_part = self.count_words_chars(diagnosis, 85)
    diagnosis_second_part = diagnosis[diagnosis_first_part.__len__():]
    procedure = prequest.procedure
    procedure_first_part = self.count_words_chars(procedure, 70)
    procedure_second_part = procedure[procedure_first_part.__len__():]
    html_string = template.render({
      'foo': 'bar',
      'imagen': settings.LOGO_REPORT,
      'prequest':prequest,
      'fpdiagnosis':diagnosis_first_part,
      'spdiagnosis':diagnosis_second_part,
      'fpprocedure':procedure_first_part,
      'spprocedure':procedure_second_part,
      'detail':details,
      'blank': range_num
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="presolicitud"'+prequest.number+'".pdf"'
    return response
  
class UptakePdfView(LoginRequiredMixin,View):
  template_name = 'uptake/report.html'
  
  def get(self, request, *args, **kwargs):
    # Render the HTML template
    uptake = Uptake.objects.get(pk=self.kwargs['pk'])
    prequest = PreRequest.objects.get(pk=uptake.pre_request.pk)
    details = UptakeDetail.objects.filter(uptake__id=self.kwargs['pk'])
    num = int(4) - int(details.count())
    range_num = range(num)
    template = get_template(self.template_name)
    html_string = template.render({
      'foo': 'bar',
      'imagen': settings.LOGO_REPORT,
      'prequest':prequest,
      'uptake':uptake,
      'detail':details,
      'blank': range_num,
    })  # Replace with your data

    # Create a PDF from the HTML string
    pdf_file = HTML(string=html_string).write_pdf()

    # Return the PDF as a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="hoja_de_consumo.pdf"'
    return response