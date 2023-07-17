import json
from datetime import datetime, timedelta
from radarr import RadarrClient
from plex import PlexClient
from discord import DiscordClient

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    # Load the settings and config
    settings = load_json('settings.json')
    config = load_json('config.json')

    # Instantiate the Radarr, Plex, and Discord clients
    radarr = RadarrClient(config['radarr']['api_key'], config['radarr']['url'])
    plex = PlexClient(config['plex']['username'], config['plex']['password'], config['plex']['server_name'])
    discord = DiscordClient(config['discord']['webhook_url'])

    # Get the list of movies from Radarr
    radarr_movies = radarr.get_movies()

    # Get the list of movies from Plex
    plex_movies = plex.get_movies()

    # Get the current date
    now = datetime.now()

    # List of movies to be deleted
    movies_to_delete = []

    # Iterate over the movies from Radarr
    for radarr_movie in radarr_movies:
        # Check if the movie exists in Plex
        plex_movie = plex_movies.get(radarr_movie['title'])

        # If the movie exists in Plex
        if plex_movie:
            # Check if the movie is old enough and doesn't have the 'Archive' or 'Keep' label
            if (radarr_movie['year'] < now.year - settings['purge_deadline'] and 
                'Archive' not in radarr_movie['labels'] and 
                'Keep' not in radarr_movie['labels'] and 
                not any(tag in radarr_movie['labels'] for tag in settings['purge_protect']) and
                (plex_movie.lastViewedAt < now - timedelta(days=settings['purge_deadline']))):

                # Add the 'Archive' label and schedule it for deletion
                radarr_movie['archive_date'] = now + timedelta(days=settings['purge_deadline'])
                radarr.update_movie(radarr_movie, add_archive=True)

        # If the movie has the 'Archive' label and it's not protected
        elif ('Archive' in radarr_movie['labels'] and 
              'Keep' not in radarr_movie['labels'] and 
              not any(tag in radarr_movie['labels'] for tag in settings['purge_protect'])):
            
            # If the movie has been in the archive for long enough and hasn't been watched since being archived
            if ((now - radarr_movie['archive_date']).days > settings['purge_cooldown'] and 
                (plex_movie is None or plex_movie.lastViewedAt < radarr_movie['archive_date'])):
                
                # Add movie to the list of movies to be deleted
                movies_to_delete.append(radarr_movie['title'])

                # Delete the movie
                radarr.delete_movie(radarr_movie)

    # If announcements are enabled and there are movies to delete, send a message to Discord
    if settings['discord_announcements'] and movies_to_delete:
        discord.send_message(f"Movies to be deleted soon: {', '.join(movies_to_delete)}. They will be deleted in {settings['purge_cooldown']} days.")

if __name__ == "__main__":
    main()
