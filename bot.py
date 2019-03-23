import json

from twython import Twython


class Bot:

    def __init__(self):
        with open('config.json', 'r') as r:
            config = json.load(r)

        self.twitter = Twython(config['APP_KEY'], config['APP_SECRET'], config['OAUTH_TOKEN'], config['OAUTH_SECRET'])
        self.auth = self.twitter.get_authentication_tokens()

    def send_tweet_with_image(self, message, image_filename):
        image = open(image_filename, 'rb')
        response = self.twitter.upload_media(media=image)
        media_id = [response['media_id']]
        self.twitter.update_status(status=message, media_ids=media_id)
