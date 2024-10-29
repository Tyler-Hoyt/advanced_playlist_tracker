import tkinter as tk


class TopBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Public
        self.label = tk.Label(self, text="Selected Playlist: ")
        self.label.config(font=("Helvetica", 14, "bold"))
        self.label.pack(side=tk.LEFT)

        # Private
        selected_directory = tk.Label(self, text="")
        selected_directory.config(font=("Helvetica", 14, "bold"))
        selected_directory.pack(side=tk.RIGHT)
