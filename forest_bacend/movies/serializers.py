from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Movie, Genre, UserMovieInteraction

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password', 'confirm_password', 'agree_to_terms')
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],  # Using email as username
            password=validated_data['password'],
            name=validated_data['name'],
            agree_to_terms=validated_data['agree_to_terms']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include email and password.")
        
        return data

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'description', 'image', 'rating', 'year')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class MovieDetailSerializer(MovieSerializer):
    video_url = serializers.SerializerMethodField()
    
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ('video_url',)
    
    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video_file:
            return request.build_absolute_uri(obj.video_file.url)
        return None

class UserMovieInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieInteraction
        fields = '__all__'