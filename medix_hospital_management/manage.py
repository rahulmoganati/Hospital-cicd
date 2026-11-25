import click
from app import create_app
from extensions import db
from models import User, Doctor, Patient, Department
app=create_app()
@app.cli.command("init-db")
def init_db():
    with app.app_context(): db.create_all()
    click.echo("Tables created.")
@app.cli.command("create-admin")
@click.option("--name",prompt="Admin name")
@click.option("--email",prompt="Admin email")
@click.password_option()
def create_admin(name,email,password):
    with app.app_context():
        if User.query.filter_by(email=email.lower()).first(): raise click.ClickException("Email exists.")
        u=User(full_name=name,email=email.lower(),role="admin"); u.set_password(password); db.session.add(u); db.session.commit()
    click.echo("Admin created.")
@app.cli.command("create-demo-users")
def create_demo_users():
    with app.app_context():
        dept=Department.query.filter_by(name="Cardiology").first()
        if not dept: dept=Department(name="Cardiology"); db.session.add(dept); db.session.flush()
        for name,email,password,role in [("Demo Doctor","doctor@medix.local","DoctorDemo123!","doctor"),("Demo Patient","patient@medix.local","PatientDemo123!","patient")]:
            if User.query.filter_by(email=email).first(): continue
            u=User(full_name=name,email=email,role=role); u.set_password(password); db.session.add(u); db.session.flush()
            if role=="doctor": db.session.add(Doctor(user_id=u.id,department_id=dept.id,specialization="Cardiology"))
            else: db.session.add(Patient(user_id=u.id))
        db.session.commit()
    click.echo("Demo users created if missing.")
