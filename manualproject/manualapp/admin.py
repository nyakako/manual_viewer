from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import *


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
    # list_display = ["order", "name"]
    search_fields = ["name"]

    list_filter = ["category__department__name", "category__name"]


class StepAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = [
        "task__category__department__name",
        "task__category__name",
        "task__name",
    ]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = [
        "department",
    ]


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ["document_number", "document_title"]
    list_filter = [
        "step__task__category__department__name",
        "step__task__category__name",
        "step__task__name",
        "step__name",
    ]


class BookmarkAdmin(admin.ModelAdmin):
    list_filter = [
        "user__username",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
