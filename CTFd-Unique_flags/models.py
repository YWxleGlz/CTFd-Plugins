# Code from https://github.com/Isotech42/CTFd-RedHerring/blob/main/models.py
from CTFd.models import db, Teams, Challenges, Flags, Users

from CTFd.models import db, Challenges

class CheaterTeams(db.Model):
    """
    Model for the cheater_teams table

    Columns:
        id (int): The ID of the record
        challengeid (int): The ID of the challenge
        cheaterid (int): The ID of the cheater
        cheatteamid (int): The ID of the team that maybe cheated
        sharerteamid (int): The ID of the team that shared the flag
        flagid (int): The ID of the flag
        date (datetime): The date of the record creation
    """

    __tablename__ = 'cheater_teams'

    id = db.Column(db.Integer, primary_key=True)
    challengeid = db.Column(db.Integer, db.ForeignKey('challenges.id', ondelete="CASCADE"))
    cheaterid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    cheatteamid = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete="CASCADE"))
    sharerteamid = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete="CASCADE"))
    flagid = db.Column(db.Integer, db.ForeignKey('flags.id', ondelete="CASCADE"))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, challengeid, cheaterid, cheatteamid, sharerteamid, flagid):
        """ Initializes the CheaterTeams object
        Args:
            challengeid (int): The ID of the challenge
            cheaterid (int): The ID of the cheater
            cheatteamid (int): The ID of the team that maybe cheated
            sharerteamid (int): The ID of the team that shared the flag
            flagid (int): The ID of the flag
        """
        self.challengeid = challengeid
        self.cheaterid = cheaterid
        self.cheatteamid = cheatteamid
        self.sharerteamid = sharerteamid
        self.flagid = flagid

    def __repr__(self):
        """ 
        Returns the string representation of the CheaterTeams object
        """
        return "<CheaterTeams Team {0} maybe cheated for challenge {1} with the flag {2} belonging to the team {3} at {4} >".format(self.cheatteamid, self.challengeid, self.flagid, self.sharerteamid, self.date)
    
    def cheated_team_name(self):
        """ 
        Get the name of the team that maybe cheated
        """
        return Teams.query.filter_by(id=self.cheatteamid).first().name

    def shared_team_name(self):
        """
        Get the name of the team that shared the flag
        """
        return Teams.query.filter_by(id=self.sharerteamid).first().name

    def challenge_name(self):
        """
        Get the name of the challenge
        """
        return Challenges.query.filter_by(id=self.challengeid).first().name
    
    def cheater_name(self):
        """
        Get the name of the cheater
        """
        return Users.query.filter_by(id=self.cheaterid).first().email