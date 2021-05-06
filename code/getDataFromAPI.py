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
        if output_file is not None:
            pickle.dump(result, open(DATA_FOLDER + "\\" + output_file, "wb"))
        return result
    else:
        print(url, response.text)
        return {}


# Import Areas
url = BASE_URL + "/areas"
output_file = "areas"
areas = getDataFromAPI(url, "areas", output_file)
area_codes = ["ITA"]

# Import Competitions
for area in area_codes:
    url = BASE_URL + "/competitions?areaId=" + area
    output_file = "competitions_" + area
    competitions = getDataFromAPI(
        url,
        "competitions",
        output_file,
    )

    for comp in competitions:

        # Import Seasons
        url = BASE_URL + "/competitions/" + str(comp["wyId"]) + "/seasons"
        output_file = "seasons_" + comp["name"].replace(" ", "_")
        seasons = getDataFromAPI(
            url,
            "seasons",
            output_file,
        )

        # Import Players
        url = BASE_URL + "/competitions/" + str(comp["wyId"]) + "/players"
        output_file = "players_" + comp["name"].replace(" ", "_")
        players = getDataFromAPI(
            url,
            "players",
            output_file,
        )

        # Import Teams
        url = BASE_URL + "/competitions/" + str(comp["wyId"]) + "/teams"
        output_file = "teams_" + comp["name"].replace(" ", "_")
        matches = getDataFromAPI(
            url,
            "teams",
            output_file,
        )

        # Import Matches
        for season in seasons:
            url = BASE_URL + "/seasons/" + season["seasonId"] + "/matches"
            output_file = (
                "matches_"
                + comp["name"].replace(" ", "_")
                + "_"
                + season["season"]["name"].replace("/", "_")
            )
            matches = getDataFromAPI(
                url,
                "matches",
                output_file,
            )

            # Import Match Events
            events_dict = {}
            for match in matches:
                url = BASE_URL + "/matches/" + str(match["matchId"]) + "/events"
                events_dict[match["matchId"]] = getDataFromAPI(url, "events", None)
            output_file = (
                "events_"
                + comp["name"].replace(" ", "_")
                + "_"
                + season["season"]["name"].replace("/", "_")
            )
            pickle.dump(events_dict, open(DATA_FOLDER + "\\" + output_file, "wb"))
