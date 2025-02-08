from django.core.management.base import BaseCommand
from game.models import GamePopularity

class Command(BaseCommand):
    help = "Refresh game popularity scores"

    def handle(self, *args, **kwargs):
        for game_popularity in GamePopularity.objects.all():
            game_popularity.update_popularity()
            game_popularity.save()
        self.stdout.write(self.style.SUCCESS("Game popularity updated successfully"))
