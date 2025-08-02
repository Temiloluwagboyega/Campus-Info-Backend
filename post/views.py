from rest_framework import viewsets, permissions, status
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


  def get_queryset(self):
    return Comment.objects.filter(post_id=self.request.query_params.get('post_id'))


  def perform_create(self, serializer):
    serializer.save(user=self.request.user)