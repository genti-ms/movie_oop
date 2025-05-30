from storage.storage_json import StorageJson
from movie_app import MovieApp

def main():
    """
    Main entry point of the movie app.
    Creates a JSON storage instance and starts the MovieApp.
    """
    storage = StorageJson('data/movies.json')
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()
