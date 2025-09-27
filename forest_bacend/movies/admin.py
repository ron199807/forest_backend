from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Genre, Movie, UserMovieInteraction

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'created_at')
    search_fields = ('email', 'name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
        ('Terms', {'fields': ('agree_to_terms',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'agree_to_terms', 'is_active', 'is_staff')}
        ),
    )
    
    readonly_fields = ('created_at',)

# Genre Admin
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Movie Admin
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year', 'rating', 'created_at')
    list_filter = ('genre', 'year', 'rating', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    filter_horizontal = ()

# User Movie Interaction Admin
class UserMovieInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'last_watched', 'progress')
    list_filter = ('last_watched',)
    search_fields = ('user__email', 'movie__title')

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(UserMovieInteraction, UserMovieInteractionAdmin)