# MediConnect - Healthcare Management Platform

A comprehensive healthcare management platform built with Django and SQLite3, enabling doctors and patients to manage appointments, medical records, checkups, and prescriptions.

## Features

### For Patients:
- 👤 Email-based authentication with secure signup
- 📋 Book appointments with doctors
- 📄 Upload and manage medical records
- 💊 Track medications and prescriptions
- 💓 View vital signs from checkups
- 🏥 Complete medical history form
- 📱 View upcoming appointments and medical information
- 💬 Chat with AI assistant for quick help

### For Doctors:
- 👨‍⚕️ Professional profile management
- 📅 View and manage patient appointments
- 💓 Record patient vital signs and checkups
- 💊 Create prescriptions for patients
- 👥 Access patient medical history and records
- 📊 Dashboard with key metrics and statistics
- 💬 Chat with AI assistant

## Technology Stack

- **Backend:** Django 4.2.0
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Authentication:** Django built-in auth system with custom user model

## Installation & Setup

### 1. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
cd mediconnect
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Default Routes

- **Login:** http://127.0.0.1:8000/
- **Sign Up:** http://127.0.0.1:8000/signup/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## User Roles

### Patient
- Create account during signup
- Complete medical history form after registration
- Book appointments with available doctors
- Upload medical records
- Track vital signs from checkups
- Manage medications

### Doctor
- Create professional account with credentials
- Manage patient appointments
- Record patient checkups with vital signs
- Create prescriptions
- View patient medical history
- Access patient information

## Database Models

### Core Models:
1. **CustomUser** - Email-based user authentication
2. **DoctorProfile** - Doctor credentials and clinic information
3. **PatientProfile** - Patient demographics and information
4. **MedicalForm** - Patient medical history questionnaire
5. **MedicalRecord** - Uploaded medical documents
6. **Appointment** - Patient-doctor appointment booking
7. **Checkup** - Vital signs and clinical information
8. **Prescription** - Medications prescribed by doctors
9. **Medication** - Patient medication tracking

## Form Validations

- **Email:** Must be unique, valid email format
- **Phone:** Exactly 8 digits
- **Password:** Minimum 7 characters, 1 digit, 1 uppercase letter
- **Date of Birth:** Must be in past and patient must be 12+ years old
- **Appointment Date:** Must be in the future
- **Experience Years:** Maximum 70 years
- **City/Country:** Minimum 2 characters

## Key Features Implementation

### Authentication
- Email-based login/signup
- Separate signup flows for doctors and patients
- Secure password hashing
- Role-based access control

### Appointments
- Future date validation
- Time slot management
- Status tracking (scheduled, confirmed, completed, cancelled)
- Patient-doctor relationship tracking

### Medical Records
- File upload support (PDF, DOC, JPG, PNG)
- Organized by patient
- Download and delete functionality

### Vital Signs Tracking
- Heart rate, blood pressure, temperature
- Oxygen saturation, weight, height
- BMI calculation and categorization
- Clinical diagnosis recording

### Medications
- Prescription-based medication creation
- Status tracking (active, completed, discontinued)
- Start and end dates
- Patient medication history

### Dashboard
- **Patient Dashboard:** Upcoming appointments, vital signs, active medications
- **Doctor Dashboard:** Today's schedule, patient count, appointment metrics

### Chatbot
- Simple AI-like assistant for common questions
- Handles: appointments, doctors, prescriptions, medications, medical records
- Quick help for users

## Admin Panel

Access the admin panel at `/admin/` with superuser credentials to:
- Manage users and roles
- View all appointments
- Manage medical records
- Monitor prescriptions and medications
- Create test data

## UI/UX Features

- Professional healthcare color scheme (blues, greens)
- Responsive design for desktop and mobile
- Clean, intuitive navigation
- Status badges and indicators
- Form validation with error messages
- Smooth transitions and animations
- Mobile-friendly layout

## File Structure

```
mediconnect/
├── manage.py
├── requirements.txt
├── mediconnect_project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mediconnect_app/              # Main app
│   ├── models.py                 # Database models
│   ├── views.py                  # Business logic
│   ├── forms.py                  # Form definitions
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin configuration
│   ├── migrations/               # Database migrations
│   ├── templates/                # HTML templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── patient/
│   │   ├── doctor/
│   │   ├── appointments/
│   │   ├── checkup/
│   │   └── prescription/
│   └── static/
│       └── css/
│           └── style.css         # Main stylesheet
└── db.sqlite3                    # SQLite database
```

## Security Considerations

- CSRF protection enabled
- Password hashing with Django's built-in system
- Role-based access control
- Secure file uploads with validation
- User authentication required for sensitive operations

## Future Enhancements

- Email notifications for appointments
- SMS reminders
- Appointment rescheduling
- Advanced medical analytics
- Telemedicine/video consultations
- Multi-language support
- Export medical records to PDF
- Patient-doctor messaging system
- Insurance integration
- Medical AI diagnosis suggestions

## Troubleshooting

### Migration Issues
```bash
python manage.py makemigrations mediconnect_app
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Reset
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Support

For issues or questions, please contact the development team or refer to Django documentation at https://docs.djangoproject.com/

## License

This project is provided as-is for educational and healthcare management purposes.

---

**MediConnect v1.0** - Healthcare at your fingertips
