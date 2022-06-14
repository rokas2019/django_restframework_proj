from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.PostListCreateAPI.as_view()),
    path('api/posts/<int:pk>/', views.PostDetailUpdateDeleteAPI.as_view()),
    path('api/posts/<int:pk>/comments/', views.CommentListCreateAPI.as_view()),
    path('api/comments/<int:pk>/', views.CommentDetailUpdateDeleteAPI.as_view()),
    path('api/posts/<int:pk>/like', views.PostLikeCreateAPI.as_view()),
    path('api/signup/', views.UserCrateAPI.as_view()),


]
