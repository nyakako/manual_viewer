from django.apps import AppConfig


class ManualappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manualapp"
    verbose_name = "Manual Viewer"  # 管理画面の表示名
