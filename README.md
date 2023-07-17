# Purgarr

Purgarr is a media management tool that helps you automate the cleanup process of your media library. Using Radarr and Plex APIs, Purgarr identifies old movies in your library that are due for deletion based on configurable criteria. It also leverages Discord to send notifications about upcoming deletions, giving users a chance to view the content before removal.

## Features

- Configurable deletion criteria: Set up rules based on the movie's age, recent viewings, and protective tags.
- Activity reset: If a movie scheduled for deletion has been watched recently, it gets a second chance.
- Discord notifications: Get notified about upcoming deletions.
- Purge protect: Prevent deletion of certain movies by applying specific tags.
- Docker support: Easily deploy Purgarr in a Docker container.

## Configuration

The application can be configured using two JSON files:

- `config.json`: Stores API information for Radarr, Plex, and Discord.
- `settings.json`: Stores application settings like deletion rules and notification settings.

Refer to `config_sample.json` and `settings_sample.json` for example configurations.

## Usage

To use Purgarr, ensure you have Docker installed and follow the steps below:

1. Clone the repository and navigate into the project directory.
2. Configure `config.json` and `settings.json` as required.
3. Build the Docker image: `docker build -t purgarr .`
4. Run the Docker container: `docker run -d purgarr`

Remember to replace actual Docker commands and paths as necessary.

## Disclaimer

Purgarr directly interacts with your Radarr and Plex setup and can result in deletion of movies from your library. Make sure you understand the configuration and use it responsibly. Always ensure your data is backed up and secure.

## Contributing

If you'd like to contribute to Purgarr, please feel free to submit a pull request!

## License

Purgarr is open-source software licensed under the MIT license.
