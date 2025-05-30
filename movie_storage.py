import json

# Der Name der JSON-Datei, in der die Filmdaten gespeichert werden
DATA_FILE = 'data.json'

def get_movies():
    """Lädt und gibt die Filmdaten aus der JSON-Datei zurück."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Wenn die Datei nicht gefunden wird, geben wir ein leeres Dictionary zurück
        return {}

def save_movies(movies):
    """Speichert die Filmdaten im JSON-Format in der Datei."""
    with open(DATA_FILE, 'w') as file:
        json.dump(movies, file, indent=4)

def add_movie(title, year, rating):
    """Fügt einen neuen Film in die JSON-Datei hinzu."""
    movies = get_movies()
    if title in movies:
        print(f"Der Film '{title}' existiert bereits.")
        return
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)

def delete_movie(title):
    """Löscht einen Film aus der JSON-Datei."""
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)


def update_movie(title, rating):
    """ Updates the rating of a movie in the JSON file. """
    movies = get_movies()
    # Strip the title to remove leading/trailing spaces
    title = title.strip()

    # Case-insensitive matching for title
    for movie_title in movies:
        if movie_title.lower() == title.lower():
            movies[movie_title]["rating"] = rating
            save_movies(movies)
            return



