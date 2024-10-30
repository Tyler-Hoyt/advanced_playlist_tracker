import tkinter as tk
from tkinter import filedialog


class TopBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.directory = None
        self.parent = parent

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

        label = tk.Label(self, text="Select Playlist Directory")
        label.pack(side=tk.RIGHT)

    def __open_directory(self):
        self.directory = filedialog.askdirectory(
            initialdir="/",
            title="Select directory"
        )

        if self.directory != "":
            self.pack_forget()
            self.parent.create_playlistbar(self.directory)
