# Medix Hospital Management – AWS Two Tier

## Project structure
- `app/`: Flask application factory.
- `models/`: SQLAlchemy database models.
- `routes/`: authentication, admin, doctor and patient routes.
- `services/`: appointment business logic.
- `utils/`: role authorization and validation.
- `templates/`: Jinja HTML pages.
- `static/`: CSS and JavaScript.
- `database/`: SQL reference.
- `deployment/`: Nginx and systemd examples.

## Local setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit DATABASE_URL and SECRET_KEY in .env
```
Create the MySQL database and user using a MySQL admin account:
```sql
CREATE DATABASE medix_hospital CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'medix_user'@'%' IDENTIFIED BY 'REPLACE_WITH_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON medix_hospital.* TO 'medix_user'@'%';
FLUSH PRIVILEGES;
```
Then:
```bash
export FLASK_APP=manage.py
flask init-db
flask create-admin
flask create-demo-users
flask --app app run
```
Demo doctor: `doctor@medix.local` / `DoctorDemo123!`
Demo patient: `patient@medix.local` / `PatientDemo123!`
Create admin using the interactive command; the admin demo card intentionally does not contain a default password.

## AWS network plan
VPC `10.0.0.0/16`
- Public application subnet `10.0.1.0/24`
- Private DB subnet A `10.0.2.0/24`
- Private DB subnet B `10.0.3.0/24` in a second AZ
- Public route `0.0.0.0/0` to Internet Gateway.
- RDS DB subnet group includes both private subnets; RDS public access disabled.
- EC2 security group: SSH 22 from your IP or use SSM; HTTP 80 for demo; HTTPS 443 after TLS.
- RDS security group: TCP 3306 source is the EC2 security group only.
RDS subnet groups require subnets in at least two AZs, even for Single-AZ RDS.

## EC2 deployment outline
Install Python venv, pip and Nginx; copy project to `/opt/medix`; create a dedicated `medix` service user; create `/opt/medix/venv`; install requirements; configure `/opt/medix/.env`; install the supplied systemd and Nginx files; enable services. Configure RDS connectivity before running `flask init-db`.

## Important
This is a learning prototype, not production healthcare software. Add production-grade audit logs, MFA, account recovery, secure cookies behind HTTPS, database migrations, backups and restore testing, transactional appointment-slot constraints, privacy controls and compliance review before real patient data is used. Use synthetic data only.
