import os

def get_playlist_names(directory):
    """Reads all file names in the specified directory."""

    file_names = []
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            file_names.append(entry)
    return file_names

# Example usage
directory_path = "C:\Program Files (x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\Saved\SaveGames\Playlists"
file_names = get_playlist_names(directory_path)
print(file_names)
