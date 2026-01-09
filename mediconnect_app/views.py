from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import (
    CustomUser, DoctorProfile, PatientProfile, MedicalForm, 
    MedicalRecord, Appointment, Checkup, Prescription, Medication, Message
)
from .forms import (
    LoginForm, DoctorSignUpForm, PatientSignUpForm, MedicalFormForm,
    MedicalRecordForm, AppointmentBookForm, CheckupForm, PrescriptionForm,
    MedicationForm, AppointmentUpdateForm
)


# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def signup_role_selection(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'auth/signup_role.html')


def doctor_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            # Create user
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role='doctor'
            )
            
            # Create doctor profile
            DoctorProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                specialization=form.cleaned_data['specialization'],
                years_of_experience=form.cleaned_data['years_of_experience'],
                license_number=form.cleaned_data['license_number'],
                clinic_name=form.cleaned_data['clinic_name'],
                clinic_address=form.cleaned_data['clinic_address'],
                working_hours=form.cleaned_data['working_hours']
            )
            
            # Log in the user
            user = authenticate(request, username=user.email, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = DoctorSignUpForm()
    
    return render(request, 'auth/doctor_signup.html', {'form': form})


def patient_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            # Create user
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role='patient'
            )
            
            # Create patient profile
            PatientProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country']
            )
            
            # Log in the user
            user = authenticate(request, username=user.email, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('complete_medical_form', user_id=user.id)
    else:
        form = PatientSignUpForm()
    
    return render(request, 'auth/patient_signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Medical Form
@login_required
def complete_medical_form(request, user_id):
    # Ensure user can only complete their own form
    if request.user.id != user_id or request.user.role != 'patient':
        return redirect('dashboard')
    
    patient_profile = get_object_or_404(PatientProfile, user__id=user_id)
    
    # Check if form already exists
    if hasattr(patient_profile, 'medical_form'):
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        form = MedicalFormForm(request.POST)
        if form.is_valid():
            medical_form = MedicalForm.objects.create(
                patient=patient_profile,
                has_chronic_diseases=form.cleaned_data.get('has_chronic_diseases', False),
                has_allergies=form.cleaned_data.get('has_allergies', False),
                has_family_history=form.cleaned_data.get('has_family_history', False),
            )
            
            # Process chronic diseases
            if form.cleaned_data.get('chronic_disease_choices'):
                medical_form.chronic_diseases = ', '.join(form.cleaned_data['chronic_disease_choices'])
            
            # Process allergies
            if form.cleaned_data.get('allergies'):
                medical_form.allergies = form.cleaned_data['allergies']
            
            # Process vaccines
            if form.cleaned_data.get('vaccine_choices'):
                medical_form.vaccines = ', '.join(form.cleaned_data['vaccine_choices'])
            
            # Process family history
            if form.cleaned_data.get('family_history_choices'):
                medical_form.family_history = ', '.join(form.cleaned_data['family_history_choices'])
            
            medical_form.save()
            
            return redirect('patient_dashboard')
    else:
        form = MedicalFormForm()
    
    return render(request, 'patient/complete_medical_form.html', {
        'form': form,
        'patient_profile': patient_profile
    })


# Dashboard Views
@login_required
def dashboard(request):
    user = request.user
    
    if user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    else:
        return redirect('login')


@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    patient = get_object_or_404(PatientProfile, user=request.user)
    
    # Get latest checkup
    latest_checkup = patient.checkups.first()
    latest_checkup = Checkup.objects.filter(patient=patient).order_by('-created_at').first()
    
    # Get upcoming appointments (next 3)
    today = date.today()
    upcoming_appointments = patient.appointments.filter(
        date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).order_by('date', 'time')[:3]
    
    # Get active medications count
    active_medications_count = patient.medications.filter(status='active').count()
    
    context = {
        'patient': patient,
        'latest_checkup': latest_checkup,
        'upcoming_appointments': upcoming_appointments,
        'active_medications_count': active_medications_count,
    }
    
    return render(request, 'patient/dashboard.html', context)


@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    
    # Total unique patients
    total_patients = doctor.appointments.values('patient').distinct().count()
    
    # Today's appointments count
    today = date.today()
    today_appointments = doctor.appointments.filter(
        date=today,
        status__in=['scheduled', 'confirmed']
    )
    today_appointments_count = today_appointments.count()
    
    # Completed vs remaining today
    completed_today = doctor.appointments.filter(
        date=today,
        status='completed'
    ).count()
    remaining_today = today_appointments_count - completed_today
    
    # Pending prescriptions today
    pending_prescriptions = doctor.prescriptions.filter(
        created_at__date=today
    ).count()
    
    # Today's schedule (next 4 appointments)
    next_4_appointments = today_appointments.order_by('time')[:4]
    
    # Recent patients
    recent_patients = PatientProfile.objects.filter(
        appointments__doctor=doctor
    ).distinct().order_by('-appointments__created_at')[:5]
    
    context = {
        'doctor': doctor,
        'total_patients': total_patients,
        'today_appointments_count': today_appointments_count,
        'completed_today': completed_today,
        'remaining_today': remaining_today,
        'pending_prescriptions': pending_prescriptions,
        'next_4_appointments': next_4_appointments,
        'recent_patients': recent_patients,
    }
    
    return render(request, 'doctor/dashboard.html', context)


# Profile Views
@login_required
def patient_profile(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    patient = get_object_or_404(PatientProfile, user=request.user)
    medical_form = getattr(patient, 'medical_form', None)
    
    # Process medical form data for template
    medical_data = None
    if medical_form:
        medical_data = {
            'has_chronic_diseases': medical_form.has_chronic_diseases,
            'chronic_diseases': [d.strip() for d in medical_form.chronic_diseases.split(',') if d.strip()] if medical_form.chronic_diseases else [],
            'has_allergies': medical_form.has_allergies,
            'allergies': medical_form.allergies,
            'vaccines': [v.strip() for v in medical_form.vaccines.split(',') if v.strip()] if medical_form.vaccines else [],
            'has_family_history': medical_form.has_family_history,
            'family_history': [f.strip() for f in medical_form.family_history.split(',') if f.strip()] if medical_form.family_history else [],
        }
    
    context = {
        'patient': patient,
        'medical_form': medical_data,
    }
    
    return render(request, 'patient/profile.html', context)


@login_required
def doctor_profile(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    
    context = {
        'doctor': doctor,
    }
    
    return render(request, 'doctor/profile.html', context)


# Appointment Views
@login_required
def symptom_checker(request):
    if request.user.role != 'patient':
        messages.error(request, "Only patients can access the Symptom Checker.")
        return redirect('dashboard')
    return render(request, 'patient/checkup_checker.html')

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    patient = get_object_or_404(PatientProfile, user=request.user)
    
    if request.method == 'POST':
        form = AppointmentBookForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('appointments_list')
    else:
        form = AppointmentBookForm()
    
    return render(request, 'appointments/book_appointment.html', {
        'form': form,
        'patient': patient
    })


@login_required
def appointments_list(request):
    if request.user.role == 'patient':
        patient = get_object_or_404(PatientProfile, user=request.user)
        appointments = patient.appointments.all().order_by('-date', '-time')
        return render(request, 'appointments/appointments_list.html', {
            'appointments': appointments
        })
    elif request.user.role == 'doctor':
        return redirect('doctor_appointments_list')
    else:
        return redirect('dashboard')


@login_required
def doctor_appointments_list(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointments = doctor.appointments.all().order_by('-date', '-time')
    
    # Filter options
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_choices': ['scheduled', 'confirmed', 'completed', 'cancelled'],
        'selected_status': status_filter,
    }
    
    return render(request, 'doctor/appointments_list.html', context)


@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check authorization
    if request.user.role == 'patient':
        if appointment.patient.user != request.user:
            return redirect('dashboard')
    elif request.user.role == 'doctor':
        if appointment.doctor.user != request.user:
            return redirect('dashboard')
    else:
        return redirect('dashboard')
    
    if request.method == 'POST' and request.user.role == 'doctor':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentUpdateForm(instance=appointment) if request.user.role == 'doctor' else None
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    
    return render(request, 'appointments/appointment_detail.html', context)


# Medical Records
@login_required
def medical_records_list(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    patient = get_object_or_404(PatientProfile, user=request.user)
    medical_records = patient.medical_records.all()
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('medical_records_list')
    else:
        form = MedicalRecordForm()
    
    context = {
        'medical_records': medical_records,
        'form': form,
    }
    
    return render(request, 'patient/medical_records_list.html', context)


@login_required
def delete_medical_record(request, record_id):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    if record.patient.user != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        record.delete()
        return redirect('medical_records_list')
    
    return render(request, 'patient/delete_medical_record.html', {'record': record})


# Checkup Views
@login_required
def doctor_patient_list(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    
    # Get unique patients for this doctor
    patients = PatientProfile.objects.filter(
        appointments__doctor=doctor
    ).distinct().order_by('user__first_name')
    
    context = {
        'patients': patients,
        'doctor': doctor,
    }
    
    return render(request, 'doctor/patient_list.html', context)


@login_required
def record_checkup(request, patient_id):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    
    # Verify this doctor has seen this patient
    has_appointment = Appointment.objects.filter(
        doctor=doctor,
        patient=patient
    ).exists()
    
    if not has_appointment:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CheckupForm(request.POST)
        if form.is_valid():
            checkup = form.save(commit=False)
            checkup.patient = patient
            checkup.doctor = request.user.doctor_profile
            checkup.save()

            # Handle Lab Tests
            test_names = request.POST.getlist('test_name[]')
            result_values = request.POST.getlist('result_value[]')
            units = request.POST.getlist('unit[]')
            reference_ranges = request.POST.getlist('reference_range[]')
            
            for i in range(len(test_names)):
                if test_names[i] and result_values[i]:  # Only save if name and result exist
                    LabTest.objects.create(
                        checkup=checkup,
                        test_name=test_names[i],
                        result_value=result_values[i],
                        unit=units[i] if i < len(units) else '',
                        reference_range=reference_ranges[i] if i < len(reference_ranges) else ''
                    )

            messages.success(request, "Checkup recorded successfully.")
            return redirect('doctor_patients_list')
    else:
        form = CheckupForm()
    
    context = {
        'form': form,
        'patient': patient,
        'doctor': doctor,
    }
    
    return render(request, 'doctor/record_checkup.html', context)


@login_required
def checkup_detail(request, checkup_id):
    checkup = get_object_or_404(Checkup, id=checkup_id)
    
    if request.user.role == 'patient':
        if checkup.patient.user != request.user:
            return redirect('dashboard')
    elif request.user.role == 'doctor':
        if checkup.doctor.user != request.user:
            return redirect('dashboard')
    else:
        return redirect('dashboard')
    
    bmi = checkup.calculate_bmi()
    bmi_category = checkup.get_bmi_category()
    
    context = {
        'checkup': checkup,
        'bmi': bmi,
        'bmi_category': bmi_category,
    }
    
    return render(request, 'checkup/checkup_detail.html', context)


# Prescription Views
@login_required
def add_prescription(request, checkup_id):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    checkup = get_object_or_404(Checkup, id=checkup_id)
    
    if checkup.doctor.user != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.checkup = checkup
            prescription.patient = checkup.patient
            prescription.doctor = checkup.doctor
            prescription.save()
            
            # Create medication record
            Medication.objects.create(
                patient=checkup.patient,
                prescription=prescription,
                medication_name=prescription.medication_name,
                dosage=prescription.dosage,
                frequency=prescription.frequency,
                status='active',
                start_date=date.today(),
            )
            
            # Check if user wants to add more prescriptions
            if 'add_another' in request.POST:
                return redirect('add_prescription', checkup_id=checkup.id)
            else:
                return redirect('checkup_detail', checkup_id=checkup.id)
    else:
        form = PrescriptionForm()
    
    context = {
        'form': form,
        'checkup': checkup,
    }
    
    return render(request, 'prescription/add_prescription.html', context)


@login_required
def prescriptions_list(request):
    if request.user.role == 'patient':
        patient = get_object_or_404(PatientProfile, user=request.user)
        prescriptions = patient.prescriptions.all().order_by('-created_at')
        
        context = {
            'prescriptions': prescriptions,
        }
        
        return render(request, 'prescription/prescriptions_list.html', context)
    else:
        return redirect('dashboard') # Doctors don't have a direct 'prescriptions_list' view, they see them via patient detail


@login_required
def medications_list(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
        
    patient = request.user.patient_profile
    status_filter = request.GET.get('status')
    
    medications = Medication.objects.filter(patient=patient).order_by('-start_date')
    
    if status_filter:
        medications = medications.filter(status=status_filter)
        
    context = {
        'medications': medications,
        'selected_status': status_filter,
    }
    
    return render(request, 'patient/medications_list.html', context)


@login_required
def edit_medication(request, medication_id):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    medication = get_object_or_404(Medication, id=medication_id)
    
    if medication.patient.user != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('medications_list')
    else:
        form = MedicationForm(instance=medication)
    
    context = {
        'form': form,
        'medication': medication,
    }
    
    return render(request, 'patient/edit_medication.html', context)


@login_required
def doctor_patient_detail(request, patient_id):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    
    # Check if doctor has ever had an appointment with this patient
    has_access = Appointment.objects.filter(doctor=doctor, patient=patient).exists()
    
    if not has_access:
        # Redirect if no access
        return redirect('doctor_patients_list')
        
    # Gather all data
    medical_form = getattr(patient, 'medical_form', None)
    medical_records = patient.medical_records.all()
    checkups = patient.checkups.filter(doctor=doctor).order_by('-created_at')
    prescriptions = patient.prescriptions.filter(doctor=doctor).order_by('-created_at')
    
    # Process medical form data for template
    medical_data = None
    if medical_form:
        medical_data = {
            'has_chronic_diseases': medical_form.has_chronic_diseases,
            'chronic_diseases': [d.strip() for d in medical_form.chronic_diseases.split(',') if d.strip()] if medical_form.chronic_diseases else [],
            'has_allergies': medical_form.has_allergies,
            'allergies': medical_form.allergies,
            'vaccines': [v.strip() for v in medical_form.vaccines.split(',') if v.strip()] if medical_form.vaccines else [],
            'has_family_history': medical_form.has_family_history,
            'family_history': [f.strip() for f in medical_form.family_history.split(',') if f.strip()] if medical_form.family_history else [],
        }

    context = {
        'patient': patient,
        'medical_form': medical_data,
        'medical_records': medical_records,
        'checkups': checkups,
        'prescriptions': prescriptions,
    }
    
    return render(request, 'doctor/patient_detail.html', context)


# Chatbot View
@login_required
def chatbot(request):
    chat_history = []
    response = None
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip().lower()
        
        if user_message:
            chat_history.append({'role': 'user', 'text': user_message})
            response = handle_chatbot_query(user_message, request.user)
            chat_history.append({'role': 'bot', 'text': response})
    
    context = {
        'messages': chat_history,
        'response': response,
    }
    
    return render(request, 'chatbot.html', context)


from .utils import predict_disease

def handle_chatbot_query(message, user):
    """Advanced chatbot query handler"""
    
    # Greeting responses
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return f"Hello {user.first_name}! 👋 I'm MediConnect Assistant. How can I help you today?"
    
    # Symptom Analysis (Keyword detection for prediction)
    # Check if message contains multiple symptoms
    detected_symptoms = []
    # This matches symptoms from our list (simple contains check)
    from .utils import DISEASE_PATTERNS
    all_symptoms = set()
    for pattern in DISEASE_PATTERNS.values():
        all_symptoms.update(pattern)
        
    for s in all_symptoms:
        if s.replace('_', ' ') in message or s in message:
            detected_symptoms.append(s)
            
    if len(detected_symptoms) >= 2:
        predictions = predict_disease(detected_symptoms)
        if predictions:
            top = predictions[0]
            response = f"Based on symptoms ({', '.join(detected_symptoms)}), it might be **{top['disease']}** ({top['probability']}% confidence). "
            response += "Please consult a doctor for accuracy."
            return response

    # Symptom Analysis (Simple keyword matching for advice)
    symptoms_advice = {
        'headache': 'Headaches can be caused by stress, dehydration, or eye strain. If it persists, please book an appointment.',
        'fever': 'A fever usually indicates your body is fighting an infection. Drink plenty of fluids and rest. If it exceeds 39°C (102°F), see a doctor immediately.',
        'cold': 'Common cold symptoms include runny nose and sore throat. Rest and hydration are key.',
        'pain': 'Where is the pain located? If it is severe or sudden chest pain, please seek emergency help immediately.',
        'tired': 'Fatigue can be due to lack of sleep, stress, or nutritional deficiency. Ensure you are getting 7-8 hours of sleep.',
    }
    
    for symptom, advice in symptoms_advice.items():
        if symptom in message:
            return f"I noticed you mentioned '{symptom}'. {advice}"

    # Appointment queries
    if 'appointment' in message:
        if user.role == 'patient':
            count = Appointment.objects.filter(patient__user=user, status='scheduled').count()
            return f"You have {count} scheduled appointment(s). You can book more by going to 'Book Appointment' from the menu."
        else:
            count = Appointment.objects.filter(doctor__user=user, status='scheduled').count()
            return f"You have {count} upcoming appointments scheduled."
    
        return "You can manage your appointments in the 'Appointments' section. Do you want to book a new one?"
        
    if 'record' in message or 'history' in message:
        return "Your medical records are available in the 'Records' tab."
        
    if 'medication' in message or 'drug' in message:
        return "You can view your active medications in the 'Medications' section."

    return "I'm here to help! I can assist with appointments, symptom advice, medications, and navigating the portal. How can I facilitate your healthcare journey today?"


@login_required
def update_appointment_status(request, appointment_id, new_status):
    if request.user.role != 'doctor':
        return redirect('dashboard')
        
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.doctor.user != request.user:
        return redirect('dashboard')
        
    if new_status in dict(Appointment.STATUS_CHOICES):
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"Appointment updated to {appointment.get_status_display()}")
        
    return redirect('doctor_appointments_list')

# Edit Profile Views
@login_required
def edit_patient_profile(request):
    if request.user.role != 'patient':
        return redirect('dashboard')
    
    patient = get_object_or_404(PatientProfile, user=request.user)
    
    if request.method == 'POST':
        # Handles User model fields (first_name, last_name, email)
        user_form = PatientSignUpForm(request.POST, instance=request.user)
        # We need a separate form for profile fields if we want to edit them, 
        # but for now we'll reuse the signup form structure or just update manually
        # ideally we should have a PatientUpdateForm.
        # Let's assume we update basic info via the User model form part
        
        # Simplified update logic for this task to ensure functionality
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        patient.phone = request.POST.get('phone')
        patient.city = request.POST.get('city')
        patient.country = request.POST.get('country')
        patient.save()
        
        messages.success(request, "Profile updated successfully.")
        return redirect('patient_profile')

    return render(request, 'patient/edit_profile.html', {'patient': patient, 'user': request.user})

@login_required
def edit_doctor_profile(request):
    if request.user.role != 'doctor':
        return redirect('dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        doctor.phone = request.POST.get('phone')
        doctor.specialization = request.POST.get('specialization')
        doctor.clinic_name = request.POST.get('clinic_name')
        doctor.clinic_address = request.POST.get('clinic_address')
        doctor.save()
        
        messages.success(request, "Profile updated successfully.")
        return redirect('doctor_profile')

    return render(request, 'doctor/edit_profile.html', {'doctor': doctor, 'user': request.user})

# AJAX API endpoints
@login_required
def get_doctor_availability(request, doctor_id):
    """Get available time slots for a doctor"""
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    appointment_date = request.GET.get('date')
    
    if not appointment_date:
        return JsonResponse({'error': 'Date is required'}, status=400)
    
    # Get existing appointments for this doctor on this date
    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=appointment_date,
        status__in=['scheduled', 'confirmed']
    ).values_list('time', flat=True)
    
    # Generate time slots (30-minute intervals from 9 AM to 5 PM)
    time_slots = []
    current_time = datetime.strptime('09:00', '%H:%M')
    end_time = datetime.strptime('17:00', '%H:%M')
    
    while current_time <= end_time:
        time_str = current_time.strftime('%H:%M')
        # Check if slot is already taken
        is_taken = False
        for taken_time in existing_appointments:
            # Simple string comparison might fail if formats differ, ensuring consistent comparison
            if str(taken_time)[:5] == time_str:
                is_taken = True
                break
        
        if not is_taken:
            time_slots.append(time_str)
            
        current_time += timedelta(minutes=30)
    
    return JsonResponse({'time_slots': time_slots})


# Messaging Views
@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'messaging/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        recipient = get_object_or_404(CustomUser, id=recipient_id)
        
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        messages.success(request, "Message sent successfully.")
        return redirect('inbox')
    
    # Get potential recipients
    if request.user.role == 'patient':
        # Patients can message their doctors (from appointments)
        doctor_ids = Appointment.objects.filter(patient__user=request.user).values_list('doctor__user__id', flat=True).distinct()
        recipients = CustomUser.objects.filter(id__in=doctor_ids)
    else:
        # Doctors can message their patients
        patient_ids = Appointment.objects.filter(doctor__user=request.user).values_list('patient__user__id', flat=True).distinct()
        recipients = CustomUser.objects.filter(id__in=patient_ids)
        
    return render(request, 'messaging/send_message.html', {'recipients': recipients})
