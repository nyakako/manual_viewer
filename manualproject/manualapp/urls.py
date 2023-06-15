from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .views import DocumentDetailView, MyLoginView, TaskListView

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("document/<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
]
