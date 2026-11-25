from flask import Blueprint, redirect, url_for
from flask_login import current_user
bp = Blueprint("main", __name__)
@bp.route("/")
def index():
    if not current_user.is_authenticated: return redirect(url_for("auth.login"))
    return redirect(url_for({"admin":"admin.dashboard","doctor":"doctor.dashboard","patient":"patient.dashboard"}[current_user.role]))
