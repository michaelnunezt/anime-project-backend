from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from anime.models import Anime, UserAnimeList, Review
from anime.serializers import AnimeSerializer, UserAnimeListSerializer, ReviewSerializer
from shared.Enums import ProjectEnum
from shared.view_models.custom_responses import APIResponse
from shared.utils import paginate_queryset


class AdminAnimeAPIView(APIView):
    """
    Admin-only API to manage anime (Create, Update, Delete)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]  # Enable multipart form data for file uploads

    def post(self, request):
        """
        Add a new anime (Admin only).
        """
        serializer = AnimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                data=serializer.data,
                message="Anime added successfully."
            ).to_dict(), status=201)
        return Response(APIResponse.error(
            project=ProjectEnum.ANIME,
            message="Failed to add anime",
            error=serializer.errors
        ).to_dict(), status=400)

    def put(self, request, id):
        """
        Update anime details (Admin only).
        """
        try:
            anime = Anime.objects.get(id=id)
            serializer = AnimeSerializer(anime, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(APIResponse.success(
                    project=ProjectEnum.ANIME,
                    data=serializer.data,
                    message="Anime updated successfully."
                ).to_dict())
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Failed to update anime",
                error=serializer.errors
            ).to_dict(), status=400)
        except Anime.DoesNotExist:
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Anime not found."
            ).to_dict(), status=404)

    def delete(self, request, id):
        """
        Delete anime by ID (Admin only).
        """
        try:
            anime = Anime.objects.get(id=id)
            anime.delete()
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                message="Anime deleted successfully."
            ).to_dict())
        except Anime.DoesNotExist:
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Anime not found."
            ).to_dict(), status=404)


class AnimeAPIView(APIView):
    """
    API for normal users to retrieve all anime or a single anime by ID.
    """
    permission_classes = [AllowAny]  # Accessible to both authenticated and non-authenticated users

    def get(self, request, id=None):
        """
        Retrieve all anime or a single anime by ID.
        """
        if id:
            try:
                anime = Anime.objects.get(id=id)
                serializer = AnimeSerializer(anime)
                return Response(APIResponse.success(
                    project=ProjectEnum.ANIME,
                    data=serializer.data
                ).to_dict())
            except Anime.DoesNotExist:
                return Response(APIResponse.error(
                    project=ProjectEnum.ANIME,
                    message="Anime not found."
                ).to_dict(), status=404)
        else:
            page = int(request.query_params.get("page", 1))
            per_page = 10
            anime_queryset = Anime.objects.all()
            paginated_data, total_pages, per_page = paginate_queryset(anime_queryset, page, per_page)
            serializer = AnimeSerializer(paginated_data, many=True)
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                data={
                    "results": serializer.data,
                    "total_pages": total_pages,
                    "per_page": per_page
                }
            ).to_dict())


class UserAnimeListAPIView(APIView):
    """
    API for users to manage their anime list (Retrieve, Add, Remove).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all anime in the user's list with pagination.
        """
        page = int(request.query_params.get("page", 1))
        per_page = 10
        user_list = UserAnimeList.objects.filter(user=request.user)
        paginated_data, total_pages, per_page = paginate_queryset(user_list, page, per_page)
        serializer = UserAnimeListSerializer(paginated_data, many=True)

        return Response(APIResponse.success(
            project=ProjectEnum.ANIME,
            data={
                "results": serializer.data,
                "total_pages": total_pages,
                "per_page": per_page
            }
        ).to_dict())

    def post(self, request):
        """
        Add an anime to the user's list.
        """
        serializer = UserAnimeListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                data=serializer.data,
                message="Anime added to your list."
            ).to_dict(), status=201)
        return Response(APIResponse.error(
            project=ProjectEnum.ANIME,
            message="Failed to add anime to list",
            error=serializer.errors
        ).to_dict(), status=400)

    def delete(self, request, id):
        """
        Remove anime from the user's list by ID.
        """
        try:
            user_list_item = UserAnimeList.objects.get(user=request.user, anime__id=id)
            user_list_item.delete()
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                message="Anime removed from your list."
            ).to_dict())
        except UserAnimeList.DoesNotExist:
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Anime not found in your list."
            ).to_dict(), status=404)


class ReviewAPIView(APIView):
    """
    API for users to manage reviews (Add, Update, Delete).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, anime_id):
        """
        Get reviews of a given anime
        """
        page = int(request.query_params.get("page", 1))
        per_page = 10
        reviews = Review.objects.filter(anime__id=anime_id)
        paginated_data, total_pages, per_page = paginate_queryset(reviews, page, per_page)
        serializer = ReviewSerializer(instance=paginated_data, many=True)
        return Response(APIResponse.success(
            project=ProjectEnum.ANIME,
            data=serializer.data
        ))

    def post(self, request):
        """
        Add a review to an anime.
        """
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                data=serializer.data,
                message="Review added successfully."
            ).to_dict(), status=201)
        return Response(APIResponse.error(
            project=ProjectEnum.ANIME,
            message="Failed to add review",
            error=serializer.errors
        ).to_dict(), status=400)

    def put(self, request, id):
        """
        Edit a review by ID.
        """
        try:
            review = Review.objects.get(id=id, user=request.user)
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(APIResponse.success(
                    project=ProjectEnum.ANIME,
                    data=serializer.data,
                    message="Review updated successfully."
                ).to_dict())
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Failed to update review",
                error=serializer.errors
            ).to_dict(), status=400)
        except Review.DoesNotExist:
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Review not found."
            ).to_dict(), status=404)

    def delete(self, request, id):
        """
        Delete a review by ID.
        """
        try:
            review = Review.objects.get(id=id, user=request.user)
            review.delete()
            return Response(APIResponse.success(
                project=ProjectEnum.ANIME,
                message="Review deleted successfully."
            ).to_dict())
        except Review.DoesNotExist:
            return Response(APIResponse.error(
                project=ProjectEnum.ANIME,
                message="Review not found."
            ).to_dict(), status=404)
