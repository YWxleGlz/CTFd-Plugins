
import os
from flask import redirect, render_template, request, url_for, Blueprint
from flask import Blueprint
from CTFd.utils.decorators import admins_only
from .models import CheaterTeams
from CTFd.models import Challenges, Flags, db
from CTFd.utils.helpers import info_for, error_for
from .utils import importFlag
from CTFd.utils.helpers import get_errors, get_infos

plugin_blueprint = Blueprint("unique_flags", __name__, template_folder="templates")


@plugin_blueprint.route("/admin/unique-flag", methods=["GET", "POST"])
@admins_only
def home():
    infos = get_infos()
    errors = get_errors()

    if request.method == "GET":
        challenges = Challenges.query.all()
        return render_template('admin-import.html', infos=infos, errors=errors, challenges=challenges)


    if request.method == "POST":

        infos, errors = importFlag(request.form["content"])

        for info in infos:
            info_for("unique_flags.home", info)
        for error in errors:
            error_for("unique_flags.home", error)

        return redirect(url_for("unique_flags.home"))
 
 
@plugin_blueprint.route("/admin/unique-flag/delete-flags", methods=["POST"])
@admins_only
def delete_flags():
    if request.form.get('challenge_id') is None:
        count = Flags.query.filter_by(type="uniqueflag").delete()
    else: 
        count = Flags.query.filter_by(type="uniqueflag", challenge_id=request.form.get('challenge_id')).delete()
    
    db.session.commit()

    info_for("unique_flags.home", f"{count} occurrence(s) deleted")

    return redirect(url_for("unique_flags.home"))
 

@plugin_blueprint.route("/admin/unique-flag/cheating-monitor", methods=["GET"])
@admins_only
def view_cheater():
    return render_template('cheat-monitor.html', cheaters=CheaterTeams.query.all())
