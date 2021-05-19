import os
import pickle
import numpy as np
import pandas as pd
from datetime import date

CODE_FOLDER = os.getcwd()
DATA_FOLDER = os.getcwd().replace("code", "data")

matchFormations = pickle.load(
    open(DATA_FOLDER + "/match_formations_Serie_A_2020_2021", "rb")
)
teams = pickle.load(open(DATA_FOLDER + "/teams_Serie_A_2020_2021", "rb"))
players = pickle.load(open(DATA_FOLDER + "/players_Serie_A_2020_2021", "rb"))
contractinfo = pickle.load(open(DATA_FOLDER + "/players_contractinfo_Serie_A_2020_2021", "rb"))

ROLES = {
    "gk": "Goalkeeper",
    "rb": "Right Back",
    "rcb": "Right Centre Back",
    "lcb": "Left Centre Back",
    "lb": "Left Back",
    "rw": "Right Winger",
    "rcmf": "Right Centre Midfielder",
    "lcmf": "Left Centre Midfielder",
    "lw": "Left Winger",
    "ss": "Second Striker",
    "cf": "Striker",
    "amf": "Attacking Midfielder",
    "rcmf3": "Right Centre Midfielder",
    "dmf": "Defensive Midfielder",
    "lcmf3": "Left Centre Midfielder",
    "rdmf": "Right Defensive Midfielder",
    "ldmf": "Left Defensive Midfielder",
    "ramf": "Right Attacking Midfielder",
    "lamf": "Left Attacking Midfielder",
    "rwf": "Right Wing Forward",
    "lwf": "Left Wing Forward",
    "rcb3": "Right Centre Back (3 at the back)",
    "cb": "Centre Back",
    "lcb3": "Left Centre Back (3 at the back)",
    "rwb": "Right Wingback",
    "lwb": "Left Wingback",
    "rb5": "Right Back (5 at the back)",
    "lb5": "Left Back (5 at the back)",
}

def getAge(birth_date):
    yyyy, mm, dd = int(birth_date[:4]), int(birth_date[5:7]), int(birth_date[-2:])
    delta = date.today() - date(yyyy, mm, dd)
    age = int(delta.days / 365)
    return age

def getMainScheme(matchFormations):
    formationsDict = {}
    for match in matchFormations.keys():
        for team in matchFormations[match].keys():
            team_id = int(team)
            if team_id not in formationsDict.keys():
                formationsDict[team_id] = {}
            for period in matchFormations[match][team].keys():
                for idx in matchFormations[match][team][period].keys():
                    for scheme in matchFormations[match][team][period][idx].keys():
                        start = matchFormations[match][team][period][idx][scheme][
                            "startSec"
                        ]
                        end = matchFormations[match][team][period][idx][scheme][
                            "endSec"
                        ]
                        if scheme not in formationsDict[team_id].keys():
                            formationsDict[team_id][scheme] = end - start
                        else:
                            formationsDict[team_id][scheme] += end - start
    return pd.DataFrame(pd.DataFrame(formationsDict).idxmax())


def getMainRole(matchFormations):
    rolesDict = {}
    for match in matchFormations.keys():
        for team in matchFormations[match].keys():
            for period in matchFormations[match][team].keys():
                for idx in matchFormations[match][team][period].keys():
                    for scheme in matchFormations[match][team][period][idx].keys():
                        start = matchFormations[match][team][period][idx][scheme][
                            "startSec"
                        ]
                        end = matchFormations[match][team][period][idx][scheme][
                            "endSec"
                        ]
                        for player in matchFormations[match][team][period][idx][scheme][
                            "players"
                        ]:
                            player_id = list(player.values())[0]["playerId"]
                            player_role = list(player.values())[0]["position"]
                            if player_id not in rolesDict.keys():
                                rolesDict[player_id] = {}
                            if player_role not in rolesDict[player_id].keys():
                                rolesDict[player_id][player_role] = end - start
                            else:
                                rolesDict[player_id][player_role] += end - start
    return pd.DataFrame(pd.DataFrame(rolesDict).idxmax())


df_scheme = pd.merge(
    pd.DataFrame(teams)[["wyId", "name"]],
    getMainScheme(matchFormations),
    left_on="wyId",
    right_index=True,
)
df_scheme.columns = ["team_id", "team_name", "main_scheme"]

df_roles = pd.merge(
    pd.DataFrame(players)[["wyId", "shortName", "currentTeamId", "height", "weight", "birthDate", "birthArea", "passportArea", "foot"]],
    getMainRole(matchFormations),
    left_on="wyId",
    right_index=True,
    how="left"
)
df_roles.columns = ["player_id", "player_name", "team_id", "height", "weight", "age", "birth_area", "passport_area", "foot", "main_role"]
df_roles["age"] = df_roles.age.apply(lambda x: getAge(x))
df_roles["birth_area"] = df_roles.birth_area.apply(lambda x: x["name"])
df_roles["passport_area"] = df_roles.passport_area.apply(lambda x: x["name"])
df_roles["main_role"] = df_roles.main_role.apply(lambda x: ROLES[x] if x == x else np.nan)

df = pd.merge(
    pd.merge(df_scheme,
    df_roles,
    left_on="team_id",
    right_on="team_id",
    how="right"),
    pd.DataFrame(contractinfo).transpose()[["contractExpiration"]],
    left_on="player_id",
    right_index=True,
    how="left"
)
df["contractExpiration"] = df.contractExpiration.apply(lambda x: int(x[:4]) if x is not None and x == x else np.nan)

pickle.dump(df, open(DATA_FOLDER + "/preprocessing_dataset", "wb"))