from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, DoctorProfile, PatientProfile, MedicalForm,
    MedicalRecord, Appointment, Checkup, Prescription, Medication
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'phone', 'license_number')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('specialization', 'years_of_experience')
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Doctor'


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'gender', 'city', 'country')
    search_fields = ('user__first_name', 'user__last_name', 'city')
    list_filter = ('gender', 'city', 'country')
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Patient'


@admin.register(MedicalForm)
class MedicalFormAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'has_chronic_diseases', 'has_allergies')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    list_filter = ('has_chronic_diseases', 'has_allergies', 'has_family_history')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    get_patient_name.short_description = 'Patient'


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'description', 'uploaded_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    get_patient_name.short_description = 'Patient'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'date', 'time', 'status')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name')
    list_filter = ('status', 'date')
    readonly_fields = ('created_at',)
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    
    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    
    get_patient_name.short_description = 'Patient'
    get_doctor_name.short_description = 'Doctor'


@admin.register(Checkup)
class CheckupAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'created_at', 'get_bmi_category')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    
    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    
    get_patient_name.short_description = 'Patient'
    get_doctor_name.short_description = 'Doctor'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'get_patient_name', 'get_doctor_name', 'created_at')
    search_fields = ('medication_name', 'patient__user__first_name', 'doctor__user__first_name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    
    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    
    get_patient_name.short_description = 'Patient'
    get_doctor_name.short_description = 'Doctor'


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'get_patient_name', 'status', 'start_date')
    search_fields = ('medication_name', 'patient__user__first_name')
    list_filter = ('status', 'start_date')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    get_patient_name.short_description = 'Patient'
