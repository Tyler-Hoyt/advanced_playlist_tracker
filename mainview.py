import tkinter as tk
from topbar import TopBar
from playlistbar import PlaylistBar
from statsview import StatsView
from selectbar import SelectBar


class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Set root attributes
        parent.title("Advanced Playlist Tracker")
        parent.wm_geometry("800x600")

        self.topbar = TopBar(self)
        self.playlistbar = PlaylistBar(self)
        self.statsview = StatsView(self)

        self.topbar.pack(side="top", fill="x")
        self.statsview.pack(side="right", fill="both", expand="True")

    def create_playlistbar(self, directory):
        self.playlistbar.pack(side="left", fill="y")
        self.playlistbar.load_playlists(directory)


if __name__ == "__main__":
    root = tk.Tk()
    MainView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
