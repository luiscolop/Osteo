from django.urls import path
from django.shortcuts import redirect
from request.views.patient.views import PatientListView, PatientCreateView, PatientUpdateView
from request.views.mhouse.views import MedicalHouseListView, MedicalHouseCreateView, MedicalHouseUpdateView
from request.views.material.views import MaterialSelectView, MaterialListView, MaterialCreateView, MaterialUpdateView
from request.views.prequest.views import *
from request.views.uptake.views import *
from request.views.entry.views import EntryListView, EntryCreateView

app_name= 'request'

urlpatterns=[
    path('', lambda req: redirect('/auth/dashboard/'),name='dashboard'),
    path('patient/',PatientListView.as_view(),name='patient'),
    path('patient/create/',PatientCreateView.as_view(),name='patient_create'),
    path('patient/<int:pk>/edit/',PatientUpdateView.as_view(),name='patient_edit'),
    path('mhouse/',MedicalHouseListView.as_view(),name='mhouse'),
    path('mhouse/create/',MedicalHouseCreateView.as_view(),name='mhouse_create'),
    path('mhouse/<int:pk>/edit/',MedicalHouseUpdateView.as_view(),name='mhouse_edit'),
    path('prerequest/',PreRequestListView.as_view(),name='prerequest'),
    path('prerequest/create/',PreRequestCreateView.as_view(),name='prerequest_create'),
    path('prerequest/<int:pk>/format/',PreRequestPdfView.as_view(),name="prerequest_format"),
    path('prerequest/<int:pk>/validate/',PreRequestValidateView.as_view(),name='prerequest_validate'),
    path('prerequest/<int:pk>/store/',PreRequestStoreView.as_view(),name="prerequest_store"),
    path('prerequest/<int:pk>/shopping/',PreRequestShoppingView.as_view(),name="prerequest_shopping"),
    path('prerequest/<int:pk>/receive/',PreRequestReceiveView.as_view(),name="prerequest_receive"),
    path('prerequest/<int:pk>/delete/',PreRequestAbortingView.as_view(),name='prerequest_delete'),
    path('uptake/',UptakeListView.as_view(),name='uptake'),
    path('uptake/<int:pk>/',UptakeCreateView.as_view(),name='uptake_create'),
    path('uptake/<int:pk>/format/',UptakePdfView.as_view(),name="uptake_format"),
    path('uptake/<int:pk>/validate/',UptakeValidateView.as_view(),name="uptake_validate"),
    path('uptake/<int:pk>/store/',UptakeStoreView.as_view(),name="uptake_store"),
    path('uptake/<int:pk>/shopping/',UptakeShoppingView.as_view(),name="uptake_shopping"),
    path('uptake/<int:pk>/paid/',UptakePaidView.as_view(),name="uptake_paid"),
    path('entry/',EntryListView.as_view(),name='entry'),
    path('entry/create/',EntryCreateView.as_view(),name='entry_create'),
    path('material/',MaterialListView.as_view(),name='material'),
    path('material/create/',MaterialCreateView.as_view(),name='material_create'),
    path('material/<int:pk>/edit/',MaterialUpdateView.as_view(),name='material_edit'),
    path('material/select/',MaterialSelectView.as_view(),name='material_select')
]