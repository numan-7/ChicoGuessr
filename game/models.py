from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.00)

    class Meta:
        ordering = ['-score', '-average_score']

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    high_score = models.IntegerField(default=0)
    lowest_score = models.IntegerField(default=0) 
    average_score = models.FloatField(default=0.00)
    last_score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class SearchStats(models.Model):
    searcher = models.ForeignKey(User, on_delete=models.CASCADE)
    searched_user_score = models.ForeignKey(Score, on_delete=models.CASCADE)

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    round = models.IntegerField(default=0)
    guesses = models.JSONField(default=list)
    random_location = models.CharField(max_length=100, default="")

    def save_game(self, score, round, guesses, random_location=""):
        self.score = score
        self.round = round
        self.guesses = guesses
        self.random_location = random_location
        self.save()
        score_instance, _ = Score.objects.get_or_create(user=self.user)
        
        if round == 5:
            score_instance.games_played += 1
            score_instance.last_score = self.score

            if score_instance.lowest_score == 0 or score < score_instance.lowest_score:
                score_instance.lowest_score = score

            if score > score_instance.high_score:
                score_instance.high_score = score

            total_score = float(score_instance.average_score) * (score_instance.games_played - 1) + self.score
            score_instance.average_score = total_score / score_instance.games_played

            # Update the corresponding Leaderboard object with the new average score
            leaderboard, _ = Leaderboard.objects.get_or_create(user=self.user)
            leaderboard.score = score_instance.high_score
            leaderboard.average_score = score_instance.average_score
            leaderboard.save()

        score_instance.save()

class ThanksHerring(models.Model):
    hello = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)