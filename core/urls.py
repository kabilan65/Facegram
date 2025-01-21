from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('settings/', views.settings, name="settings"),
    path('new_post/', views.new_post, name="new_post"),
    path('post-detail/<int:pk>/', views.post_detail, name="post_detail"),
    path('follow/', views.follow, name="follow"),
    path('search/', views.search, name="search"),
    path('delete_post/<int:pk>/', views.delete_post, name="delete_post"),
    path('profile/<str:username>/', views.user_profile, name="profile"),
    path('like-post/<int:pk>/', views.like_post, name="like-post"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
]