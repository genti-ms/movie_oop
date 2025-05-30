import random
import statistics
from omdb_api import fetch_movie_from_omdb

class MovieApp:
    """
    Main application class to manage movies.

    Provides commands for listing, adding (via OMDb), deleting,
    updating ratings, showing stats, searching, and more.
    """

    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage instance.

        Args:
            storage: An instance implementing the IStorage interface.
        """
        self._storage = storage

    def _command_list_movies(self):
        """Display all stored movies with year and rating."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
        else:
            for title, details in movies.items():
                print(f"{title} ({details['year']}), Rating: {details['rating']}")
        input("\nPress Enter to continue ")

    def _command_add_movie_api(self):
        """
        Add a new movie by searching OMDb API with the title entered by the user.

        Fetches title, year, rating, and poster URL from OMDb and stores them.
        Handles errors like movie not found or API connection issues.
        """
        title = input("Enter movie title to search (OMDb): ").strip()
        if not title:
            print("Title cannot be empty.")
            input("\nPress Enter to continue ")
            return

        movie = fetch_movie_from_omdb(title)
        if movie is None:
            print("Movie could not be found or loaded.")
            input("\nPress Enter to continue ")
            return

        movies = self._storage.list_movies()
        if movie['title'] in movies:
            print(f"Movie '{movie['title']}' already exists in storage.")
        else:
            self._storage.add_movie(
                movie['title'],
                movie['year'],
                movie['rating'],
                movie['poster']
            )
            print(f"Movie '{movie['title']}' added successfully.")
        input("\nPress Enter to continue ")

    def _command_delete_movie(self):
        """Delete a movie from storage by title."""
        title = input("Enter movie title to delete: ").strip()
        movies = self._storage.list_movies()
        if title not in movies:
            print("Movie not found.")
        else:
            self._storage.delete_movie(title)
            print(f"Movie '{title}' deleted.")
        input("\nPress Enter to continue ")

    def _command_update_movie(self):
        """
        Update the rating of an existing movie.

        This command remains unchanged, allowing manual rating update.
        """
        title = input("Enter movie title to update: ").strip()
        movies = self._storage.list_movies()
        if title not in movies:
            print("Movie not found.")
            input("\nPress Enter to continue ")
            return

        try:
            rating = float(input("Enter new rating (1-10): ").strip())
            if rating < 1 or rating > 10:
                raise ValueError
        except ValueError:
            print("Invalid rating.")
            input("\nPress Enter to continue ")
            return

        self._storage.update_movie(title, rating)
        print(f"Movie '{title}' updated.")
        input("\nPress Enter to continue ")

    def _command_stats(self):
        """
        Show statistics about movies: average rating, median, best and worst rated movies.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            input("\nPress Enter to continue ")
            return

        ratings = [details["rating"] for details in movies.values()]
        avg = sum(ratings) / len(ratings)
        med = statistics.median(ratings)
        best = max(ratings)
        worst = min(ratings)

        best_movies = [t for t, d in movies.items() if d["rating"] == best]
        worst_movies = [t for t, d in movies.items() if d["rating"] == worst]

        print(f"Average rating: {avg:.2f}")
        print(f"Median rating: {med:.2f}")

        print(f"\nBest movie(s) with rating {best}:")
        for m in best_movies:
            print(f" - {m}")

        print(f"\nWorst movie(s) with rating {worst}:")
        for m in worst_movies:
            print(f" - {m}")

        input("\nPress Enter to continue ")

    def _command_random_movie(self):
        """Print a random movie from the storage."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            input("\nPress Enter to continue ")
            return
        title, details = random.choice(list(movies.items()))
        print(f"Random movie: {title} ({details['year']}), Rating: {details['rating']}")
        input("\nPress Enter to continue ")

    def _command_search_movie(self):
        """Search movies by a substring in their title and display matches."""
        query = input("Enter search term: ").strip().lower()
        movies = self._storage.list_movies()
        matches = {t: d for t, d in movies.items() if query in t.lower()}
        if matches:
            for title, details in matches.items():
                print(f"{title} ({details['year']}), Rating: {details['rating']}")
        else:
            print("No matching movies found.")
        input("\nPress Enter to continue ")

    def _command_movies_sorted_by_rating(self):
        """List all movies sorted by rating in descending order."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            input("\nPress Enter to continue ")
            return

        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        print("\nMovies sorted by rating (high to low):")
        for title, details in sorted_movies:
            print(f"{title} ({details['year']}), Rating: {details['rating']}")
        input("\nPress Enter to continue ")

    def _command_generate_website(self):
        """
        Generate an HTML website from the movie list using the template.
        """
        try:
            with open("_static/index_template.html", "r", encoding="utf-8") as f:
                template = f.read()

            title = "My Movie App"
            movies = self._storage.list_movies()

            movie_html = ""
            for name, info in movies.items():
                movie_html += f'''
                <li>
                  <div class="movie">
                    <img src="{info['poster']}" alt="{name} poster" class="movie-poster">
                    <div class="movie-title">{name}</div>
                    <div class="movie-year">{info['year']}</div>
                  </div>
                </li>
                '''

            final_html = template.replace("__TEMPLATE_TITLE__", title)
            final_html = final_html.replace("__TEMPLATE_MOVIE_GRID__", movie_html)

            with open("index.html", "w", encoding="utf-8") as f:
                f.write(final_html)

            print("Website was generated successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        input("\nPress Enter to continue ")



    def run(self):
        """
        Run the main menu loop to accept and process user commands.
        """
        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie (via OMDb API)")
            print("3. Delete movie")
            print("4. Update movie rating")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website")
            choice = input("Enter choice (0-9): ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie_api()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_movies_sorted_by_rating()
            elif choice == "9":
                self._command_generate_website()
            else:
                print("Invalid choice. Please enter a number between 0 and 9.")
