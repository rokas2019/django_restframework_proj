from rest_framework import generics, permissions, exceptions, mixins, status
from rest_framework.response import Response
from . import models
from . import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class PostListCreateAPI(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, *kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot delete posts not of your own').capitalize())

    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.update(request, *args, *kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot change posts not of your own').capitalize())


class CommentListCreateAPI(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.Comment.objects.filter(post=post)


class CommentDetailUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot delete comments not of your own').capitalize())

    def put(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot update comments not of your own').capitalize())


class PostLikeCreateAPI(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.PostLike.objects.filter(user=self.request.user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise exceptions.ValidationError(_('You have already liked this post').capitalize())
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.ValidationError(_('You havent liked this post yet').capitalize())


class UserCrateAPI(generics.CreateAPIView, mixins.DestroyModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = get_user_model().objects.filter(id=self.request.user)
            if request.exists():
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise exceptions.ValidationError(_('unauthenticated user cannot be deleted').capitalize())
