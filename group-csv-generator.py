#!/usr/bin/python3
import random, string, csv


GROUPS = ["A", "B", "C"]
TEAMS_PER_GROUP = 12

def random_string(length=6):
    """Generate a random password of lowercase letters.

    Args:
        length (int, optional): The length of the random string. Defaults to 6.

    Returns:
        str: A random string of lowercase letters.
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Generate team names and password for groups A, B, and C

with open('teams.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["name", "password"]
    writer.writerow(field)  # Add this line to write the column names

    for group in GROUPS:
        for i in range(1,TEAMS_PER_GROUP+1):
            writer.writerow([f"Team-{group}-{i:02}", random_string()])