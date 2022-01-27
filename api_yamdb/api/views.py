from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reviews.models import Category, Genre, Review, Title, Comment
from .filters import TitleFilter
from .permissions import (AdminOrSuperuser, IsAdminOrReadOnly,
                          IsUserAnonModerAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, InputTitleSerializer,
                          OutputTitleSerializer, ReviewSerializer,
                          UserInfoSerializer, UserSerializer)
from .paginators import FourPerPagePagination

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # https://www.django-rest-framework.org/api-guide/generic-views/#attributes
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperuser,)
    pagination_class = FourPerPagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        serializer_class=UserInfoSerializer,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@action(detail=True, methods=['LIST', 'POST', 'DEL'])
class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = FourPerPagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


@action(detail=True, methods=['LIST', 'POST', 'DEL'])
class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = FourPerPagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.select_related('category')
        .prefetch_related('genre')
        .annotate(rating=Avg('reviews__score'))
        .order_by('id')
    )
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = FourPerPagePagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', 'year', 'category', 'genre')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OutputTitleSerializer
        return InputTitleSerializer


class ReViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    serializer_class = ReviewSerializer
    pagination_class = FourPerPagePagination

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return Review.objects.filter(
            title_id=self.kwargs.get('title_id')
        ).select_related('author')

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    serializer_class = CommentSerializer
    pagination_class = FourPerPagePagination

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return Comment.objects.filter(
            review__title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        ).select_related('author')

    def perform_create(self, serializer):
        review = self._get_review()
        author = self.request.user
        serializer.save(author=author, review=review)
