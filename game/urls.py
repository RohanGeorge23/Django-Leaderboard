from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContestantViewSet, GameViewSet, GameSessionViewSet, LeaderboardViewSet, GamePopularityViewSet
)

router = DefaultRouter()
router.register(r'contestants', ContestantViewSet)
router.register(r'games', GameViewSet)
router.register(r'game_sessions', GameSessionViewSet)
router.register(r'leaderboard', LeaderboardViewSet)
router.register(r'game_popularity', GamePopularityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
