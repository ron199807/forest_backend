from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Movie, CustomUser, UserMovieInteraction
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    MovieSerializer,
    MovieDetailSerializer,
    UserMovieInteractionSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Movie.objects.all().order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        return queryset

class MovieDetailView(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Movie.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class HeroMoviesView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Get featured movies for hero section
        hero_movies = Movie.objects.filter(rating__gte=8.0).order_by('-rating')[:5]
        serializer = MovieSerializer(hero_movies, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def stream_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Track user interaction
    interaction, created = UserMovieInteraction.objects.get_or_create(
        user=request.user,
        movie=movie
    )
    interaction.save()
    
    # For actual streaming, you might want to use django-range-response
    # or implement proper streaming logic
    response = HttpResponse(movie.video_file, content_type='video/mp4')
    response['Content-Disposition'] = f'inline; filename="{movie.title}.mp4"'
    return response

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    response = HttpResponse(movie.video_file, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{movie.title}.mp4"'
    return response

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'username': user.username
        })
    

class UserMovieInteractionView(generics.ListCreateAPIView):
    serializer_class = UserMovieInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserMovieInteraction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# views.py
from django.conf import settings
from django.http import JsonResponse

def debug_media(request):
    return JsonResponse({
        'media_root': str(settings.MEDIA_ROOT),
        'base_dir': str(settings.BASE_DIR),
        'image_path': str(settings.MEDIA_ROOT / 'movie_images' / 'eternal-wilderness.jpg'),
    })        