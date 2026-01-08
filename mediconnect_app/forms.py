from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from datetime import date
import re
from .models import (
    CustomUser, DoctorProfile, PatientProfile, MedicalForm, 
    MedicalRecord, Appointment, Checkup, Prescription, Medication
)


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.check_password(password):
                    raise ValidationError("Invalid email or password")
            except CustomUser.DoesNotExist:
                raise ValidationError("Invalid email or password")
        
        return self.cleaned_data


class DoctorSignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password (min 7 chars, 1 digit, 1 uppercase)'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))
    
    phone = forms.CharField(max_length=8, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '8 digit phone number'
    }))
    specialization = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Specialization (e.g., Cardiology)'
    }))
    years_of_experience = forms.IntegerField(min_value=0, max_value=70, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Years of Experience (max 70)'
    }))
    license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'License Number'
    }))
    clinic_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Clinic Name'
    }))
    clinic_address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Clinic Address',
        'rows': 3
    }))
    working_hours = forms.CharField(max_length=100, initial="9:00 AM - 5:00 PM", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Working Hours'
    }))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 8:
            raise ValidationError("Phone must be exactly 8 digits")
        return phone
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 7:
            raise ValidationError("Password must be at least 7 characters")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least 1 digit")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least 1 uppercase letter")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data


class PatientSignUpForm(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password (min 7 chars, 1 digit, 1 uppercase)'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))
    
    phone = forms.CharField(max_length=8, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '8 digit phone number'
    }))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-input'
    }))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Country'
    }))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 8:
            raise ValidationError("Phone must be exactly 8 digits")
        return phone
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 7:
            raise ValidationError("Password must be at least 7 characters")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least 1 digit")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least 1 uppercase letter")
        return password
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        
        if dob >= today:
            raise ValidationError("Date of birth must be in the past")
        
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 12:
            raise ValidationError("You must be at least 12 years old")
        
        return dob
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if len(city) < 2:
            raise ValidationError("City must be at least 2 characters")
        return city
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if len(country) < 2:
            raise ValidationError("Country must be at least 2 characters")
        return country
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data


class MedicalFormForm(forms.ModelForm):
    # Chronic diseases
    has_chronic_diseases = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    chronic_disease_choices = forms.MultipleChoiceField(
        choices=[
            ('Diabetes', 'Diabetes'),
            ('Hypertension', 'Hypertension'),
            ('Asthma', 'Asthma'),
            ('Heart Disease', 'Heart Disease'),
            ('Cancer', 'Cancer'),
            ('Kidney Disease', 'Kidney Disease'),
            ('Liver Disease', 'Liver Disease'),
            ('Other', 'Other'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    # Allergies
    has_allergies = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    allergies = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Describe your allergies'
    }))
    
    # Vaccines
    vaccine_choices = forms.MultipleChoiceField(
        choices=[
            ('BCG', 'BCG'),
            ('Hepatitis B', 'Hepatitis B'),
            ('Polio', 'Polio'),
            ('MMR', 'MMR'),
            ('Tetanus', 'Tetanus'),
            ('Influenza', 'Influenza'),
            ('COVID-19', 'COVID-19'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    # Family history
    has_family_history = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    family_history_choices = forms.MultipleChoiceField(
        choices=[
            ('Diabetes', 'Diabetes'),
            ('Hypertension', 'Hypertension'),
            ('Cancer', 'Cancer'),
            ('Heart Disease', 'Heart Disease'),
            ('Other', 'Other'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    class Meta:
        model = MedicalForm
        fields = ['has_chronic_diseases', 'has_allergies', 'has_family_history']


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the document'
            })
        }


class AppointmentBookForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your symptoms or reason for appointment'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = DoctorProfile.objects.all()
    
    def clean_date(self):
        appointment_date = self.cleaned_data.get('date')
        if appointment_date and appointment_date <= date.today():
            raise ValidationError("Appointment date must be in the future")
        return appointment_date


class CheckupForm(forms.ModelForm):
    class Meta:
        model = Checkup
        fields = [
            'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'temperature', 'oxygen_saturation', 'weight', 'height',
            'symptoms', 'diagnosis', 'predicted_disease', 'notes'
        ]
        widgets = {
            'heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'bpm',
                'min': '30',
                'max': '200'
            }),
            'blood_pressure_systolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mmHg',
                'min': '50',
                'max': '250'
            }),
            'blood_pressure_diastolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mmHg',
                'min': '30',
                'max': '150'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°F',
                'min': '95.0',
                'max': '108.0',
                'step': '0.1'
            }),
            'oxygen_saturation': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '%',
                'min': '50',
                'max': '100'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'kg',
                'step': '0.1'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe symptoms'
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Clinical diagnosis'
            }),
            'predicted_disease': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Predicted disease (if any)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            })
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'medication_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Medication name'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 500mg'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3 times a day'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 10 days'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Special instructions (e.g., take with food)'
            })
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medication_name', 'dosage', 'frequency', 'status', 'start_date', 'end_date', 'notes']
        widgets = {
            'medication_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Medication name'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 500mg'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2 times daily'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            })
        }


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add notes to the appointment'
            })
        }
