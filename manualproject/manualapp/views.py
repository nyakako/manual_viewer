from datetime import timedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, EmailAuthenticationForm
from .models import Bookmark, Category, Document, Step, Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all().order_by("-created_at")
        else:
            return Task.objects.filter(
                category__department=self.request.user.department
            ).order_by("-created_at")


class TaskStepsView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_step_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["steps"] = self.object.step_set.all().order_by("order")
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "document_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_bookmarked"] = Bookmark.objects.filter(
            user=self.request.user, document=self.object
        ).exists()
        related_step = self.object.step_set.first()
        if related_step is not None:
            context["task_id"] = related_step.task.id
            context["task_name"] = related_step.task.name
            context["step_name"] = related_step.name
            context["step_order"] = related_step.order
            context["related_documents"] = related_step.documents.exclude(
                id=self.object.id
            )
        else:
            context["task_id"] = None
            context["task_name"] = None
            context["step_name"] = None
            context["related_documents"] = Document.objects.none()
        return context


class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = "login.html"
    redirect_authenticated_user = True


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration.html"
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.redirect_authenticated_user:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class BookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        document = get_object_or_404(Document, pk=kwargs["pk"])
        bookmark, created = Bookmark.objects.get_or_create(
            user=self.request.user, document=document
        )

        if created:
            message = "Bookmark added."
        else:
            bookmark.delete()
            message = "Bookmark removed."

        return JsonResponse({"message": message})


class GetStepsAndDocumentsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get("task_id")
        if task_id is not None:
            task = Task.objects.get(id=task_id)
            steps = list(Step.objects.filter(task=task).values())
            documents = list(
                Document.objects.filter(step__task=task).distinct().values()
            )
            return JsonResponse({"steps": steps, "documents": documents})
        else:
            return JsonResponse({"steps": [], "documents": []})


class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = "bookmark_list.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by("-created_at")


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = "document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        # Check if the user is an admin
        if self.request.user.is_staff:
            # If the user is an admin, return all manuals
            documents = Document.objects.annotate(
                department_name=F("step__task__category__department__name"),
                category_name=F("step__task__category__name"),
                task_name=F("step__task__name"),
            ).order_by("-updated_at")
        else:
            # If the user is not an admin, return only the manuals related to the user's department
            user_department = self.request.user.department
            documents = (
                Document.objects.filter(
                    step__task__category__department=user_department
                )
                .annotate(
                    department_name=F("step__task__category__department__name"),
                    category_name=F("step__task__category__name"),
                    task_name=F("step__task__name"),
                )
                .order_by("-updated_at")
            )

        return documents.distinct()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        two_weeks_ago = now - timedelta(weeks=2)

        if self.request.user.is_staff:
            context["recent_documents"] = Document.objects.filter(
                updated_at__gte=two_weeks_ago
            ).order_by("-updated_at")[:10]
            context["recent_bookmarks"] = Bookmark.objects.order_by("-created_at")[:10]
        else:
            user_department = self.request.user.department
            context["recent_documents"] = Document.objects.filter(
                step__task__category__department=user_department,
                updated_at__gte=two_weeks_ago,
            ).order_by("-updated_at")[:10]
            context["recent_bookmarks"] = Bookmark.objects.filter(
                user=self.request.user,
                document__step__task__category__department=user_department,
            ).order_by("-created_at")[:10]

        return context
