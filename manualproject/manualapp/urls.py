from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

# from .views import MyLoginView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("documents/", views.document_list, name="document_list"),
]
