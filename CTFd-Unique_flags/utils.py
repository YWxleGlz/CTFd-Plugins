import csv, io

import sqlalchemy
from CTFd.models import Teams
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.models import Teams, Flags, db

def getTeamID(classe, groupe):
    """
    Get the ID of a team from its class and group

    Args:
        classe (string)
        groupe (string)

    Returns:
        int: The ID of the team
    """
    team_name = f"Team-{classe.upper()}-{int(groupe):02}"
    result =  Teams.query.filter_by(name=team_name).first()
    return "Error" if result is None else result.id


def importFlag(csv_content):
    """
    Import flags from a CSV file into the database

    Args:
        csv_content (string): The content of the CSV file (Check assets/example.csv) to see the format

    Returns:
        A list of infos and a list of errors
    """
    infos = get_infos()
    errors = get_errors()

    csvfile = io.StringIO(csv_content)
    csvreader = csv.DictReader(csvfile, delimiter=";")

    if 'CLASS' not in csvreader.fieldnames or 'GROUP' not in csvreader.fieldnames or 'FLAG' not in csvreader.fieldnames or 'CHALLENGE_ID' not in csvreader.fieldnames:
        errors.append("You need at least the columns 'CLASS', 'GROUP', 'FLAG', 'CHALLENGE_ID'.")
        return infos, errors
    
    previous_team = "" # This variable is used to avoid multiple queries to the database

    flags = []
    for row in csvreader:
        if previous_team != str(row['CLASS'])+str(row['GROUP']):
            previous_team = str(row['CLASS'])+str(row['GROUP'])
            teamid = getTeamID(row['CLASS'], row['GROUP'])
            if id == "Error":
                errors.append(f"There's a problem with the {row} line, the team is not found in CTFd")


        flags.append(Flags(challenge_id=row['CHALLENGE_ID'], type="uniqueflag", content=row["FLAG"], data=teamid))



    try:
        s = db.session()
        s.bulk_save_objects(flags)
        s.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        db.session.rollback()
        errors.append("Foreign key error: FOREIGN KEY constraint failed, Make sure challenges exist")
    except Exception as e:
        print(e)
        db.session.rollback()
        errors.append("Unknown error during import, check logs")

    if len(errors) == 0:
        infos.append("Import success")
    return infos, errors




