# MediConnect - Quick Start Guide

## 🚀 Run the Application in 3 Steps

### Step 1: Install & Setup (One-time)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual Setup:**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Step 2: Start Server

```bash
python manage.py runserver
```

### Step 3: Access Application

- **Main App:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📝 Test the Application

### Create Test Accounts:

**Option A: Use Admin Panel**
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Add User" or "Add Doctor Profile" / "Add Patient Profile"

**Option B: Use Sign Up Pages**
1. Go to http://127.0.0.1:8000/
2. Click "Sign Up"
3. Select "Doctor" or "Patient"
4. Fill in required information
5. Complete medical form (if patient)

---

## 🧪 Test Scenarios

### As a Patient:

1. Sign up with patient account
2. Complete medical history form
3. Go to "Book Appointment"
4. Select a doctor
5. Choose date and time
6. Submit appointment
7. Check dashboard for upcoming appointments
8. Upload medical records
9. View medications and prescriptions
10. Use chatbot for help

### As a Doctor:

1. Sign up with doctor account
2. Go to dashboard
3. Check "Today's Schedule"
4. Click on an appointment
5. Click "Record Checkup"
6. Fill in vital signs
7. Save checkup
8. Click "Add Prescription"
9. Create medications
10. View all patients

---

## 📊 Key Pages to Visit

### Patients:
- `/` - Login
- `/signup/` - Sign up role selection
- `/patient/dashboard/` - Dashboard with vital signs
- `/appointments/book/` - Book appointment
- `/appointments/` - View appointments
- `/medical-records/` - Upload records
- `/medications/` - View medications
- `/patient/profile/` - View profile
- `/chatbot/` - Chat with assistant

### Doctors:
- `/doctor/dashboard/` - Dashboard with metrics
- `/doctor/appointments/` - Manage appointments
- `/doctor/patients/` - View all patients
- `/doctor/checkup/<patient_id>/` - Record checkup
- `/doctor/profile/` - View profile

---

## 🔐 Test Credentials

After running `python manage.py createsuperuser`:
- Username: (email you entered)
- Password: (password you created)

---

## 📱 Features to Test

### Authentication:
- ✅ Login with email
- ✅ Sign up as patient
- ✅ Sign up as doctor
- ✅ Role-based redirects

### Appointments:
- ✅ Book appointment with future date
- ✅ View appointments
- ✅ Update appointment status (doctor)
- ✅ View appointment details

### Medical:
- ✅ Complete medical form
- ✅ Upload medical records
- ✅ Record vital signs
- ✅ Calculate BMI
- ✅ Add prescriptions
- ✅ Track medications

### Dashboard:
- ✅ Patient dashboard with metrics
- ✅ Doctor dashboard with schedule
- ✅ Display vital signs
- ✅ Show active medications

### UI/UX:
- ✅ Responsive design on mobile
- ✅ Form validation
- ✅ Error messages
- ✅ Status badges
- ✅ Chatbot responses

---

## 🐛 Troubleshooting

### Issue: "No module named 'django'"
**Solution:**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'mediconnect_app'"
**Solution:**
```bash
python manage.py makemigrations mediconnect_app
python manage.py migrate
```

### Issue: Static files not loading (CSS)
**Solution:**
```bash
python manage.py collectstatic
```

### Issue: Database locked
**Solution:**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Port 8000 already in use
**Solution:**
```bash
python manage.py runserver 8001
# Then visit http://127.0.0.1:8001/
```

---

## 📚 Directory Structure

```
mediconnect/
├── manage.py                 ← Run commands here
├── db.sqlite3                ← Database file
├── requirements.txt          ← Dependencies
├── setup.bat / setup.sh      ← Setup scripts
├── README.md                 ← Full documentation
├── COMPLETION_SUMMARY.md     ← What was built
├── mediconnect_project/      ← Django settings
└── mediconnect_app/          ← Main application
    ├── models.py             ← Database schemas
    ├── views.py              ← Business logic
    ├── forms.py              ← Form validation
    ├── urls.py               ← URL routing
    ├── admin.py              ← Admin config
    ├── templates/            ← HTML files
    └── static/css/           ← Styling
```

---

## 💡 Tips & Tricks

1. **Check Migrations:**
   ```bash
   python manage.py showmigrations
   ```

2. **Create Test Data in Shell:**
   ```bash
   python manage.py shell
   from mediconnect_app.models import CustomUser
   user = CustomUser.objects.first()
   print(user.email)
   ```

3. **Access Django Admin:**
   - Go to `/admin/`
   - View/edit all data
   - Create test records

4. **View Database:**
   - Use SQLite viewer (optional)
   - File: `db.sqlite3`

5. **Check Server Logs:**
   - Watch console output
   - Look for error messages
   - Check validation errors

---

## ✅ Development Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Migrations run
- [ ] Superuser created
- [ ] Server running on :8000
- [ ] Can access login page
- [ ] Can sign up as patient
- [ ] Can sign up as doctor
- [ ] Can book appointment
- [ ] Can record checkup
- [ ] Can add prescription
- [ ] Dashboard shows data
- [ ] Admin panel accessible

---

## 📞 Support

For issues:
1. Check README.md for detailed docs
2. Review COMPLETION_SUMMARY.md for features
3. Check console output for errors
4. Verify virtual environment is activated
5. Ensure all dependencies are installed

---

**Happy Testing! 🎉**

Need help? Check the full README.md or COMPLETION_SUMMARY.md
