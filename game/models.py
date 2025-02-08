from django.db import models
from django.utils.timezone import now, localtime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class Contestant(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ended', 'Ended')
    ]
    
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class GameSession(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)  # ✅ Use string reference
    contestant = models.ForeignKey("Contestant", on_delete=models.CASCADE)  # ✅ Use string reference
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)

    def session_length(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def __str__(self):
        return f"{self.contestant.name} - {self.game.name}"

class Leaderboard(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, null=True, blank=True)  # ✅ Use string reference
    contestant = models.ForeignKey("Contestant", on_delete=models.CASCADE)  # ✅ Use string reference
    score = models.IntegerField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.contestant.name} - {self.score}"

class GamePopularity(models.Model):
    game = models.OneToOneField("Game", on_delete=models.CASCADE)  # ✅ Use string reference
    popularity_score = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def update_popularity(self):
        yesterday = localtime(now()) - timedelta(days=1)
        sessions_yesterday = GameSession.objects.filter(game=self.game, start_time__date=yesterday.date())
        
        w1 = sessions_yesterday.count()
        w2 = GameSession.objects.filter(game=self.game, end_time=None).count()
        w3 = self.game.upvotes
        w4 = max((s.session_length() for s in sessions_yesterday), default=0)
        w5 = sessions_yesterday.count()

        max_daily_players = max(w1, 1)
        max_concurrent_players = max(w2, 1)
        max_upvotes = max(w3, 1)
        max_session_length = max(w4, 1)
        max_daily_sessions = max(w5, 1)

        self.popularity_score = (
            0.3 * (w1 / max_daily_players) +
            0.2 * (w2 / max_concurrent_players) +
            0.25 * (w3 / max_upvotes) +
            0.15 * (w4 / max_session_length) +
            0.1 * (w5 / max_daily_sessions)
        )
        self.save()

@receiver(post_save, sender=Game)
def create_game_popularity(sender, instance, created, **kwargs):
    if created:
        GamePopularity.objects.create(game=instance)