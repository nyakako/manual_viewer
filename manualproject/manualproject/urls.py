"""
URL configuration for manualproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("manualapp.urls")),
    path("manualapp/", include("manualapp.urls")),
]

# ckeditor_uploader用
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ローカル環境、Debug=Falseで動作確認する為の設定
urlpatterns += (
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
)

admin.site.site_header = "Manual Viewer 管理者用画面"  # default: "Django administration"
# admin.site.index_title = "Manual Viewer 管理者用画面"  # default: "Site administration"
admin.site.site_title = "Manual Viewer 管理者用画面"  # default: "Django site admin"
