from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(verbose_name="部署名", max_length=255)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "部署"
        verbose_name_plural = "部署"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name="カテゴリ名", max_length=255)
    department = models.ForeignKey(
        Department, verbose_name="部署", blank=True, on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(verbose_name="作業名", max_length=255)
    category = models.ForeignKey(
        Category, verbose_name="カテゴリ", blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "作業"
        verbose_name_plural = "作業"

    def __str__(self):
        return self.name


class Document(models.Model):
    document_number = models.CharField(verbose_name="ドキュメント番号", max_length=255)
    document_title = models.CharField(verbose_name="ドキュメントタイトル", max_length=255)
    document_filename = models.CharField(verbose_name="ドキュメントファイル名", max_length=255)
    document_content = models.TextField(verbose_name="ドキュメント内容")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "マニュアル"
        verbose_name_plural = "マニュアル"

    def __str__(self):
        return self.document_number + " " + self.document_title


class Step(models.Model):
    name = models.CharField(verbose_name="手順名", max_length=255)
    task = models.ForeignKey(Task, verbose_name="作業", on_delete=models.CASCADE)
    # previous_steps = models.ManyToManyField(
    #     "self",
    #     verbose_name="前手順",
    #     blank=True,
    #     symmetrical=False,
    #     related_name="is_next_steps",
    # )
    next_steps = models.ManyToManyField(
        "self",
        verbose_name="後手順",
        blank=True,
        symmetrical=False,
        related_name="previous_steps",
    )
    documents = models.ManyToManyField(
        Document,
        verbose_name="関連ドキュメント",
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "作業手順"
        verbose_name_plural = "作業手順"

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    department = models.ForeignKey(
        Department, verbose_name="部署", on_delete=models.PROTECT, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="ユーザー", on_delete=models.CASCADE)
    document = models.ForeignKey(
        Document, verbose_name="ドキュメント", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "ブックマーク"
        verbose_name_plural = "ブックマーク　"
