"""
Simple script to manually test the StorageJson class.
"""

from storage_json import StorageJson

def main():
    storage = StorageJson('john.json')

    print("Current movies:", storage.list_movies())

    storage.add_movie("Titanic", 1997, 9, "titanic_poster.jpg")
    storage.add_movie("Inception", 2010, 8, "inception_poster.jpg")

    print("After adding movies:", storage.list_movies())

    storage.update_movie("Titanic", 10)
    print("After updating Titanic rating:", storage.list_movies())

    storage.delete_movie("Inception")
    print("After deleting Inception:", storage.list_movies())

if __name__ == "__main__":
    main()
