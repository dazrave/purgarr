import requests
import json

class DiscordClient:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
        self.webhook_url = config['discord']['webhook_url']

    def send_message(self, content):
        data = {
            "content": content
        }
        response = requests.post(self.webhook_url, data=data)
        response.raise_for_status()
