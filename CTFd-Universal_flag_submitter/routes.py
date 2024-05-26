
import os

import sqlalchemy

from CTFd.cache import clear_challenges
from CTFd.models import (
    Challenges,
    Solves,
    db,
)
import copy
from flask import Blueprint, redirect, render_template, request, url_for
from CTFd.plugins.challenges import get_chal_class
from CTFd.utils.decorators import admins_only
from CTFd.utils.helpers import error_for, get_errors, get_infos, info_for
from CTFd.utils.user import get_current_user
from .decorators import is_allowed_to_attempt
from .utils import add_fail, add_solves


plugin_blueprint = Blueprint("universal_flag_submitter", __name__, template_folder="templates")


@plugin_blueprint.route("/attempt-hidden-challenge", methods=["POST"])
@is_allowed_to_attempt
def attempt_hidden_challenge():

    chall = db.session.query(Challenges).filter(Challenges.state == "visible").all()
    for challenge in chall:
        chal_class = get_chal_class(challenge.type)
        status, message = chal_class.attempt(challenge, request)

        user = get_current_user()
        
        if status:
            # check if the Solves is already in the database
            alreadySolve = db.session.query(Solves).filter_by(challenge_id=challenge.id, user_id=user.id).first()
            if alreadySolve:
                return {"success": False, "message": "You already solved this challenge.", "design": "neutral"}

            add_solves(challenge.id, request)

            return {"success": status, "message": message, "challenge" : {"id": challenge.id,
                                            "name": challenge.name, 
                                            "category": challenge.category}, "design": "success"}


    add_fail(chall[0].id, request)

    return {"success": status, "message": message, "design": "danger"}


@plugin_blueprint.route("/admin/hide-challenge", methods=["GET", "POST"])
@admins_only
def home():

    if request.method == "GET":
        infos = get_infos()
        errors = get_errors()
        challenges_view = []
        for challenge in Challenges.query.filter_by(state="visible").all():

            checked = bool(
                challenge.requirements is not None
                and "prerequisites" in challenge.requirements
                and challenge.id in challenge.requirements["prerequisites"]
            )

            challenges_view.append({
                "id": challenge.id,
                "name": challenge.name,
                "category": challenge.category,
                "state": challenge.state,
                "checked": checked
            })

        return render_template('admin-challenge-hide.html', infos=infos, errors=errors, challenges=challenges_view)

    if request.method == "POST":

        challenges = Challenges.query.filter_by(state="visible").all()
        for challenge in challenges:

            challenge.requirements = sqlalchemy.sql.null()

            db.session.commit()
            print(f"Removed prerequisites from challenge ID {challenge.id}")


        for challenge in request.form.getlist("challenges"):
            challenge = Challenges.query.filter_by(id=challenge).first()
            requirements = {"prerequisites" : [int(challenge.id)]}
            
            challenge.requirements = copy.deepcopy(requirements)
            db.session.commit()
        
        clear_challenges()
        info_for("universal_flag_submitter.home", "Saved changes")


        return redirect(url_for("universal_flag_submitter.home"))
