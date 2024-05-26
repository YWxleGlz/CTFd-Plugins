import functools
from CTFd.utils import get_config
from flask import abort

import contextlib
import os
from flask import abort, redirect, render_template, request, url_for
from CTFd.utils.user import (
    authed,
    get_current_team,
    get_current_user
)
from CTFd.utils import config, get_config
from CTFd.utils.logging import log
from CTFd.models import db
from flask import Blueprint
from CTFd.utils.decorators import admins_only

from CTFd.models import Teams, Flags, db
from CTFd.models import (
    ChallengeFiles,
    Challenges,
    Fails,
    Flags,
    Hints,
    Solves,
    Tags,
    db,
)
from CTFd.utils.helpers import info_for, error_for
from CTFd.utils import user as current_user
from CTFd.utils.user import get_current_team, get_current_user
from CTFd.utils import config, get_config, set_config
from CTFd.utils.dates import ctf_ended, ctf_paused, ctftime
from CTFd.plugins.challenges import CHALLENGE_CLASSES, get_chal_class
from flask import render_template, Blueprint, request
from CTFd.utils.decorators import admins_only

from CTFd.utils.helpers import get_errors, get_infos
from .utils import add_fail, add_solves
from CTFd.cache import (
    cache,
    clear_challenges,
    clear_config,
    clear_pages,
    clear_standings,
)

def is_allowed_to_attempt(f):

    @functools.wraps(f)
    def is_allowed_to_attempt_wrapper(*args, **kwargs):


        if authed() is False:
            return (
                    {"success": False, 
                        "message": "Veuillez vous authentifier.", 
                        "design": "neutral"
                    },
                403,
            )



        if config.is_teams_mode() and get_current_team() is None:
            return (
                    {"success": False, 
                        "message": "veuillez d'abord rejoindre une équipe.", 
                        "design": "neutral"
                    },
                403,
            )

        if request.content_type != "application/json":
            abort(400)
        else:
            request_data = request.get_json()
            if request_data.get("submission") is None:
                abort(400)


        if ctf_paused() or ctftime() is False:
            return (
                    {"success": False, 
                        "message": "{} is paused".format(config.ctf_name()), 
                        "design": "neutral"
                        },
                403,
            )

        if is_bruteforcing(request_data):
            return ({"success": False, "message": "You're submitting flags too fast. Slow down.", "design": "neutral"}, 429)
        else:
            return f(*args, **kwargs)
    
    def is_bruteforcing(request):

        user = get_current_user()

        kpm = current_user.get_wrong_submissions_per_minute(user.account_id)
        kpm_limit = int(get_config("incorrect_submissions_per_min", default=10))
        if kpm > kpm_limit:

            log(
                "submissions",
                "[{date}] {name} submitted {submission} on UNIVERSAL-PAGE with kpm {kpm} [TOO FAST]",
                name=user.name,
                submission=request.get("submission", "").encode("utf-8"),
                
                kpm=kpm,
            )
            # Submitting too fast
            return True
            
        
        return False
            

    return is_allowed_to_attempt_wrapper










