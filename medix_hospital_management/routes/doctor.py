from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import Doctor, Appointment
from utils.decorators import roles_required
from services.appointment_service import set_status
bp=Blueprint("doctor",__name__)
@bp.route("/")
@roles_required("doctor")
def dashboard():
    profile=Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    return render_template("doctor/dashboard.html", profile=profile, items=Appointment.query.filter_by(doctor_id=profile.id).order_by(Appointment.appointment_at).all())
@bp.route("/appointments/<int:item_id>/status",methods=["POST"])
@roles_required("doctor")
def update_status(item_id):
    profile=Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    item=Appointment.query.filter_by(id=item_id,doctor_id=profile.id).first_or_404()
    try: set_status(item,request.form.get("status","")); flash("Status updated.","success")
    except ValueError as e: flash(str(e),"danger")
    return redirect(url_for("doctor.dashboard"))
