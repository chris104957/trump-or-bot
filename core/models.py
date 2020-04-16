from django.db import models
import random


def get_choice():
    return random.choice(['A', 'B', 'C', 'D'])


class TweetManager(models.Manager):
    def select_random(self, **filters):
        ids = self.filter(**filters).values_list('pk', flat=True)
        return self.get(pk=random.choice(ids))


class GameManager(models.Manager):
    def create_game(self, player_name: str):
        player, _ = Player.objects.get_or_create(name=player_name.lower())
        obj = self.create(player=player)

        for i in range(20):
            q = Question.objects.create(
                game=obj,
                real_tweet=RealTweet.objects.select_random(content__gte=100),
            )
            for i in range(3):
                q.fake_tweets.add(FakeTweet.objects.select_random())

        return obj


class RealTweet(models.Model):
    objects = TweetManager()
    content = models.TextField()

    def __str__(self):
        return self.content


class FakeTweet(models.Model):
    objects = TweetManager()
    content = models.TextField()

    def __str__(self):
        return self.content


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Game(models.Model):
    objects = GameManager()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def get_question_by_index(self, index):
        return self.questions.all()[index - 1]

    @property
    def score(self):
        return self.questions.filter(answer='REAL').count()


class Question(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='questions')
    real_tweet = models.ForeignKey(RealTweet, on_delete=models.CASCADE)
    fake_tweets = models.ManyToManyField(FakeTweet)
    correct_answer = models.CharField(max_length=2, default=get_choice)

    answer = models.CharField(
        max_length=10, choices=(('REAL', 'REAL'), ('FAKE', 'FAKE')), blank=True
    )
