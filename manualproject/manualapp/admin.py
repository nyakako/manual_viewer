from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import *


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        """
        モデルの表示順を任意に変更
        """
        ordering = {
            "作業": 1,
            "作業手順": 2,
            "マニュアル": 3,
            "部署": 4,
            "カテゴリ": 5,
            "ユーザー": 6,
            "ブックマーク": 7,
        }

        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app["models"].sort(key=lambda x: ordering[x["name"]])

        return app_list


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "department",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "change_password")}),
        ("情報", {"fields": ("username", "department")}),
        (
            "権限",
            {
                "fields": ("is_active", "is_staff"),
            },
        ),
        ("日付", {"fields": ("date_joined", "last_login")}),
    )
    readonly_fields = (
        "change_password",
        "date_joined",
        "last_login",
    )
    list_display = [
        "email",
        "username",
        "department",
        "is_staff",
        "is_active",
        "last_login",
    ]
    search_fields = ("email", "username")
    list_filter = ("department", "is_staff", "is_active", "last_login")
    ordering = ("id",)

    def change_password(self, obj):
        return format_html(
            '<a class="button" href="/admin/manualapp/customuser/{}/password/">パスワード変更</a>',
            obj.id,
        )

    change_password.short_description = "パスワード"


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "get_category", "get_department"]
    search_fields = ["name"]
    list_filter = ["category__department__name", "category__name"]

    def get_department(self, obj):
        return obj.category.department.name

    get_department.short_description = "部署"

    def get_category(self, obj):
        return obj.category.name

    get_category.short_description = "カテゴリ"


class StepAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "get_task", "get_category", "get_department"]
    search_fields = ["name"]
    list_filter = [
        "task__category__department__name",
        "task__category__name",
        "task__name",
    ]

    def get_task(self, obj):
        return obj.task.name

    get_task.short_description = "作業名"

    def get_category(self, obj):
        return obj.task.category.name

    get_category.short_description = "カテゴリ"

    def get_department(self, obj):
        return obj.task.category.department.name

    get_department.short_description = "部署"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "department"]
    search_fields = ["name"]
    list_filter = [
        "department",
    ]


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "document_number",
        "document_title",
        "get_steps",
        "get_task_name",
        "get_category_name",
        "get_department_name",
    ]
    search_fields = ["document_number", "document_title"]
    list_filter = [
        "step__task__category__department__name",
        "step__task__category__name",
        "step__task__name",
        "step__name",
    ]

    def get_steps(self, obj):
        return ", ".join([str(step) for step in obj.step_set.all()])

    get_steps.short_description = "手順"

    def get_task_name(self, obj):
        step = obj.step_set.first()
        return step.task.name if step else "-"

    get_task_name.short_description = "作業名"

    def get_category_name(self, obj):
        step = obj.step_set.first()
        return step.task.category.name if step else "-"

    get_category_name.short_description = "カテゴリ名"

    def get_department_name(self, obj):
        step = obj.step_set.first()
        return step.task.category.department.name if step else "-"

    get_department_name.short_description = "部署名"


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["get_user_name", "get_document_number", "get_document_title"]
    search_fields = [
        "user",
        "document__document_number",
        "document__document_title",
    ]
    list_filter = ["user__username", "document__document_title"]

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = "ユーザー名"

    def get_document_number(self, obj):
        return obj.document.document_number

    get_document_number.short_description = "ドキュメント番号"

    def get_document_title(self, obj):
        return obj.document.document_title

    get_document_title.short_description = "ドキュメントタイトル"


mysite = CustomAdminSite()
admin.site = mysite

admin.site.register(CustomUser, CustomUserAdmin, site=mysite)
admin.site.register(Department, DepartmentAdmin, site=mysite)
admin.site.register(Category, CategoryAdmin, site=mysite)
admin.site.register(Task, TaskAdmin, site=mysite)
admin.site.register(Step, StepAdmin, site=mysite)
admin.site.register(Document, DocumentAdmin, site=mysite)
admin.site.register(Bookmark, BookmarkAdmin, site=mysite)
