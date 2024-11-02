import json
import pandas as pd
import os
import re
import tkinter as tk
from datetime import datetime


class StatsView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.is_training = False

        self.controlpanel = ControlPanel(self)
        self.leftstatsbar = LeftStatsBar(self)

        self.controlpanel.pack(side="bottom", fill="x")
        self.leftstatsbar.pack(side="left", fill="y")

    def load_playlist(self, playlist_name):
        with open(self.parent.topbar.directory + '/' + playlist_name,
                  'r'
                  ) as file:
            data = json.load(file)
            self.leftstatsbar.set_scenarios(data['scenarioList'])

    def start_threshold_training(self):
        self.is_training = True
        self.controlpanel.start_button.config(state=tk.DISABLED)
        self.controlpanel.end_button.config(state=tk.NORMAL)

        parent_widgets = self.parent.playlistbar.winfo_children()
        parent_widgets += self.parent.topbar.winfo_children()
        for widget in parent_widgets:
            if widget.winfo_class() == "Button":
                widget.config(state=tk.DISABLED)

    def end_threshold_training(self):
        self.is_training = False
        self.controlpanel.start_button.config(state=tk.NORMAL)
        self.controlpanel.end_button.config(state=tk.DISABLED)

        parent_widgets = self.parent.playlistbar.winfo_children()
        for widget in parent_widgets:
            if widget.winfo_class() == "Button":
                widget.config(state=tk.NORMAL)


class LeftStatsBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def set_scenarios(self, scenarios):
        # Destroy previous labels
        for widget in self.winfo_children():
            widget.destroy()

        highscore_label = tk.Label(self, text="Highscore")
        highscore_label.grid(row=0, column=1, padx=10, pady=2)

        threshold_label = tk.Label(self, text="Threshold")
        threshold_label.grid(row=0, column=2, padx=10, pady=2)

        cur_row = 1
        for scen in scenarios:
            scen_name_label = tk.Label(self, text=scen['scenario_name'])
            scen_name_label.grid(row=cur_row, column=0, sticky="w", padx=20, pady=2)
            score_dict = self.get_scenario_scores(scen['scenario_name'])

            scen_highscore_label = tk.Label(self, text=score_dict[scen['scenario_name']]['score'])
            scen_highscore_label.grid(row=cur_row, column=1, sticky="w", padx=20, pady=2)

            threshold_label = tk.Label(self, text=score_dict[scen['scenario_name']]['score']*0.9)
            threshold_label.grid(row=cur_row, column=2, sticky="w", padx=20, pady=2)
            cur_row += 1

    def get_scenario_scores(self, scenario_name):
        cur_sens = 0.0
        with open(self.parent.parent.topbar.settings_path, "r") as settings_file:
            data = json.load(settings_file)
            cur_sens = data["floatSettings"]["EFloatSettingId::XSens"]

        d = {}
        for dirpath, dirnames, filenames in os.walk(self.parent.parent.topbar.scores_path):
            for file in filenames:
                if file.split('-')[0].rstrip() == scenario_name:
                    with open(f"{self.parent.parent.topbar.scores_path}/{file}", newline='\n') as csvfile:
                        for line in csvfile:
                            filename = scenario_name.split(" - ")[0]
                            if "Horiz Sens" in line and re.search(r'\d+.\d+', line):
                                stripped = line.rstrip()
                                sens = re.findall(r'\d+.\d+', stripped)[0]
                                sens = float(sens)
                                if sens == cur_sens:
                                    if filename in d:
                                        d[filename]["sens"] = sens
                                    else:
                                        d[filename] = {"score": 0, "sens": sens}
                                else:
                                    if filename not in d:
                                        # No score on this sens
                                        d[filename] = {"score": 0, "sens": 0}
                            if "Score" in line:
                                stripped = line.rstrip()
                                score = re.findall(r'\d+.\d+', stripped)[0]
                                score = float(score)
                                if filename in d:
                                    if d[filename]["score"] < score and d[filename]["sens"] == cur_sens:
                                        d[filename]["score"] = score
        return d


class ControlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Public
        self.start_button = tk.Button(
                self,
                text="Start Threshold Training",
                command=self.parent.start_threshold_training
        )
        self.start_button.config(state=tk.DISABLED)
        self.start_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.end_button = tk.Button(
                self,
                text="End Threshold Training",
                command=self.parent.end_threshold_training
        )
        self.end_button.config(state=tk.DISABLED)
        self.end_button.pack(side=tk.RIGHT, padx=10, pady=10)
