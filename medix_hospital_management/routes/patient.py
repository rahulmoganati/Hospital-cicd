from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import Patient, Doctor, User, Appointment
from utils.decorators import roles_required
from utils.validators import parse_future_datetime
from services.appointment_service import book
bp=Blueprint("patient",__name__)
@bp.route("/")
@roles_required("patient")
def dashboard():
    profile=Patient.query.filter_by(user_id=current_user.id).first_or_404()
    doctors=Doctor.query.join(User).filter(User.is_active.is_(True)).all()
    items=Appointment.query.filter_by(patient_id=profile.id).order_by(Appointment.appointment_at.desc()).all()
    return render_template("patient/dashboard.html",doctors=doctors,items=items)
@bp.route("/book",methods=["POST"])
@roles_required("patient")
def book_page():
    profile=Patient.query.filter_by(user_id=current_user.id).first_or_404()
    try:
        doctor_id=int(request.form.get("doctor_id","")); doctor=Doctor.query.filter_by(id=doctor_id).first_or_404()
        when=parse_future_datetime(request.form.get("appointment_at")); reason=request.form.get("reason","").strip()
        if not reason: raise ValueError("Enter reason for visit.")
        book(profile.id,doctor.id,when,reason); flash("Appointment request submitted.","success")
    except (ValueError,TypeError) as e: flash(str(e),"danger")
    return redirect(url_for("patient.dashboard"))
