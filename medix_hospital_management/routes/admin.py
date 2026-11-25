from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import User, Doctor, Patient, Department, Appointment
from utils.decorators import roles_required
bp = Blueprint("admin", __name__)
@bp.route("/")
@roles_required("admin")
def dashboard():
    return render_template("admin/dashboard.html", doctors=Doctor.query.count(), patients=Patient.query.count(), appointments=Appointment.query.order_by(Appointment.appointment_at.desc()).limit(10).all())
@bp.route("/doctors", methods=["GET","POST"])
@roles_required("admin")
def doctors_page():
    if request.method == "POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); password=request.form.get("password",""); spec=request.form.get("specialization","").strip()
        if not name or not email or len(password)<10 or not spec: flash("Complete all fields; password needs 10 characters.","danger")
        elif User.query.filter_by(email=email).first(): flash("Email already exists.","danger")
        else:
            user=User(full_name=name,email=email,role="doctor"); user.set_password(password); db.session.add(user); db.session.flush()
            db.session.add(Doctor(user_id=user.id,specialization=spec)); db.session.commit(); flash("Doctor created.","success")
        return redirect(url_for("admin.doctors_page"))
    return render_template("admin/doctors.html", items=Doctor.query.all())
@bp.route("/patients")
@roles_required("admin")
def patients_page(): return render_template("admin/patients.html", items=Patient.query.all())
@bp.route("/appointments")
@roles_required("admin")
def appointments_page(): return render_template("admin/appointments.html", items=Appointment.query.order_by(Appointment.appointment_at.desc()).all())
@bp.route("/departments", methods=["GET","POST"])
@roles_required("admin")
def departments_page():
    if request.method=="POST":
        name=request.form.get("name","").strip()
        if name and not Department.query.filter_by(name=name).first(): db.session.add(Department(name=name)); db.session.commit(); flash("Department added.","success")
        else: flash("Enter a unique name.","warning")
        return redirect(url_for("admin.departments_page"))
    return render_template("admin/departments.html", items=Department.query.all())
