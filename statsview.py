import json
import pandas as pd
import os
import tkinter as tk


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
            label = tk.Label(self, text=scen['scenario_name'])
            label.grid(row=cur_row, column=0, sticky="w", padx=20, pady=2)
            self.get_scenario_scores(scen['scenario_name'])
            cur_row += 1

    def get_scenario_scores(self, scenario_name):
        count = 0
        for dirpath, dirnames, filenames in os.walk(self.parent.parent.topbar.scores_path):
            for filename in filenames:
                if filename.split('-')[0].rstrip() == scenario_name and count == 1464:
                    df = pd.read_csv(self.parent.parent.topbar.scores_path + '/' + filename)
                    df_rows = df.loc[['Score:', 'Horiz Sens:']]
                    df_cols = df_rows.iloc[:, [0]]
                    print(df_cols)
                count+=1


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
