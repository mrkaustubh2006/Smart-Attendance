import csv
import os
import sys

try:
    import qrcode
except ImportError:
    print("❌ qrcode library not installed")
    print("Run: pip install qrcode[pil]")
    sys.exit(1)

# ================= PATH SAFETY =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(BASE_DIR, "students.csv")
QR_DIR = os.path.join(BASE_DIR, "qr_codes")

os.makedirs(QR_DIR, exist_ok=True)

# ================= INPUT =================
student_id = input("Enter Student ID (e.g. STD001: ").strip()
name = input("Enter Student Name: ").strip()
subjects = input("Enter Subjects (AI|ML|DS): ").strip()

if not student_id or not name or not subjects:
    print("❌ All fields are mandatory")
    sys.exit(1)

# ================= CHECK DUPLICATE =================
if os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row and row[0] == student_id:
                print("❌ Student ID already exists")
                sys.exit(1)

# ================= SAVE STUDENT =================
file_exists = os.path.exists(STUDENT_FILE)

with open(STUDENT_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["StudentID", "Name", "Subjects"])
    writer.writerow([student_id, name, subjects])

# ================= GENERATE QR =================
qr_data = student_id  # secure & simple
qr = qrcode.make(qr_data)

qr_path = os.path.join(QR_DIR, f"{student_id}.png")
qr.save(qr_path)

print("\n✅ STUDENT REGISTERED SUCCESSFULLY")
print("👤 Name:", name)
print("📘 Subjects:", subjects)
print("🔳 QR saved at:", qr_path)
