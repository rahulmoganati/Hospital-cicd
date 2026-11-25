from extensions import db
from models import Appointment
def book(patient_id, doctor_id, when, reason):
    conflict = Appointment.query.filter_by(doctor_id=doctor_id, appointment_at=when).filter(Appointment.status.in_(["Pending","Confirmed"])).first()
    if conflict: raise ValueError("That doctor already has an appointment at this time.")
    item = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_at=when, reason=reason, status="Pending")
    db.session.add(item); db.session.commit()
    return item
def set_status(item, status):
    if status not in {"Confirmed","Rejected","Completed","Cancelled"}: raise ValueError("Invalid status.")
    item.status = status; db.session.commit()
