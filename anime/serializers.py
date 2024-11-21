from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from anime.models import *


class AnimeSerializer(ModelSerializer):
    class Meta:
        model = Anime
        fields = [
            "id",
            "title",
            "description",
            "genre",
            "release_date",
            "duration",
            "thumbnail",
            "video_url"
        ]

    def validate_thumbnail(self, value):
        if value.size > 5 * 1024 * 1024:  # Restrict file size to 5MB
            raise ValidationError("Thumbnail size must be less than 5MB.")
        return value


class UserAnimeListSerializer(ModelSerializer):
    class Meta:
        model = UserAnimeList
        fields = "__all__"  # Include all fields in the UserAnimeList model
        read_only_fields = ["user"]  # The user field will be populated automatically


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"  # Include all fields in the Review model
        read_only_fields = ["user", "anime", "created_at", "updated_at"]  # Auto-populated fields
