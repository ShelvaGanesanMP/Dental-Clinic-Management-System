import random
import string
from django.db import models
from decimal import Decimal
from django.contrib.postgres.fields import JSONField 

# Create your models here.

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.date} ({self.start_time} - {self.end_time})"
    
class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Treatment(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    
class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    description = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    teeth = models.CharField(max_length=10)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Diagnosis for {self.patient.name}"

class PatientXRay(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='xrays')
    image = models.ImageField(upload_to='patient_xrays/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    item = models.CharField(max_length=200)
    frequency = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    form = models.CharField(max_length=50, choices=[
        ('gel', 'Gel'),
        ('pill', 'Pill'),
        ('tablet', 'Tablet'),
        ('lotion', 'Lotion')
    ])
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.item} ({self.patient.name})"
class Meta:
    unique_together = ('patient', 'item')

    
class LabOrder(models.Model):
    order_item = models.CharField(max_length=100)
    description = models.TextField()
    lab_name = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.order_item
    
    
class Payment(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.patient.name} - {self.paid_amount} on {self.date}"
   
class DentalChart(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    permanent_data = models.JSONField(default=list)
    deciduous_data = models.JSONField(default=list)



# doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)