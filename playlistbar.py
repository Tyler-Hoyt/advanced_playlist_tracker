import os
import tkinter as tk
import json


class PlaylistBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def load_playlists(self, directory):
        playlist_names = self.__get_playlist_names(directory)

        cur_row = 0
        for name in playlist_names:
            label = tk.Label(self, text=name)
            label.grid(row=cur_row, column=0, padx=2, pady=2)

            button = tk.Button(
                self,
                text="Select Playlist",
                command=lambda name=name: self.__change_selected_playlist(name)
            )
            button.grid(row=cur_row, column=1, padx=2, pady=(5, 0))

            cur_row += 1

    def __get_playlist_names(self, directory):
        """Reads all file names in the specified directory."""

        file_names = []
        for entry in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, entry)):
                if self.__is_playlist_file(os.path.join(directory, entry)):
                    file_names.append(entry)
        return file_names

    def __is_playlist_file(self, file_path):
        """Checks if the file is a valid playlist file"""
        if file_path.endswith(".json"):
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Need to add more checks here but fine for now
                if 'scenarioList' in data:
                    return True
        return False

    def __change_selected_playlist(self, selected_playlist):
        """Changes the selected playlist"""

        self.parent.statsview.load_playlist(selected_playlist)
        self.parent.topbar.label.config(
                text="Selected Playlist: " + selected_playlist
        )
        self.parent.statsview.controlpanel.start_button.config(
                state=tk.NORMAL
        )
