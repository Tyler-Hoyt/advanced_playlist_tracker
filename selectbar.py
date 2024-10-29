import tkinter as tk
from tkinter import filedialog


class SelectBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.directory = None

        label = tk.Label(self, text="Select Playlist Directory")
        label.pack(side=tk.LEFT, expand=True)

        button = tk.Button(
                self,
                text="Open Directory",
                command=self.__open_directory
        )
        button.pack(side=tk.LEFT, expand=True)

    def __open_directory(self):
        self.directory = filedialog.askdirectory(
            initialdir="/",
            title="Select directory"
        )

        if self.directory is not None:
            self.pack_forget()
            self.parent.create_playlistbar(self.directory)
