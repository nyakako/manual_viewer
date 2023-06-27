from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import views
from .views import (
    BookmarkListView,
    BookmarkView,
    CustomLoginView,
    CustomRegisterView,
    DocumentDetailView,
    DocumentListView,
    GetStepsAndDocumentsView,
    HomeView,
    TaskListView,
    TaskStepsView,
)

# app_name = "manualapp"

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("task/<int:pk>/steps/", TaskStepsView.as_view(), name="task_step_list"),
    path("document/<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("document/<int:pk>/bookmark/", BookmarkView.as_view(), name="bookmark"),
    path(
        "get_steps_and_documents/",
        GetStepsAndDocumentsView.as_view(),
        name="get_steps_and_documents",
    ),
    path("bookmarks/", BookmarkListView.as_view(), name="bookmark_list"),
    path("documents/", DocumentListView.as_view(), name="document_list"),
    path("home/", HomeView.as_view(), name="home"),
]
