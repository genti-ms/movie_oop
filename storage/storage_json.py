import json
from .istorage import IStorage

class StorageJson(IStorage):
    """
    JSON file based implementation of the IStorage interface.
    """

    def __init__(self, file_path):
        """
        Initializes the storage with the path to the JSON file.

        Args:
            file_path (str): Path to the JSON storage file.
        """
        self._file_path = file_path

    def _load_data(self):
        try:
            with open(self._file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_data(self, data):
        with open(self._file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def list_movies(self):
        """
        Returns all movies from the JSON storage.

        Returns:
            dict: Dictionary of movies.
        """
        return self._load_data()

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the JSON storage.

        Args:
            title (str): Movie title.
            year (int): Release year.
            rating (float): Movie rating.
            poster (str): Poster path or URL.
        """
        data = self._load_data()
        data[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self._save_data(data)

    def delete_movie(self, title):
        """
        Deletes a movie from the JSON storage by title.

        Args:
            title (str): Movie title to delete.
        """
        data = self._load_data()
        if title in data:
            del data[title]
            self._save_data(data)

    def update_movie(self, title, rating):
        """
        Updates the rating of a movie.

        Args:
            title (str): Movie title.
            rating (float): New rating.
        """
        data = self._load_data()
        if title in data:
            data[title]["rating"] = rating
            self._save_data(data)


