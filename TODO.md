# TODO - Smart Attendance Web Portal (Flask)

- [ ] Step 1: Create required directory structure inside `Smart-Attendance/` (static/css, static/js, static/qr_codes, static/images; templates/*.html)
- [ ] Step 2: Replace `Smart-Attendance/app.py` with full Flask portal (login, admin dashboard, student registration, student profile, subjects management, QR attendance scanner, attendance records, excel export, reports, settings)
- [ ] Step 3: Implement CSV-backed storage:
  - [ ] students.csv with fields: StudentID, Name, Class, RollNumber, Subjects, Email, PasswordHash, QRCodeFile, AttendancePercentage (or computed)
  - [ ] attendance_log.csv with attendance events
- [ ] Step 4: Automatic QR generation on student registration (write PNG into `Smart-Attendance/static/qr_codes/`)
- [ ] Step 5: Frontend pages using Bootstrap 5 + Font Awesome, modern UI, connect to Flask routes
- [ ] Step 6: QR Attendance Scanner endpoint:
  - [ ] Provide a page that takes StudentID / QR payload
  - [ ] Validate token and append to attendance_log.csv
- [ ] Step 7: Reports Dashboard + Export to Excel (use `pandas` to write .xlsx)
- [ ] Step 8: Run & test:
  - [ ] `python Smart-Attendance/app.py`
  - [ ] verify registration->QR->student login->attendance->reports->export

