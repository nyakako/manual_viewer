from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
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
        Department, verbose_name="部署", on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"

    def __str__(self):
        return f"{self.name} - {self.department.name}"


class Task(models.Model):
    name = models.CharField(verbose_name="作業名", max_length=255)
    category = models.ForeignKey(
        Category,
        verbose_name="カテゴリ",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="カテゴリ名、部署名で検索できます。",
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
    document_filename = models.CharField(
        verbose_name="ドキュメントファイル名", max_length=255, null=True, blank=True
    )
    document_content = RichTextUploadingField(verbose_name="ドキュメント内容")
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
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ステップ",
        help_text="手順一覧での表示順です。",
    )
    next_steps = models.ManyToManyField(
        "self",
        verbose_name="後手順",
        blank=True,
        symmetrical=False,
        related_name="previous_steps",
        help_text="手順名、作業名で検索できます。",
    )
    documents = models.ManyToManyField(
        Document,
        verbose_name="関連ドキュメント",
        blank=True,
        help_text="ドキュメント番号、ドキュメントタイトルで検索できます。",
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name = "作業手順"
        verbose_name_plural = "作業手順"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order} - {self.name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, verbose_name="ユーザー名")
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    department = models.ForeignKey(
        Department,
        verbose_name="部署",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="管理者以外は所属している部署のマニュアルのみ参照可能です。",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="利用中",
        help_text="退職者等、利用しないユーザーは削除せずにこのチェックを外してください。",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="管理者",
        help_text="チェックすると管理者サイトへのログイン、すべてのマニュアルの参照が可能になります。",
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="ユーザー", on_delete=models.CASCADE)
    document = models.ForeignKey(
        Document, verbose_name="ドキュメント", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)

    class Meta:
        verbose_name = "ブックマーク"
        verbose_name_plural = "ブックマーク"

    def __str__(self):
        return f"{self.user.username} - {self.document.document_number} - {self.document.document_title}"
