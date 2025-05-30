import csv
import os
from .istorage import IStorage

class StorageCsv(IStorage):
    """
    CSV file based implementation of the IStorage interface.
    """

    def __init__(self, filename):
        """
        Initialize with a CSV filename.
        Creates file with header if it does not exist.
        """
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["title", "year", "rating", "poster"])  # Poster Spalte auch hier

    def list_movies(self):
        """
        Returns all movies as a dict:
        {title: {"year": int, "rating": float, "poster": str}, ...}
        """
        movies = {}
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row['title']
                    year = int(row['year'])
                    rating = float(row['rating'])
                    poster = row.get('poster', '')  # Falls Poster fehlt, leerer String
                    movies[title] = {"year": year, "rating": rating, "poster": poster}
        except FileNotFoundError:
            pass
        return movies

    def add_movie(self, title, year, rating, poster):
        """
        Add or overwrite a movie.
        """
        movies = self.list_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Delete a movie by title.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Update rating of an existing movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Save the movies dict to CSV.
        """
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    "title": title,
                    "year": details['year'],
                    "rating": details['rating'],
                    "poster": details.get('poster', '')
                })
