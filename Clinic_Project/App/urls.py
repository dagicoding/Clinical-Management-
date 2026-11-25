from django.urls import path
from . import views

urlpatterns = [
    path('patient_register/', views.register_patient, name = 'patient_register'),
    path('nurse_onvisit/', views.nurse_visits, name = 'nurseOnVisit'),
    path('nurse_vital/<int:visit_id>/', views.vital_signs, name = 'nurseVital'),
    path('doctor_Onvisit/', views.doctorVisits, name = 'doctorVisits'),
    path('doctor/treatPatient/<int:visit_id>/', views.treat_patient, name = 'treatPatient'),
    path('doctor/clinicalNote/<int:visit_id>/', views.clinicalNote  , name = 'clinicalNote'),

]