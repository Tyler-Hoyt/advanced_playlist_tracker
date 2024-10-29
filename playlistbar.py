import os
import tkinter as tk


class PlaylistBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #directory_path = "C:/Program Files (x86)/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/Saved/SaveGames/Playlists"
        #playlist_names = self.__get_playlist_names(directory_path)
        playlist_names = ["Test1", "Test2", "Test3"]

        cur_row = 0
        for name in playlist_names:
            label = tk.Label(self, text=name)
            label.grid(row=cur_row, column=0, padx=2, pady=2)

            button = tk.Button(
                self,
                text="Select Playlist",
                command=lambda name=name: self.__change_selected_playlist(name)
            )
            button.grid(row=cur_row, column=1, padx=2, pady=2)

            cur_row += 1

    def __get_playlist_names(self, directory):
        """Reads all file names in the specified directory."""

        file_names = []
        for entry in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, entry)):
                file_names.append(entry)
        return file_names

    def __change_selected_playlist(self, selected_playlist):
        """Changes the selected playlist"""

        self.parent.statsview.load_playlist(selected_playlist)
        self.parent.topbar.label.config(
                text="Selected Playlist: " + selected_playlist
        )
        self.parent.statsview.controlpanel.start_button.config(
                state=tk.NORMAL
        )
