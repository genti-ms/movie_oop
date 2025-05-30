import json

# The name of the JSON file where movie data is stored
DATA_FILE = 'data.json'

def get_movies():
    """Loads and returns movie data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_movies(movies):
    """Saves movie data in JSON format to the file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(movies, file, indent=4)

def add_movie(title, year, rating):
    """Adds a new movie to the JSON file."""
    movies = get_movies()
    if title in movies:
        print(f"The movie '{title}' already exists.")
        return
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)

def delete_movie(title):
    """Deletes a movie from the JSON file."""
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)

def update_movie(title, rating):
    """Updates the rating of a movie in the JSON file."""
    movies = get_movies()
    # Strip the title to remove leading/trailing spaces
    title = title.strip()

    # Case-insensitive matching for the title
    for movie_title in movies:
        if movie_title.lower() == title.lower():
            movies[movie_title]["rating"] = rating
            save_movies(movies)
            return
