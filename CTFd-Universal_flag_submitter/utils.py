from CTFd.models import (
    Fails,
    Solves,
    db,
)

from CTFd.cache import clear_challenges
from CTFd.utils.user import get_current_user

def add_submission(submission_type, challenge_id, request):
    """
    Générique pour ajouter une soumission de fail ou solve.
    submission_type: 'fail' ou 'solve' pour déterminer le type de soumission.
    challenge_id: ID du challenge concerné.
    request: objet de requête Flask. 
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

