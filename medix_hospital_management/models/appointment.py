from datetime import datetime
from extensions import db
class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    appointment_at = db.Column(db.DateTime, nullable=False, index=True)
    reason = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    patient = db.relationship("Patient", backref="appointments")
    doctor = db.relationship("Doctor", backref="appointments")
