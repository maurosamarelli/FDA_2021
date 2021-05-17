import os
import pickle
import pandas as pd

CODE_FOLDER = os.getcwd()
DATA_FOLDER = os.getcwd().replace("code", "data")

matchFormations = pickle.load(
    open(DATA_FOLDER + "/match_formations_Serie_A_2020_2021", "rb")
)
teams = pickle.load(open(DATA_FOLDER + "/teams_Serie_A_2020_2021", "rb"))


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


df_scheme = pd.merge(
    pd.DataFrame(teams)[["wyId", "name"]],
    getMainScheme(matchFormations),
    left_on="wyId",
    right_index=True,
)
df_scheme.columns = ["team_id", "team_name", "main_scheme"]
