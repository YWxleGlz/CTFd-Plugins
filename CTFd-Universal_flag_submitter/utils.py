from CTFd.models import (
    Fails,
    Solves,
    db,
)

from CTFd.cache import clear_challenges
from CTFd.utils.user import get_current_user

def add_submission(submission_type, challenge_id, request):
    """
    Generic function to add a submission to the database

    Args:
        submission_type (string): The type of submission to add
        challenge_id (int): The ID of the challenge
        request: The request object
    """

    # Récupérer l'utilisateur
    user = get_current_user()

    team = user.team.id if user.team else None
    # Créer l'objet de soumission en fonction du type
    submission_class = Fails if submission_type == 'fail' else Solves
    submission = submission_class(
        user_id=user.id,
        team_id=team,
        challenge_id=challenge_id,
        ip=request.remote_addr,
        provided=f"UNIVERSAL-{request.json['submission']}"
    )

    # Ajouter à la session et commit
    db.session.add(submission)
    db.session.commit()

    # Clear le cache pour afficher directement le challenge à l'utilisateur
    if submission_type == 'solve':
        clear_challenges()


def add_fail(challenge_id, request):
    add_submission('fail', challenge_id, request)

def add_solves( challenge_id, request):
    add_submission('solve', challenge_id, request)

