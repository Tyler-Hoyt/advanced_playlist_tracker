import json
import os
import tkinter as tk

class StatsView(tk.Frame):
    directory_path = "C:\Program Files (x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\Saved\SaveGames\Playlists"
    scores_path = "C:\Program Files (x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\stats"

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.bottomstatsbar = BottomStatsBar(self)
        self.leftstatsbar = LeftStatsBar(self)

        self.bottomstatsbar.pack(side="bottom", fill="x")
        self.leftstatsbar.pack(side="left", fill="y")

    def load_playlist(self, playlist_name):
        with open(self.directory_path + '\\' + playlist_name, 'r') as file:
            data = json.load(file)
            self.leftstatsbar.set_scenarios(data['scenarioList'])

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

        threshold_label= tk.Label(self, text="Threshold")
        threshold_label.grid(row=0, column=2, padx=10, pady=2)

        cur_row = 1
        for scen in scenarios:
            label = tk.Label(self, text=scen['scenario_name'])
            label.grid(row=cur_row, column=0, sticky="w", padx=20, pady=2)
           
            self.get_scenario_scores(scen['scenario_name'])
            cur_row+=1

    def get_scenario_scores(self, scenario_name):
        for dirpath, dirnames, filenames in os.walk(self.parent.scores_path):
            for filename in filenames:
                if filename.split('-')[0].rstrip() == scenario_name:
                    print(filename)

class BottomStatsBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        start_button = tk.Button(self, text="Start Threshold Training") 
        start_button.pack(side=tk.RIGHT, padx=10, pady=10)

        end_button = tk.Button(self, text="End Threshold Training")
        end_button.pack(side=tk.RIGHT, padx=10, pady=10)
