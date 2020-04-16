from django.core.management.base import BaseCommand
from django.conf import settings
import os
from core.models import RealTweet, FakeTweet
import markovify


class Command(BaseCommand):
    help = 'Populate the app with an equal number of real and fake tweets'

    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'data')

        with open(os.path.join(data_path, 'cleaned_tweets.txt'), 'r') as f:
            for line in f.readlines():
                RealTweet.objects.get_or_create(content=line)

        real_tweet_count = RealTweet.objects.count()

        with open(os.path.join(data_path, 'model.json')) as f:
            model_json = f.read()

        model = markovify.Text.from_json(model_json)

        for i in range(real_tweet_count):
            FakeTweet.objects.get_or_create(content=model.make_short_sentence(280))
