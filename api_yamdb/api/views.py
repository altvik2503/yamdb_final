import uuid

from api_yamdb.settings import EMAIL_FROM_DEFAULT
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, response, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
    User,
)

from .mixins import CreateDestroyListViewSet
from .filter import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorAdminModeratorOrReadOnly
)
from .serializers import (
    AuthetificationSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    RegistrationSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    """View-функция url auth/signup/."""

    username = request.data.get('username')
    email = request.data.get('email')

    try:
        user = User.objects.get(username=username, email=email)

        confirmation_code = str(uuid.uuid4())
        user.confirmation_code = confirmation_code
        user.save()

        data = request.data

    except ObjectDoesNotExist:
        serializer = RegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            # Данные некорректны
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        confirmation_code = str(uuid.uuid4())

        User.objects.get_or_create(
            username=username,
            email=email,
            confirmation_code=confirmation_code,
        )
        data = serializer.data

    send_mail(
        username,
        confirmation_code,
        EMAIL_FROM_DEFAULT,
        (email,),
        fail_silently=False,
    )

    return response.Response(
        data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    """View-функция url auth/token/."""

    serializer = AuthetificationSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(
            # Данные некорректны
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)

    confirmation_code = serializer.validated_data.get('confirmation_code')
    if confirmation_code != str(user.confirmation_code):
        # Неверный код подтверждения
        return response.Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    return response.Response(
        {'token': str(RefreshToken.for_user(user).access_token)},
        status=status.HTTP_200_OK,
    )


class UsersViewSet(viewsets.ModelViewSet):
    """Класс вьюсета модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=('get', 'patch',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def me(self, request):
        """Обработка своей учётной записи."""

        username = request.user.username
        user = get_object_or_404(User, username=username)

        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return response.Response(
                    # Данные некорректны
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(
                role=user.role,
                confirmation_code=user.confirmation_code,
            )

        serializer = UserSerializer(user)
        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CategoryViewSet(CreateDestroyListViewSet):
    """Класс вьюсета модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class GenreViewSet(CreateDestroyListViewSet):
    """Класс вьюсета модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Класс вьюсета модели Title."""

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс вьюсета модели Review с определением queryset`а."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс вьюсета модели Comment с определением queryset`а."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
