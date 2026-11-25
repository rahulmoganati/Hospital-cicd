from extensions import db
class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    specialization = db.Column(db.String(120), nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    user = db.relationship("User", backref=db.backref("doctor_profile", uselist=False))
    department = db.relationship("Department")
