from django.urls import path
from . import views

urlpatterns = [
    path('patient_register/', views.register_patient, name = 'patient_register'),
]