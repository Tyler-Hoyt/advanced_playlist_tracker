import os
import tkinter as tk
from tkinter import filedialog
from constants.paths import WIN_DIR_PATH, WIN_SCORES_PATH, WIN_SETTINGS_PATH
from utils import get_playlist_names, get_scenario_scores


class TopBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.selected_playlist_label = tk.Label(self, text="Selected Playlist: ")
        self.open_directory_button = tk.Button(self, text="Open Directory", command=self.__open_directory)
        self.button_label = tk.Label(self, text="Select Playlist Directory")

        self.selected_playlist_label.config(font=("Helvetica", 14, "bold"))

        self.selected_playlist_label.pack(side=tk.LEFT)
        self.open_directory_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.button_label.pack(side=tk.RIGHT)

        if os.environ["OS"] == "Windows_NT":
            print("nice")
            self.open_directory_button.config(state=tk.DISABLED)
            self.parent.directory = WIN_DIR_PATH
            self.parent.scores_path = WIN_SCORES_PATH
            self.parent.settings_path = WIN_SETTINGS_PATH
            self.parent.create_playlistbar(self.parent.directory)

    def __open_directory(self):
        self.parent.directory = filedialog.askdirectory(initialdir="/", title="Select directory")
        if self.parent.directory != "":
            self.parent.create_playlistbar(self.directory)


class PlaylistBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def load_playlist(self, directory):
        playlist_names = get_playlist_names(directory)

        cur_row = 0
        for name in playlist_names:
            label = tk.Label(self, text=name)
            button = tk.Button(
                self,
                text="Select Playlist",
                command=lambda name=name: self.__change_selected_playlist(name)
            )

            label.grid(row=cur_row, column=0, padx=2, pady=2)
            button.grid(row=cur_row, column=1, padx=2, pady=(5, 0))

            cur_row += 1

    def __change_selected_playlist(self, selected_playlist):
        self.parent.statspanel.load_playlist(selected_playlist)
        self.parent.topbar.selected_playlist_label.config(
            text="Selected Playlist: " + selected_playlist
        )
        self.parent.statspanel.controlpanel.start_button.config(
            state=tk.NORMAL
        )


class StatsPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.controlpanel = ControlPanel(self)
        self.scenariobar = ScenarioBar(self)

        self.controlpanel.pack(side="bottom", fill="x")
        self.scenariobar.pack(side="left", fill="y")

    def start_threshold_training(self):
        self.parent.is_training = True
        self.controlpanel.start_button.config(state=tk.DISABLED)
        self.controlpanel.end_button.config(state=tk.NORMAL)

        parent_widgets = self.parent.playlistbar.winfo_children()
        parent_widgets += self.parent.topbar.winfo_children()
        for widget in parent_widgets:
            if widget.winfo_class() == "Button":
                widget.config(state=tk.DISABLED)

    def end_threshold_training(self):
        self.parent.is_training = False
        self.controlpanel.start_button.config(state=tk.NORMAL)
        self.controlpanel.end_button.config(state=tk.DISABLED)

        parent_widgets = self.parent.playlistbar.winfo_children()
        parent_widgets += self.parent.topbar.winfo_children()
        for widget in parent_widgets:
            if widget.winfo_class() == "Button":
                widget.config(state=tk.NORMAL)


class ScenarioBar(tk.Frame):
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
            score_dict = get_scenario_scores(self.parent.parent.settings_path, self.parent.parent.scores_path, scen['scenario_name'])

            scen_highscore_label = tk.Label(self, text=score_dict[scen['scenario_name']]['score'])
            scen_highscore_label.grid(row=cur_row, column=1, sticky="w", padx=20, pady=2)

            threshold_label = tk.Label(self, text=score_dict[scen['scenario_name']]['score']*0.9)
            threshold_label.grid(row=cur_row, column=2, sticky="w", padx=20, pady=2)
            cur_row += 1


class ControlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.start_button = tk.Button(self, text="Start Training")
        self.end_button = tk.Button(self, text="End Training")

        self.start_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        self.end_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        self.start_button.config(state=tk.DISABLED)
        self.end_button.config(state=tk.DISABLED)

