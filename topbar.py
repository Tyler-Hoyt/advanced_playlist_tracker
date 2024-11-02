import os
import tkinter as tk
from tkinter import filedialog


class TopBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.directory = None
        self.scores_path = None
        self.settings_path = None
        self.parent = parent

        win_directory_path = "C:/Program Files (x86)/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/Saved/SaveGames/Playlists"
        win_scores_path = "C:/Program Files (x86)/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/stats"
        win_settings_path = "C:/Program Files (x86)/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/Saved/SaveGames/PrimaryUserSettings.json"

        # Public
        self.label = tk.Label(self, text="Selected Playlist: ")
        self.label.config(font=("Helvetica", 14, "bold"))
        self.label.pack(side=tk.LEFT)

        button = tk.Button(
                self,
                text="Open Directory",
                command=self.__open_directory
        )
        button.pack(side=tk.RIGHT, padx=(0, 10))

        print(os.environ["OS"])
        if os.environ["OS"] == "Windows_NT":
            button.config(state=tk.DISABLED)
            self.directory = win_directory_path
            self.scores_path = win_scores_path
            self.settings_path = win_settings_path
            self.parent.create_playlistbar(self.directory)
            print("playlist directory defaulted")

        label = tk.Label(self, text="Select Playlist Directory")
        label.pack(side=tk.RIGHT)

    def __open_directory(self):
        self.directory = filedialog.askdirectory(
            initialdir="/",
            title="Select directory"
        )

        if self.directory != "":
            self.parent.create_playlistbar(self.directory)
