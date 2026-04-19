from django import forms
from .models import Doctor,DoctorSchedule
from .models import Patient
from .models import Treatment
from django import forms
from .models import Diagnosis
from .models import PatientXRay
from .models import Prescription
from .models import LabOrder



class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'password', 'qualification', 'phone', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'whatsapp', 'email', 'address']
        widgets = {
            'gender': forms.Select(choices=Patient.GENDER_CHOICES),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'id': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'phone'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'whatsapp'
            }),
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter treatment name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
        }


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['diagnosis', 'description', 'teeth', 'doctor', 'treatment', 'amount', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super(DiagnosisForm, self).__init__(*args, **kwargs)
        self.fields['treatment'].queryset = Treatment.objects.all()
        self.fields['doctor'].queryset = Doctor.objects.all()


class XRayUploadForm(forms.ModelForm):
    class Meta:
        model = PatientXRay
        fields = ['image']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['item', 'frequency', 'notes', 'form']


class LabOrderForm(forms.ModelForm):
    class Meta:
        model = LabOrder
        fields = ['order_item', 'description', 'lab_name', 'patient_name', 'status']








