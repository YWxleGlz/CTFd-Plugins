import os
from CTFd.models import db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.migrations import upgrade
from CTFd.plugins.flags import CTFdStaticFlag, FLAG_CLASSES
from CTFd.utils.user import get_current_team, get_current_user
from .routes import plugin_blueprint
from .models import CheaterTeams

directory_name = os.path.dirname(__file__).split(os.sep)[-1] # Get the directory name of this file

class UniqueFlag(CTFdStaticFlag):

    name = "uniqueflag"
    templates = {  # Nunjucks templates used for key editing & viewing
        "create": f"/plugins/{directory_name}/assets/unique/create.html",
        "update": f"/plugins/{directory_name}/assets/unique/edit.html",
    }

    @staticmethod
    def compare(chal_key_obj, provided_flag):
        """
        Compare the provided flag to the saved flag

        Args:
            chal_key_obj: A CTFd.models.Flags object
            provided_flag: A string provided by the user


        Returns:
            bool: Whether or not the provided flag is correct
        """
        # Get the actual flag to check for the challenge submitted (the function compare() is called for each flag of the challenge)

        saved_flag = chal_key_obj.content
        curr_team_id = get_current_team().id

        if len(saved_flag) != len(provided_flag):
            return False

        result = 0

        for x, y in zip(saved_flag, provided_flag):
            result |= ord(x) ^ ord(y)

        if result != 0:
            return False
        
        # Check if the team id of the player is the same as the team id of the flag data
        # True = the flag is correct and the player is in the right team
        # False = the flag is correct but the player is not in the right team
        team_id = chal_key_obj.data
        if int(team_id) == int(curr_team_id):
            return True
        
        # The player is not in the right team, so we add the record in the cheater_teams table
        curr_user_id = get_current_user().id
        cheater = CheaterTeams(challengeid=chal_key_obj.challenge_id, cheaterid=curr_user_id, cheatteamid=curr_team_id, sharerteamid=team_id, flagid=chal_key_obj.id)
        db.session.add(cheater)
        return False



def load(app):
    """ 
    Load the plugin into CTFd
    Creates the database table and registers the blueprint
    """
    app.db.create_all()
    app.register_blueprint(plugin_blueprint)


    upgrade(plugin_name="unique_flags")
    FLAG_CLASSES['uniqueflag'] = UniqueFlag
    register_plugin_assets_directory(
        app, base_path=f"/plugins/{directory_name}/assets/"
    )
