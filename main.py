import tkinter as tk
from ui import TopBar, StatsPanel, PlaylistBar


class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.directory = None
        self.scores_path = None
        self.settings_path = None
        self.is_training = False

        # Set root attributes
        parent.title("Advanced Playlist Tracker")
        parent.wm_geometry("800x600")

        self.maincontainer = tk.Frame(self)
        self.playlistbar = PlaylistBar(self.maincontainer)
        self.statspanel = StatsPanel(self.maincontainer)
        self.topbar = TopBar(self)

        self.topbar.pack(side="top", fill="x")
        self.maincontainer.pack(side="top", fill="both", expand=True)
        self.statspanel.pack(side="right", fill="y")
        self.playlistbar.pack(side="left", fill="y")

    def create_playlistbar(self, directory):
        self.playlistbar.pack(side="left", fill="y", pady=20)
        self.playlistbar.load_playlist(directory)


if __name__ == "__main__":
    root = tk.Tk()
    MainView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
