import requests

API_KEY = "db49531e"  # Your OMDb API key

def fetch_movie_from_omdb(title: str) -> dict | None:
    """
    Fetch movie details from OMDb API by title.

    Args:
        title (str): The movie title to search.

    Returns:
        dict: A dictionary with keys 'title', 'year', 'rating', and 'poster' if movie found.
        None: If movie is not found or an error occurs.
    """
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": API_KEY,
        "t": title,
        "r": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error connecting to OMDb API: {e}")
        return None

    data = response.json()
    if data.get("Response") == "True":
        year_str = data.get("Year", "0")
        try:
            year = int(year_str.split("–")[0])
        except (ValueError, AttributeError):
            year = 0

        try:
            rating = float(data.get("imdbRating", "0")) if data.get("imdbRating") != "N/A" else 0.0
        except ValueError:
            rating = 0.0

        poster = data.get("Poster", "")
        if poster == "N/A":
            poster = ""

        return {
            "title": data.get("Title", title),
            "year": year,
            "rating": rating,
            "poster": poster
        }
    else:
        print(f"Movie '{title}' not found.")
        return None
