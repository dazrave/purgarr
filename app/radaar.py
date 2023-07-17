import requests
from datetime import datetime

class RadarrClient:
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url

    def get_movies(self):
        response = requests.get(f"{self.url}/api/movie", params={"apikey": self.api_key})
        response.raise_for_status()
        return response.json()

    def update_movie(self, movie, add_archive=False, remove_archive=False):
        if add_archive:
            # If the movie doesn't already have the 'Archive' label, add it
            if 'Archive' not in movie['labels']:
                movie['labels'].append('Archive')
                movie['archive_date'] = datetime.now()
        elif remove_archive:
            # If the movie has the 'Archive' label, remove it
            if 'Archive' in movie['labels']:
                movie['labels'].remove('Archive')
                movie['archive_date'] = None

        response = requests.put(
            f"{self.url}/api/movie/{movie['id']}",
            params={"apikey": self.api_key},
            json=movie
        )
        response.raise_for_status()

    def delete_movie(self, movie):
        response = requests.delete(
            f"{self.url}/api/movie/{movie['id']}",
            params={"apikey": self.api_key}
        )
        response.raise_for_status()
