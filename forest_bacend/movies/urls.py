from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', views.UserProfileView.as_view(), name='profile'),
    
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/hero/', views.HeroMoviesView.as_view(), name='hero-movies'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<str:movie_id>/stream/', views.stream_movie, name='stream-movie'),
    path('movies/<str:movie_id>/download/', views.download_movie, name='download-movie'),
    path('deburg-media/', views.debug_media, name='debug-media'),
]