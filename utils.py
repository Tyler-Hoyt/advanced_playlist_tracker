import json
import os
import re


def get_playlist_names(directory):
    playlist_names = []
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            if is_playlist_file(os.path.join(directory, entry)):
                playlist_names.append(entry)
    return playlist_names


# TODO: Need to add more checks here
def is_playlist_file(file_path):
    if file_path.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if 'scenarioList' in data:
                return True
    return False


def get_scenario_list(directory_path, playlist_name):
    with open(f"{directory_path}/{playlist_name}", "r") as file:
        data = json.load(file)
        return data['scenarioList']


def get_scenario_scores(scores_path, settings_path, scenario_name):
    cur_sens = 0.0

    with open(settings_path, "r") as settings_file:
        data = json.load(settings_file)
        cur_sens = data["floatSettings"]["EFloatSettingId::XSens"]

    highscore_files = {}
    for dirpath, dirnames, filenames in os.walk(scores_path):
        for file in filenames:
            if file.split('-')[0].rstrip() == scenario_name:
                with open(f"{scores_path}/{file}", newline='\n') as csvfile:
                    for line in csvfile:
                        cur_filename = scenario_name.split(" - ")[0]

                        if "Horiz Sens" in line and re.search(r'\d+.\d+', line):
                            stripped = line.rstrip()
                            sens = re.findall(r'\d+.\d+', stripped)[0]
                            sens = float(sens)

                            if sens == cur_sens:
                                if cur_filename in highscore_files:
                                    highscore_files[cur_filename]["sens"] = sens
                                else:
                                    highscore_files[cur_filename] = {
                                        "score": 0,
                                        "sens": sens
                                    }
                            else:
                                if cur_filename not in highscore_files:
                                    highscore_files = {
                                        "score": 0,
                                        "sens": 0
                                    }
                        if "Score" in line:
                            stripped = line.rstrip()
                            score = re.findall(r'\d+.\d+', stripped)[0]
                            score = float(score)

                            if cur_filename in highscore_files:
                                if highscore_files[cur_filename]["score"] < score and highscore_files[cur_filename]["sens"] == cur_sens:
                                    highscore_files[cur_filename]["score"] = score
    return highscore_files
