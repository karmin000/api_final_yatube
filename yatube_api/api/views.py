from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Group, Post
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnlyPermission
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("group",)
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        """Возвращает комментарии конкретного поста."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        """Создаёт комментарий от имени текущего пользователя."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки подписок."""
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("user__username", "following__username")
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Используем related_name="follower" из модели Subscription."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Создаём подписку от имени текущего пользователя."""
        serializer.save(user=self.request.user)
