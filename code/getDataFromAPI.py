import os
import pickle

import requests
from requests.auth import HTTPBasicAuth

USERNAME = "3c032px-2enbodnmt-1oaxj1g-rtnobevj1l"
TOKEN = "-#YSqU4w=ZDo6Lv%bdzK_MP3aB,CPf"
API_VERSION = "v3"
BASE_URL = "https://apirest.wyscout.com/" + API_VERSION

CODE_FOLDER = os.getcwd()
DATA_FOLDER = os.getcwd().replace("code", "data")


def getDataFromAPI(url, obj, output_file):
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, TOKEN))
    if response.ok:
        result = response.json()[obj]
        pickle.dump(result, open(DATA_FOLDER + "\\" + output_file, "wb"))
        return result
    else:
        print(url, response.text)
        return {}


# Import Areas
areas = getDataFromAPI(BASE_URL + "/areas", "areas", "areas")
area_codes = ["ITA"]

# Import Competitions
for area in area_codes:
    competitions = getDataFromAPI(
        BASE_URL + "/competitions?areaId=" + area,
        "competitions",
        "competitions_" + area,
    )

    # Import Seasons
    for comp in competitions:
        seasons = getDataFromAPI(
            BASE_URL + "/competitions/" + str(comp["wyId"]) + "/seasons",
            "seasons",
            "seasons_" + comp["name"].replace(" ", "_"),
        )

        # Import Matches
        for season in seasons:
            matches = getDataFromAPI(
                BASE_URL + "/seasons/" + season["seasonId"] + "/matches",
                "matches",
                "matches_"
                + comp["name"].replace(" ", "_")
                + "_"
                + season["season"]["name"].replace("/", "_"),
            )

        # Import Players
        players = getDataFromAPI(
            BASE_URL + "/competitions/" + str(comp["wyId"]) + "/players",
            "players",
            "players_" + comp["name"].replace(" ", "_"),
        )
