import datetime as dt
import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
        read_only_field = ('role',)


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор данных регистрации."""

    username = serializers.CharField(
        validators=(
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Имя занято.'
            ),
        ),
        required=True,
    )

    email = serializers.EmailField(
        validators=(
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Email уже зарегистрирован.'
            ),
        ),
        required=True,
    )

    def validate_username(self, value):
        """Валидация поля username."""

        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Имя зарезервировано."
            )

        if not re.match(r'^[\w.@+-]+\Z', value):  # шаблон из задания, может \Z
            #  r'^[\w.@+-]+)$' # шаблон из примеров
            #  r'^users/(?P<username>[\w.@+-]+)$' # шаблон для username
            raise serializers.ValidationError(
                "Неверный формат имени."
            )

        return value


class AuthetificationSerializer(serializers.Serializer):
    """Сериализатор данных аутентификации."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений метод POST, PATCH, DELETE."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год публикации!')
        return value

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений метод GET."""

    genre = GenreSerializer(read_only=True, many=True,)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    class Meta:
        fields = ('id', 'text', 'score', 'author', 'title', 'pub_date',)
        model = Review

    def validate(self, data):
        request = self.context['request']
        author = request.user
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
