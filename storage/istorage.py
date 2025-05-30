from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    Interface for movie storage classes defining CRUD operations.
    """

    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of movies stored.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the storage.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the storage by title.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the rating of a movie by title.
        """
        pass
