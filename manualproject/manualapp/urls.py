from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import (
    BookmarkView,
    CustomLoginView,
    CustomRegisterView,
    DocumentDetailView,
    TaskListView,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("document/<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("document/<int:pk>/bookmark/", BookmarkView.as_view(), name="bookmark"),
]
