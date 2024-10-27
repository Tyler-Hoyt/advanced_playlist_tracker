import tkinter as tk

class TopBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.label = tk.Label(self, text="Selected Playlist: ")
        self.label.pack(side=tk.LEFT)
