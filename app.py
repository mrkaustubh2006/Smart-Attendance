
from flask import Flask, render_template, request, jsonify
import pandas as pd
import csv
import qrcode
from datetime import datetime
import os

app = Flask(__name__)

# ================= DASHBOARD =================

@app.route("/")
@app.route("/dashboard")
def dashboard():

    total_students = 0

    if os.path.exists("students.csv"):
        try:
            df = pd.read_csv("students.csv")
            total_students = len(df)
        except:
            total_students = 0

    return render_template(
        "dashboard.html",
        total_students=total_students
    )

# ================= QR SCANNER PAGE =================

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    qr_image = None
    student_id = None

    if request.method == "POST":

        name = request.form["name"]
        student_class = request.form["student_class"]
        roll_no = request.form["roll_no"]
        subjects = request.form["subjects"]

        if os.path.exists("students.csv"):
            df = pd.read_csv("students.csv")
        else:
            df = pd.DataFrame(
                columns=[
                    "StudentID",
                    "Name",
                    "Class",
                    "RollNo",
                    "Subjects"
                ]
            )

        student_id = f"STD{len(df)+1:03d}"

        new_row = pd.DataFrame([{
            "StudentID": student_id,
            "Name": name,
            "Class": student_class,
            "RollNo": roll_no,
            "Subjects": subjects
        }])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_csv(
            "students.csv",
            index=False
        )

        # CREATE QR
        os.makedirs(
            "static/qr_codes",
            exist_ok=True
        )

        qr = qrcode.make(student_id)

        qr_path = (
            f"static/qr_codes/{student_id}.png"
        )

        qr.save(qr_path)

        qr_image = (
            f"qr_codes/{student_id}.png"
        )

        return render_template(
            "register_student.html",
            student_id=student_id,
            qr_image=qr_image
        )

    return render_template(
        "register_student.html",
        student_id=None,
        qr_image=None
    )



# ================= STUDENTS =================

@app.route("/students")
def students():

    students = []

    if os.path.exists("students.csv"):
        try:
            df = pd.read_csv("students.csv")
            students = df.to_dict(
                orient="records"
            )
        except:
            pass

    return render_template(
        "students.html",
        students=students
    )


# ================= ATTENDANCE LOG =================

@app.route("/attendance")
def attendance():

    attendance = []

    if os.path.exists("attendance_log.csv"):
        try:
            df = pd.read_csv(
                "attendance_log.csv"
            )

            attendance = df.to_dict(
                orient="records"
            )

        except:
            pass

    return render_template(
        "attendance.html",
        attendance=attendance
    )


# ================= REPORT =================

@app.route("/report")
def report():

    total_students = 0
    total_attendance = 0

    if os.path.exists("students.csv"):
        try:
            total_students = len(
                pd.read_csv("students.csv")
            )
        except:
            pass

    if os.path.exists("attendance_log.csv"):
        try:
            total_attendance = len(
                pd.read_csv(
                    "attendance_log.csv"
                )
            )
        except:
            pass

    return render_template(
        "report.html",
        total_students=total_students,
        total_attendance=total_attendance
    )


# ================= ATTENDANCE API =================

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        })

    student_id = str(
        data.get("student_id", "")
    ).strip()

    if student_id == "":
        return jsonify({
            "success": False,
            "message": "Invalid QR"
        })

    if not os.path.exists("students.csv"):
        return jsonify({
            "success": False,
            "message": "students.csv not found"
        })

    students = pd.read_csv("students.csv")

    students.columns = students.columns.str.strip()

    if "StudentID" not in students.columns:
        return jsonify({
            "success": False,
            "message": "StudentID column missing"
        })

    if "Name" not in students.columns:
        return jsonify({
            "success": False,
            "message": "Name column missing"
        })

    student = students[
        students["StudentID"].astype(str).str.strip() == student_id
    ]

    if student.empty:
        return jsonify({
            "success": False,
            "message": "Student not registered"
        })

    name = student.iloc[0]["Name"]

    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists("attendance_log.csv"):

        attendance = pd.read_csv("attendance_log.csv")

        if not attendance.empty:

            duplicate = attendance[
                (attendance["StudentID"].astype(str) == student_id)
                &
                (attendance["Date"].astype(str) == today)
            ]

            if not duplicate.empty:
                return jsonify({
                    "success": False,
                    "message": "Attendance already marked today"
                })

    file_exists = os.path.exists("attendance_log.csv")

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
                "Date",
                "Time",
                "Method"
            ])

        writer.writerow([
            student_id,
            name,
            today,
            datetime.now().strftime("%H:%M:%S"),
            "QR"
        ])

    return jsonify({
        "success": True,
        "message": f"Attendance Marked : {name}"
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
