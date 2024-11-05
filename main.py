import os
import tkinter as tk
from tkinter import filedialog
from constants.paths import WIN_DIR_PATH, WIN_SCORES_PATH, WIN_SETTINGS_PATH
from playlistbar import PlaylistBar
from statsview import StatsView


class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.directory = None
        self.scores_path = None
        self.settings_path = None

        # Set root attributes
        parent.title("Advanced Playlist Tracker")
        parent.wm_geometry("800x600")

        self.playlistbar = PlaylistBar(self)
        self.statsview = StatsView(self)
        self.topbar = TopBar(self)

        self.topbar.pack(side="top", fill="x")
        self.statsview.pack(side="right", fill="both", expand="True")

    def create_playlistbar(self, directory):
        self.playlistbar.pack(side="left", fill="y", pady=20)
        self.playlistbar.load_playlists(directory)


class TopBar(tk.Frame):
    def __init(self, parent, *args, **kwargs):
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
            self.open_directory_button.config(state=tk.DISABLED)
            self.parent.directory = WIN_DIR_PATH
            self.parent.scores_path = WIN_SCORES_PATH
            self.parent.settings_path = WIN_SETTINGS_PATH

    def __open_directory(self):
        self.parent.directory = filedialog.askdirectory(initialdir="/", title="Select directory")
        if self.parent.directory != "":
            self.parent.create_playlistbar(self.directory)


if __name__ == "__main__":
    root = tk.Tk()
    MainView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
