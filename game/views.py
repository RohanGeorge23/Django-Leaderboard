from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.timezone import now, localtime, timedelta
from .models import Contestant, Game, GameSession, Leaderboard, GamePopularity
from .serializers import ContestantSerializer, GameSerializer, GameSessionSerializer, LeaderboardSerializer, GamePopularitySerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.all()
    serializer_class = ContestantSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def update(self, request, *args, **kwargs):
        """Allows Partial Updates (PATCH)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

    @action(detail=True, methods=['post'], url_path='exit')
    def exit_game(self, request, pk=None):
        """Marks the game session as ended by setting end_time."""
        game_session = get_object_or_404(GameSession, pk=pk, end_time=None)
        game_session.end_time = now()
        game_session.save()
        return Response({"message": "Contestant has exited the game.", "end_time": game_session.end_time})

class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    def list(self, request):
        leaderboard = Leaderboard.objects.order_by('-score')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)

class GamePopularityViewSet(viewsets.ModelViewSet):
    queryset = GamePopularity.objects.all()
    serializer_class = GamePopularitySerializer

    @action(detail=True, methods=['get'])
    def get_popularity(self, request, game_id=None):
        """Fetch or create the popularity score for a specific game."""
        game = get_object_or_404(Game, id=game_id)
        
        # Ensure GamePopularity exists
        game_popularity, created = GamePopularity.objects.get_or_create(game=game)
        
        # Update and return the popularity score
        game_popularity.update_popularity()
        serializer = self.get_serializer(game_popularity)
        return Response(serializer.data, status=200)
    
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=['get'], url_path='leaderboard')
    def leaderboard(self, request, pk=None):
        """Retrieve leaderboard for a specific game."""
        game = get_object_or_404(Game, pk=pk)
        leaderboard = Leaderboard.objects.filter(game=game).order_by('-score')
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='popularity')
    def popularity(self, request, pk=None):
        """Retrieve popularity score for a specific game."""
        game = get_object_or_404(Game, pk=pk)
        game_popularity, created = GamePopularity.objects.get_or_create(game=game)
        game_popularity.update_popularity()
        serializer = GamePopularitySerializer(game_popularity)
        return Response(serializer.data, status=200)
