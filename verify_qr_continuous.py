
import cv2
import csv
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import winsound
import sys
import time

# ===================== SUBJECT INPUT =====================

root = tk.Tk()
root.withdraw()

subject = simpledialog.askstring(
    "Subject",
    "Enter Subject Name:"
)

if not subject:
    print("❌ Subject not entered")
    sys.exit(1)

# ===================== LOAD STUDENTS =====================

df = pd.read_csv("students.csv")
df.columns = df.columns.str.strip()

STUDENTS = {}
STUDENT_SUBJECTS = {}

for _, row in df.iterrows():

    sid = str(row["StudentID"]).strip()
    name = str(row["Name"]).strip()
    subjects = str(row["Subjects"]).strip()

    STUDENTS[sid] = name
    STUDENT_SUBJECTS[sid] = [
        s.strip()
        for s in subjects.split("|")
    ]

# ===================== DUPLICATE CHECK =====================

def already_marked(student_id, subject, date):

    if not os.path.exists("attendance_log.csv"):
        return False

    with open(
        "attendance_log.csv",
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.reader(f)

        next(reader, None)

        for row in reader:

            if (
                len(row) >= 4
                and row[0] == student_id
                and row[2] == subject
                and row[3] == date
            ):
                return True

    return False

# ===================== SUBJECT CHECK =====================

def subject_allowed(student_id, subject):
    return subject in STUDENT_SUBJECTS.get(
        student_id,
        []
    )

# ===================== CAMERA =====================

cap = cv2.VideoCapture(0)

qr = cv2.QRCodeDetector()

today = datetime.now().strftime("%Y-%m-%d")

file_exists = os.path.exists(
    "attendance_log.csv"
)

last_scan_time = 0

SCAN_DELAY = 2

# ===================== SOUNDS =====================

def beep_ok():
    winsound.MessageBeep(
        winsound.MB_OK
    )

def beep_block():
    winsound.MessageBeep(
        winsound.MB_ICONHAND
    )

print("\n🚀 SMART ATTENDANCE SYSTEM")
print(f"📘 Subject : {subject}")
print("📸 Show QR | ESC to stop\n")

# ===================== MAIN LOOP =====================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    qr_data, _, _ = qr.detectAndDecode(
        frame
    )

    current_time = time.time()

    if qr_data and (
        current_time - last_scan_time
        > SCAN_DELAY
    ):

        last_scan_time = current_time

        # INVALID QR
        if qr_data not in STUDENTS:

            print(
                f"❌ INVALID QR : {qr_data}"
            )

            beep_block()

            continue

        student_id = qr_data

        name = STUDENTS[student_id]

        # NOT ENROLLED
        if not subject_allowed(
            student_id,
            subject
        ):

            print(
                f"❌ NOT ENROLLED : {name}"
            )

            beep_block()

            continue

        # DUPLICATE
        if already_marked(
            student_id,
            subject,
            today
        ):

            print(
                f"⚠ PRESENT REPEATED : {name}"
            )

            beep_block()

            continue

        # MARK ATTENDANCE
        with open(
            "attendance_log.csv",
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            if not file_exists:

                writer.writerow([
                    "StudentID",
                    "Name",
                    "Subject",
                    "Date",
                    "Time",
                    "Method"
                ])

                file_exists = True

            writer.writerow([
                student_id,
                name,
                subject,
                today,
                datetime.now().strftime(
                    "%H:%M:%S"
                ),
                "QR"
            ])

        print(
            f"✅ PRESENT : {name}"
        )

        beep_ok()

    cv2.imshow(
        "Smart Attendance - QR Mode",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()

print("\n🛑 Attendance Session Ended")

sys.exit(0)
