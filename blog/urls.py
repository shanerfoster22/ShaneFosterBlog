from django.urls import path
from . import views
from .views import EditPost

urlpatterns = [
    path("", views.blog, name="blog"),
    path("upload/", views.upload_blog, name="upload_blog"),
    path("edit_post/<str:slug>/", EditPost.as_view(), name="edit_post"),
    path("'<int:id>/delete_post'", views.delete_post, name="delete_post"),
    path("register/", views.register, name="register"),
    path("login/", views.Login, name="Login"),
    path("logout/", views.Logout, name="Logout"),
    path("profile/", views.profile, name="profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
]