from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer



class IsBroadcaster(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.profile.role == 'broadcaster'
  

class IsStudent(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.profile.role == 'student'
  

class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all().order_by('-created_at')
  serializer_class = PostSerializer
  lookup_field = 'slug'

  def get_permissions(self):
    if self.action in ['create', 'update', 'partial_update', 'destroy']:
      return [permissions.IsAuthenticated(), IsBroadcaster()]   
    return[permissions.IsAuthenticated()]
  

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
  serializer_class = LikeSerializer
  permission_classes  = [permissions.IsAuthenticated, IsStudent]


  def get_queryset(self):
    return Like.objects.filter(user=self.request.user)
  

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)



class CommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticated]
  lookup_field = 'slug'

  def get_queryset(self):
    # For nested routing, get post from URL parameters
    if hasattr(self, 'kwargs') and 'post_pk' in self.kwargs:
      post_slug = self.kwargs['post_pk']
      try:
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)
      except Post.DoesNotExist:
        return Comment.objects.none()
    
    # Fallback for direct access
    post_slug = self.request.query_params.get('post_slug')
    if post_slug:
      try:
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)
      except Post.DoesNotExist:
        return Comment.objects.none()
    return Comment.objects.all()

  def perform_create(self, serializer):
    # For nested routing, get post from URL parameters
    if hasattr(self, 'kwargs') and 'post_pk' in self.kwargs:
      post_slug = self.kwargs['post_pk']
      try:
        post = Post.objects.get(slug=post_slug)
        serializer.save(user=self.request.user, post=post)
        return
      except Post.DoesNotExist:
        raise serializers.ValidationError("Post not found")
    
    # Fallback for direct access
    post_slug = self.request.data.get('post_slug')
    if post_slug:
      try:
        post = Post.objects.get(slug=post_slug)
        serializer.save(user=self.request.user, post=post)
      except Post.DoesNotExist:
        raise serializers.ValidationError("Post not found")
    else:
      raise serializers.ValidationError("post_slug is required")