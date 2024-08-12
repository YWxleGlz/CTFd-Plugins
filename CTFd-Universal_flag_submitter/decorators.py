import functools
from CTFd.utils import get_config
from flask import abort
from flask import abort,  request
from CTFd.utils.user import (
    authed,
    get_current_team,
    get_current_user
)
from CTFd.utils import config, get_config
from CTFd.utils.logging import log

from CTFd.utils import user as current_user
from CTFd.utils.user import get_current_team, get_current_user
from CTFd.utils import config, get_config
from CTFd.utils.dates import ctf_paused, ctftime
from flask import  request



def is_allowed_to_attempt(f):
    """
    Decorator to check if the user is allowed to submit a flag.
    """

    @functools.wraps(f)
    def is_allowed_to_attempt_wrapper(*args, **kwargs):


        if authed() is False:
            return (
                    {"success": False, 
                        "message": "You must be logged in to access to this feature.", 
                        "design": "neutral"
                    },
                403,
            )

        if config.is_teams_mode() and get_current_team() is None:
            return (
                    {"success": False, 
                        "message": "Please create or join a team to submit flags.", 
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










