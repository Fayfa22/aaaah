from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import os

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    phone = models.CharField(max_length=8, validators=[MinValueValidator(10000000)])
    specialization = models.CharField(max_length=100)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    license_number = models.CharField(max_length=50, unique=True)
    clinic_name = models.CharField(max_length=150)
    clinic_address = models.TextField()
    working_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.specialization}"


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=8, validators=[MinValueValidator(10000000)])
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class MedicalForm(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name='medical_form')
    
    # Chronic diseases
    has_chronic_diseases = models.BooleanField(default=False)
    chronic_diseases = models.TextField(blank=True, help_text="Comma separated: Diabetes, Hypertension, Asthma, Heart Disease, Cancer, Kidney Disease, Liver Disease, Other")
    
    # Allergies
    has_allergies = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)
    
    # Vaccines
    vaccines = models.TextField(blank=True, help_text="Comma separated: BCG, Hepatitis B, Polio, MMR, Tetanus, Influenza, COVID-19")
    
    # Family history
    has_family_history = models.BooleanField(default=False)
    family_history = models.TextField(blank=True, help_text="Comma separated: Diabetes, Hypertension, Cancer, Heart Disease, Other")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Medical Form - {self.patient.user.first_name}"


def medical_file_path(instance, filename):
    return os.path.join('medical_records', str(instance.patient.user.id), filename)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_records')
    file = models.FileField(upload_to=medical_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Medical Record - {self.patient.user.first_name}"
    
    class Meta:
        ordering = ['-uploaded_at']


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Appointment - {self.patient.user.first_name} with Dr. {self.doctor.user.first_name}"
    
    class Meta:
        ordering = ['-date', '-time']
        unique_together = ('patient', 'doctor', 'date', 'time')


class Checkup(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='checkups')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='checkups')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='checkup')
    
    # Vital signs
    heart_rate = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(200)])
    blood_pressure_systolic = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(250)])
    blood_pressure_diastolic = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(150)])
    temperature = models.FloatField(validators=[MinValueValidator(95.0), MaxValueValidator(108.0)])
    oxygen_saturation = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(100)])
    weight = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    height = models.FloatField(validators=[MinValueValidator(50), MaxValueValidator(300)])
    
    # Clinical
    symptoms = models.TextField()
    diagnosis = models.TextField()
    predicted_disease = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_bmi(self):
        # BMI = weight (kg) / (height (m))^2
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)
    
    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def __str__(self):
        return f"Checkup - {self.patient.user.first_name} ({self.created_at.date()})"


class Prescription(models.Model):
    checkup = models.ForeignKey(Checkup, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='prescriptions')
    
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100, help_text="e.g., 3 times a day, twice daily")
    duration = models.CharField(max_length=100, help_text="e.g., 10 days, 2 weeks")
    instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.medication_name} - {self.patient.user.first_name}"
    
    class Meta:
        ordering = ['-created_at']


class Medication(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued'),
    )
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medications')
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True, related_name='medications')
    
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medication_name} - {self.patient.user.first_name}"
    
    class Meta:
        ordering = ['-start_date']
