from django.urls import path
from . import views

urlpatterns = [
    path('patient_register/', views.register_patient, name = 'patient_register'),
    path('labPayment/', views.lab_payment_list, name = 'lab_payment_list'),
    path('reception/lab-payment/<int:visit_id>/',views.lab_payment_detail,name='lab_payment_detail'),
    path('reception/lab-payment/<int:visit_id>/confirm/',views.confirm_lab_payment,name='confirm_lab_payment'),
    path('reception/Del_payment/<int:visit_id>/confirm/',views.delete_lab_payment,name='delete_lab_payment'),
    path('nurse_onvisit/', views.nurse_visits, name = 'nurseOnVisit'),
    path('nurse_vital/<int:visit_id>/', views.vital_signs, name = 'nurseVital'),
    path('doctor_Onvisit/', views.doctorVisits, name = 'doctorVisits'),
    path('doctor/treatPatient/<int:visit_id>/', views.treat_patient, name = 'treatPatient'),
    path('doctor/clinicalNote/<int:visit_id>/', views.clinicalNote  , name = 'clinicalNote'),
    path('doctor/labrequest/<int:visit_id>/', views.labRequest, name = 'labRequest'),
    path('doctor/lab-request/<int:visit_id>/add/<int:test_id>/',views.add_lab_test,name='add_lab_test'),
    path('doctor/lab-request/<int:visit_id>/delete/<int:test_id>/',views.delete_lab_test,name='delete_lab_test'),
    path('doctor/lab-request/<int:visit_id>/send/',views.send_lab_request,name='send_lab_request'),
    path('lab/', views.labrequestview, name = 'labrequestview'),
    path('lab_requests/<int:visit_id>/',views.labrequestdetail,name='labrequestdetail'),
    path('labresult/<int:visit_id>/', views.labResult, name = 'labresults'),
    path('doctor/prescription/<int:visit_id>/', views.prescription, name = 'prescription'),
]