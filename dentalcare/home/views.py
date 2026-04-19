from .decorators import role_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home.models import Doctor
from .forms import DoctorForm,DoctorSchedule
from .forms import DoctorScheduleForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .models import Patient
from .forms import PatientForm
import json
from .models import Treatment
from .forms import TreatmentForm
from .models import Appointment
from datetime import datetime
from django.contrib import messages
from django.db.models import Min, Max
from datetime import date
from .models import Patient
from .models import Diagnosis, Treatment
from .forms import DiagnosisForm
from .models import PatientXRay
from .forms import XRayUploadForm
from .models import Patient, Prescription
from .forms import PrescriptionForm
from django.utils import timezone
from .models import LabOrder
from .forms import LabOrderForm
from .models import Diagnosis
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Diagnosis, Payment
from datetime import datetime
from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Appointment, Patient, Payment, LabOrder, Diagnosis
from datetime import datetime
from django.db.models.functions import TruncMonth, TruncYear
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, DentalChart
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from decimal import Decimal


def dental_chart_view(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    chart, created = DentalChart.objects.get_or_create(patient=patient)
    
    context = {
        "patient": patient,
        "permanent_data": json.dumps(chart.permanent_data or [{"number": i + 1, "status": "normal"} for i in range(32)]),
        "deciduous_data": json.dumps(chart.deciduous_data or [{"number": i + 1, "status": "normal"} for i in range(20)]),
    }
    return render(request, 'dentalchart.html', context)

def save_dental_chart(request, patient_id):
    if request.method == 'POST':
        chart, _ = DentalChart.objects.get_or_create(patient_id=patient_id)
        chart.permanent_data = json.loads(request.POST.get('permanent_data', '[]'))
        chart.deciduous_data = json.loads(request.POST.get('deciduous_data', '[]'))
        chart.save()
        return redirect('dental_chart', patient_id=patient_id)


def analytics_dashboard(request):
    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')

    appointments = Appointment.objects.all()
    payments = Payment.objects.all()
    diagnoses = Diagnosis.objects.all()
    patients = Patient.objects.all()

    if filter_type == 'date':
        filter_date = datetime.strptime(filter_value, '%Y-%m-%d').date()
        appointments = appointments.filter(date=filter_date)
        payments = payments.filter(date=filter_date)
        diagnoses = diagnoses.filter(created_at__date=filter_date)
        patients = patients.filter(created_at__date=filter_date)

    elif filter_type == 'month':
        month = int(filter_value.split('-')[1])
        year = int(filter_value.split('-')[0])
        appointments = appointments.filter(date__month=month, date__year=year)
        payments = payments.filter(date__month=month, date__year=year)
        diagnoses = diagnoses.filter(created_at__month=month, created_at__year=year)
        patients = patients.filter(created_at__month=month, created_at__year=year)

    elif filter_type == 'year':
        year = int(filter_value)
        appointments = appointments.filter(date__year=year)
        payments = payments.filter(date__year=year)
        diagnoses = diagnoses.filter(created_at__year=year)
        patients = patients.filter(created_at__year=year)

    appointment_count = appointments.count()
    patient_count = patients.count()
    total_amount = diagnoses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = payments.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_pending = total_amount - total_paid
    
    context = {
        'appointment_count': appointment_count,
        'patient_count': patient_count,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'filter_type': filter_type or '',
        'filter_value': filter_value or ''
    }
    return render(request, 'analysis.html', context)

@role_required(allowed_roles=['admin'])
def payment_summary(request):
    selected_date = request.GET.get('filter_date')
    diagnoses = Diagnosis.objects.all().select_related('patient', 'treatment')

    if selected_date:
        diagnoses = diagnoses.filter(created_at__date=selected_date)

    payments = []
    total_amount = total_paid = total_pending = 0

    for d in diagnoses:
        paid = Payment.objects.filter(diagnosis=d).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        pending = d.amount - paid if d.amount else 0

        payments.append({
            'diagnosis': d,
            'date': d.created_at.date(),
            'patient': d.patient,
            'treatment': d.treatment,
            'amount': d.amount,
            'paid': paid,
            'pending': pending
        })

        total_amount += d.amount or 0
        total_paid += paid
        total_pending += pending

    context = {
        'payments': payments,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'selected_date': selected_date or ''
    }
    return render(request, 'payment_summary.html', context)

def add_payment(request):
    if request.method == 'POST':
        diagnosis_id = request.POST.get('diagnosis_id')
        paid_amount = request.POST.get('paid_amount')

        diagnosis = Diagnosis.objects.get(id=diagnosis_id)
        Payment.objects.create(
            diagnosis=diagnosis,
            patient=diagnosis.patient,
            treatment=diagnosis.treatment,
            paid_amount=paid_amount
        )

    return redirect('payment_summary')

@role_required(allowed_roles=['doctor', 'admin'])
def lab_orders(request):
    if request.method == "POST":
        order_item = request.POST.get('order_item')
        description = request.POST.get('description')
        lab_name = request.POST.get('lab_name')
        patient_name = request.POST.get('patient_name')
        status = request.POST.get('status')

        LabOrder.objects.create(
            order_item=order_item,
            description=description,
            lab_name=lab_name,
            patient_name=patient_name,
            status=status
        )
        return redirect('lab_orders')

    patients = Patient.objects.all()
    orders = LabOrder.objects.all().order_by('-created_at')
    return render(request, 'lab.html', {'orders': orders, 'patients': patients})


@csrf_exempt
def delete_lab_order(request, id):
    if request.method == 'POST':
        order = LabOrder.objects.get(id=id)
        order.delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def edit_lab_order(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = LabOrder.objects.get(id=id)
        order.order_item = data['order_item']
        order.description = data['description']
        order.lab_name = data['lab_name']
        order.patient_name = data['patient_name']
        order.status = data['status']
        order.save()
        return JsonResponse({'status': 'success'})


def search_patient(request):
    query = request.GET.get('q', '')
    matches = []
    if query:
        matches = Patient.objects.filter(name__icontains=query).values_list('name', flat=True)[:10]
    return JsonResponse(list(matches), safe=False)


def patient_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            item_name = form.cleaned_data['item'].strip().lower()

            # Check for duplicate medicine name for the same patient
            if Prescription.objects.filter(patient=patient, item__iexact=item_name).exists():
                messages.error(request, f"The medicine '{form.cleaned_data['item']}' is already prescribed to this patient.")
            else:
                prescription = form.save(commit=False)
                prescription.patient = patient
                prescription.save()
                messages.success(request, f"Medicine '{prescription.item}' added successfully.")
                return redirect('patient_prescription', patient_id=patient.id)
    else:
        form = PrescriptionForm()

    return render(request, 'patient_prescription.html', {
        'patient': patient,
        'prescriptions': prescriptions,
        'form': form,
        'today': timezone.now().date()
    })

def delete_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)
    patient_id = prescription.patient.id
    prescription.delete()
    return redirect('patient_prescription', patient_id=patient_id)


def xray_gallery(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    xrays = patient.xrays.all()

    if request.method == 'POST':
        form = XRayUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xray = form.save(commit=False)
            xray.patient = patient
            xray.save()
            return redirect('xray_gallery', patient_id=patient.id)
    else:
        form = XRayUploadForm()

    return render(request, 'xray_gallery.html', {'patient': patient, 'xrays': xrays, 'form': form})

def delete_xray(request, xray_id):
    xray = get_object_or_404(PatientXRay, id=xray_id)
    patient_id = xray.patient.id
    xray.delete()
    return redirect('xray_gallery', patient_id=patient_id)


def patient_diagnosis(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    diagnoses = Diagnosis.objects.filter(patient=patient)

    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.patient = patient
            if not diagnosis.amount and diagnosis.treatment:
                diagnosis.amount = diagnosis.treatment.price
            diagnosis.save()
            return redirect('patient_diagnosis', patient_id=patient.id)
    else:
        form = DiagnosisForm()

    return render(request, 'patient_diagnosis.html', {
        'patient': patient,
        'diagnoses': diagnoses,
        'form': form,
    })


def get_treatment_amount(request):
    treatment_id = request.GET.get('treatment_id')
    amount = 0
    if treatment_id:
        try:
            treatment = Treatment.objects.get(id=treatment_id)
            amount = treatment.price
        except Treatment.DoesNotExist:
            pass
    return JsonResponse({'amount': float(amount)})

def update_diagnosis(request, id):
    if request.method == 'POST':
        diagnosis = Diagnosis.objects.get(id=id)
        data = json.loads(request.body)
        diagnosis.description = data['description']
        diagnosis.teeth = data['teeth']
        diagnosis.status = data['status']
        diagnosis.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def delete_diagnosis(request, id):
    if request.method == 'POST':
        diagnosis = Diagnosis.objects.get(id=id)
        diagnosis.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def signin(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")

        if name.lower() == "admin" and password == "admin":
            request.session['user_role'] = 'admin'
            return redirect("analytics_dashboard") 
        
        doctor = Doctor.objects.filter(name=name, password=password).first()
        if doctor:
            request.session['user_role'] = 'doctor'
            return redirect("all_appointments")  
        messages.error(request, "Invalid Credentials. Please try again.")
    return render(request, "signin.html")

def receptionist_dashboard(request):
    return render(request, "reception.html")

def doctor_dashboard(request):
    return render(request, "patients.html")

@role_required(['admin'])
def view_doctors(request):
    doctors = Doctor.objects.all()  
    return render(request, 'view_doctor.html', {'doctors': doctors})

def add_update_schedule(request):
    return render(request, 'add_update_schedule.html')

class ScheduleSearchForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

@csrf_exempt
def update_doctor_inline(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            doctor = Doctor.objects.get(pk=request.POST['doctor_id'])
            doctor.name = request.POST['name']
            doctor.password = request.POST['password']
            doctor.qualification = request.POST['qualification']
            doctor.phone = request.POST['phone']
            doctor.email = request.POST['email']
            doctor.save()
            return JsonResponse({'status': 'success'})
        except Doctor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Doctor not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid'})

@csrf_exempt
def add_doctor_inline(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            doctor = Doctor.objects.create(
                name=request.POST['name'],
                password=request.POST['password'],
                qualification=request.POST.get('qualification', ''),
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', '')
            )
            return JsonResponse({'status': 'success', 'doctor_id': doctor.doctor_id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid'})

@csrf_exempt
def update_schedule_inline(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        try:
            schedule = DoctorSchedule.objects.get(id=id)
            schedule.date = date
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.save()
            return JsonResponse({'status': 'success'})
        except DoctorSchedule.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Schedule not found'})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'})


@csrf_exempt
def delete_schedule(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        DoctorSchedule.objects.filter(id=id).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

@role_required(allowed_roles=['admin'])
def view_schedule(request):
    form = DoctorScheduleForm()
    search_form = ScheduleSearchForm(request.GET)
    schedules = DoctorSchedule.objects.all()
    doctors = Doctor.objects.all()
    if search_form.is_valid():
        selected_date = search_form.cleaned_data.get('date')
        if selected_date:
            schedules = schedules.filter(date=selected_date)
    name_query = request.GET.get('name')
    if name_query:
        schedules = schedules.filter(doctor__name__icontains=name_query)   
    today = date.today()
    schedules = schedules.filter(date__gte=today).order_by('date', 'start_time')    
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_schedule')

    return render(request, 'view_schedule.html', {
        'schedules': schedules,
        'form': form,
        'search_form': search_form,
        'doctors': doctors
    })


@csrf_exempt
def update_patient(request, patient_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.name = data.get('name', patient.name)
            patient.email = data.get('email', patient.email)
            patient.gender = data.get('gender', patient.gender)
            patient.age = data.get('age', patient.age)
            patient.phone = data.get('phone', patient.phone)
            patient.whatsapp = data.get('whatsapp', patient.whatsapp)
            patient.address = data.get('address', patient.address)
            patient.save()
            return JsonResponse({'success': True})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})

@csrf_exempt
def delete_patient(request, patient_id):
    if request.method == "POST":
        try:
            Patient.objects.get(id=patient_id).delete()
            return JsonResponse({'success': True})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})

@role_required(allowed_roles=['admin'])    
def treatment_view(request):
    treatments = Treatment.objects.all()
    form = TreatmentForm()

    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('treatment')  

    return render(request, 'treatment.html', {'treatments': treatments, 'form': form})

@csrf_exempt
def update_treatment(request, treatment_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            treatment = Treatment.objects.get(pk=treatment_id)
            treatment.name = data['name']
            treatment.price = data['price']
            treatment.save()
            return JsonResponse({'success': True})
        except Treatment.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

@csrf_exempt
def delete_treatment(request, treatment_id):
    if request.method == 'POST':
        try:
            treatment = Treatment.objects.get(pk=treatment_id)
            treatment.delete()
            return JsonResponse({'success': True})
        except Treatment.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

@role_required(allowed_roles=['doctor', 'admin'])       
def patient_appointments(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    doctors = Doctor.objects.all()

    warning = None

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST['date']
        time = request.POST['time']
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        selected_time = datetime.strptime(time, "%H:%M").time()
        schedules = DoctorSchedule.objects.filter(doctor=doctor, date=date)
        is_available = any(
            schedule.start_time <= selected_time <= schedule.end_time
            for schedule in schedules
        )
        if not is_available:
            warning = f"Doctor {doctor.name} is not available on {date} at {time}."
        else:
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=date,
                time=time
            )
            return redirect('patient_appointments', patient_id=patient.id)

    return render(request, 'appointment.html', {
        'patient': patient,
        'appointments': appointments,
        'doctors': doctors,
        'warning': warning,
    })

def delete_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@role_required(allowed_roles=['doctor', 'admin'])
def all_appointments(request):
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'all_appointments.html', {'appointments': appointments})

#def send_sms(request):
#    if request.method == "POST":
#        appointment_id = request.POST.get("appointment_id")
#        try:
 #           appointment = Appointment.objects.get(id=appointment_id)
#            print(f"[SIMULATED SMS] To: {appointment.patient.phone} - Hello {appointment.patient.name}, your appointment is on {appointment.date} at {appointment.time} with Dr. {appointment.doctor.name}.")
#            appointment.sms_status = "sent"
#            appointment.save()
#            return JsonResponse({"status": "success", "message": "SMS sent", "new_status": "sent"})
#        except Appointment.DoesNotExist:
#            return JsonResponse({"status": "error", "message": "Appointment not found"})
        
@role_required(allowed_roles=['doctor', 'admin'])
def patient_dashboard(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = PatientForm()

    today = date.today()
    patients = Patient.objects.all().order_by('-created_at')

    appointment_map = {}

    for patient in patients:
        # Appointments
        last_appointment = Appointment.objects.filter(patient=patient, date__lt=today).order_by('-date').first()
        next_appointments = Appointment.objects.filter(patient=patient, date__gte=today).order_by('date')

        appointment_map[patient.id] = {
            'last': last_appointment.date if last_appointment else None,
            'next': [appt.date for appt in next_appointments]
        }

        # Payments:
        total_paid = Payment.objects.filter(patient=patient).aggregate(
            total=Coalesce(Sum('paid_amount'), Decimal('0.00'))
        )['total']

        total_diagnosis_amount = Diagnosis.objects.filter(patient=patient).aggregate(
            total=Coalesce(Sum('amount'), Decimal('0.00'))
        )['total']

        total_pending = total_diagnosis_amount - total_paid if total_diagnosis_amount else Decimal('0.00')

        # Attach directly to patient
        patient.paid_amount = total_paid
        patient.pending_amount = total_pending

    context = {
        'form': form,
        'patients': patients,
        'appointment_map': appointment_map,
    }
    return render(request, 'patients.html', context)


    
def logout_view(request):
    request.session.flush()  
    return redirect('signin')  