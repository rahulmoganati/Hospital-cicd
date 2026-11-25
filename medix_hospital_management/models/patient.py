from extensions import db
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(30))
    address = db.Column(db.String(300))
    user = db.relationship("User", backref=db.backref("patient_profile", uselist=False))
