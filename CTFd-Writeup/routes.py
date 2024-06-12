
from flask import render_template, Blueprint, request, redirect, url_for, session
from CTFd.models import Solves, Challenges, db
from CTFd.utils.decorators import admins_only
from .models import WriteupModel
from CTFd.utils.user import  get_current_team, get_current_user_attrs
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.utils.helpers import info_for, error_for
from .decorators import plugin_enabled
from CTFd.utils import config, get_config, set_config
from CTFd.utils.decorators import authed_only

plugin_blueprint = Blueprint('writeup', __name__, template_folder='templates')

@plugin_blueprint.route("/writeup/<int:challenge_id>", methods=["GET"])
@plugin_enabled
@authed_only
def view_writeup(challenge_id):
    if challenge_is_unlocked(challenge_id):
        return render_template('custom-page.html', content=get_writeup(challenge_id))
    else:
        return render_template('error.html')

@plugin_blueprint.route("/admin/writeup", methods=["GET"])
@admins_only
def view_admin_writeup():
    infos = get_infos()
    errors = get_errors()

    if not get_config("plugin_writeup_enabled"):
        errors.append("Please note that the plugin is currently disabled.")

    return render_template('writeup_config.html', challenges=get_all_challenges(), infos=infos, errors=errors, config=get_config("plugin_writeup_enabled"))

@plugin_blueprint.route("/admin/writeup", methods=["POST"])
@admins_only
def admin_update_config():
    infos = get_infos()
    errors = get_errors()

    if request.form.get("plugin_enabled") == "on":
        set_config("plugin_writeup_enabled", True)
        infos.append("Plugin enabled, server restart required for changes to take effect.")
    else:
        set_config("plugin_writeup_enabled", False)
        infos.append("Plugin disabled, a server restart is required for changes to take effect.")

    return render_template('writeup_config.html', challenges=get_all_challenges(), infos=infos, errors=errors, config=get_config("plugin_writeup_enabled"))


@plugin_blueprint.route("/admin/writeup/edit/<int:challenge_id>", methods=["GET", "POST"])
@admins_only
def edit_writeup(challenge_id):
    if request.method == "GET":
        writeup = WriteupModel.query.filter_by(id=challenge_id).first()
        challenge = get_challenge_by_id(challenge_id)

        return render_template('writeup_editor.html', challenge_info=challenge, writeup=writeup)

    if request.method == "POST":

        try: 
            writeup = WriteupModel.query.filter_by(id=challenge_id).first()

            # Create new writeup model instance if it doesn't exist
            if not writeup:
                writeup = WriteupModel(challenge_id, request.form["description"], True)
            else:
                writeup.content = request.form["description"]

            db.session.add(writeup)
            db.session.commit()

            info_for(
                "writeup.view_admin_writeup",
                f"Successfully updated writeup for challenge {challenge_id}.",
            )
            return redirect(url_for('writeup.view_admin_writeup'))

        except Exception as e:
            print(e)

            error_for(
                "writeup.view_admin_writeup",
                f"Failed to update writeup for challenge {challenge_id}.",
            )

            return redirect(url_for('writeup.view_admin_writeup'))

@plugin_blueprint.route("/admin/writeup/delete/<int:challenge_id>", methods=["POST"])
@admins_only
def delete_writeup(challenge_id):
    writeup = WriteupModel.query.filter_by(id=challenge_id).first_or_404()
    db.session.delete(writeup)
    db.session.commit()

    info_for(
        "writeup.view_admin_writeup",
        f"Successfully deleted writeup for challenge {challenge_id}.",
    )

    return {"success": True}


@plugin_blueprint.route("/admin/writeup/visibility/<int:challenge_id>", methods=["PUT"])
@admins_only
def toogle_writeup_visibility(challenge_id):
    
    writeup = WriteupModel.query.filter_by(id=challenge_id).first_or_404()
    writeup.visible = not writeup.visible

    db.session.commit()

    info_for(
        "writeup.view_admin_writeup",
        f"Challenge {writeup.challenge.name} ({writeup.id}) is now {'visible' if writeup.visible else 'hidden'}",
    )

    return {"success": True}



def challenge_is_unlocked(challenge_id):
    user = get_current_user_attrs()
    team = get_current_team()

    if config.is_teams_mode() and team is not None:
        return db.session.query(Solves).filter(Solves.team_id == user.team_id, Solves.challenge_id == challenge_id).count()
    else:
        return db.session.query(Solves).filter(Solves.user_id == user.id, Solves.challenge_id == challenge_id).count()

def get_writeup(challenge_id):
    return db.session.query(Challenges, WriteupModel).outerjoin(WriteupModel, Challenges.id == WriteupModel.id).filter(Challenges.id == challenge_id, Challenges.state == "visible").first()

def get_all_challenges():
    return Challenges.query.all()

def get_challenge_by_id(challenge_id):
    return Challenges.query.filter_by(id=challenge_id).first_or_404()
