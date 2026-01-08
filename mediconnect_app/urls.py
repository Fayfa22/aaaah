from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('signup/', views.signup_role_selection, name='signup_role'),
    path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Medical Form
    path('complete-medical-form/<int:user_id>/', views.complete_medical_form, name='complete_medical_form'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # Profiles
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    
    # Appointments
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('doctor/appointments/', views.doctor_appointments_list, name='doctor_appointments_list'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    
    # Medical Records
    path('medical-records/', views.medical_records_list, name='medical_records_list'),
    path('medical-records/delete/<int:record_id>/', views.delete_medical_record, name='delete_medical_record'),
    
    # Checkups
    path('doctor/patients/', views.doctor_patient_list, name='doctor_patients_list'),
    path('doctor/checkup/<int:patient_id>/', views.record_checkup, name='record_checkup'),
    path('checkup/<int:checkup_id>/', views.checkup_detail, name='checkup_detail'),
    
    # Prescriptions
    path('prescription/add/<int:checkup_id>/', views.add_prescription, name='add_prescription'),
    path('prescriptions/', views.prescriptions_list, name='prescriptions_list'),
    
    # Medications
    path('medications/', views.medications_list, name='medications_list'),
    path('medications/edit/<int:medication_id>/', views.edit_medication, name='edit_medication'),
    
    # Chatbot
    path('chatbot/', views.chatbot, name='chatbot'),
    
    # API endpoints
    path('api/doctor/<int:doctor_id>/availability/', views.get_doctor_availability, name='doctor_availability'),
]
