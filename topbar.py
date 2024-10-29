import tkinter as tk


class TopBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Public
        self.label = tk.Label(self, text="Selected Playlist: ")
        self.label.config(font=("Helvetica", 14, "bold"))
        self.label.pack(side=tk.LEFT)

        # Private
        title = tk.Label(self, text="Advanced Playlist Tracker")
        title.config(font=("Helvetica", 14, "bold"))
        title.pack(side=tk.RIGHT)
