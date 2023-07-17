from plexapi.server import PlexServer
import json

class PlexClient:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
        self.baseurl = config['plex']['url']
        self.token = config['plex']['api_key']
        self.plex = PlexServer(self.baseurl, self.token)

    def get_media_views(self, movie_title):
        movie = self.plex.library.section('Movies').get(movie_title)
        return movie.viewCount if movie.viewCount else 0
