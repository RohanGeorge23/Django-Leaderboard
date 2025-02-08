from rest_framework import serializers
from .models import Contestant, Game, GameSession, Leaderboard, GamePopularity

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'

class GamePopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePopularity
        fields = '__all__'
