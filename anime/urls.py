from django.urls import path
from anime.views import *

urlpatterns = [
    path('anime/', AnimeAPIView.as_view(), name='anime-list'),  # GET all anime
    path('anime/<int:id>/', AnimeAPIView.as_view(), name='anime-detail'),  # GET single anime
    path('admin/anime/', AdminAnimeAPIView.as_view(), name='admin-anime-create'),  # POST anime
    path('admin/anime/<int:id>/', AdminAnimeAPIView.as_view(), name='admin-anime-update-delete'),  # PUT, DELETE anime
    path('my-list/', UserAnimeListAPIView.as_view(), name='user-anime-list'),  # GET, POST anime list
    path('my-list/<int:id>/', UserAnimeListAPIView.as_view(), name='user-anime-list-delete'),  # DELETE anime from list
    path("reviews/<int:anime_id>", ReviewAPIView.as_view(), name='reviews'),  # GET reviews of any anime
    path('reviews/', ReviewAPIView.as_view(), name='reviews'),  # POST reviews
    path('reviews/<int:id>/', ReviewAPIView.as_view(), name='review-detail'),  # PUT, DELETE reviews
]