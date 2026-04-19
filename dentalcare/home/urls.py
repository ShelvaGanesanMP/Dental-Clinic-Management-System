from django.urls import path
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", lambda request: redirect("signin/")),
    path("signin/", views.signin, name="signin"),
    path("receptionist/", views.receptionist_dashboard, name="reception_dashboard"),
    path("doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path('view-doctors/', views.view_doctors, name='view_doctors'),
    path('add-update-schedule/', views.add_update_schedule, name='add_update_schedule'),
    path('view_schedule/', views.view_schedule, name='view_schedule'),
    path('update-doctor-inline/', views.update_doctor_inline, name='update_doctor_inline'),
    path('add-doctor-inline/', views.add_doctor_inline, name='add_doctor_inline'),
    path('update_schedule_inline/', views.update_schedule_inline, name='update_schedule_inline'),
    path('delete_schedule/', views.delete_schedule, name='delete_schedule'),
    path('patient_dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('patients/update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('treatments/', views.treatment_view, name='treatment'),
    path('update-treatment/<int:treatment_id>/', views.update_treatment, name='update-treatment'),
    path('delete-treatment/<int:treatment_id>/', views.delete_treatment, name='delete-treatment'),
    path('appointments/<int:patient_id>/', views.patient_appointments, name='patient_appointments'),
    path('all-appointments/', views.all_appointments, name='all_appointments'),  
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),   
    path('patient/<int:patient_id>/diagnosis/', views.patient_diagnosis, name='patient_diagnosis'),
    path('update_diagnosis/<int:id>/', views.update_diagnosis, name='update_diagnosis'),
    path('delete_diagnosis/<int:id>/', views.delete_diagnosis, name='delete_diagnosis'),
    path('patient/<int:patient_id>/xrays/', views.xray_gallery, name='xray_gallery'),
    path('delete_xray/<int:xray_id>/', views.delete_xray, name='delete_xray'),
    path('prescription/<int:patient_id>/', views.patient_prescription, name='patient_prescription'),
    path('prescription/delete/<int:id>/', views.delete_prescription, name='delete_prescription'),
    path('lab/', views.lab_orders, name='lab_orders'),
    path('lab/delete/<int:id>/', views.delete_lab_order, name='delete_lab_order'),
    path('lab/edit/<int:id>/', views.edit_lab_order, name='edit_lab_order'),
    path('payment_summary/', views.payment_summary, name='payment_summary'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('dental-chart/<int:patient_id>/', views.dental_chart_view, name='dental_chart'),
    path('save-dental-chart/<int:patient_id>/', views.save_dental_chart, name='save_dental_chart'),
    path('logout/', views.logout_view, name='logout'),
    path('get_treatment_amount/', views.get_treatment_amount, name='get_treatment_amount'),
    path('lab/search_patient/', views.search_patient, name='search_patient'),
    



    
    
   

    

    
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
