from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, EmailAuthenticationForm
from .models import Bookmark, Category, Document, Step, Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks.html"
    context_object_name = "task_list"

    def get_queryset(self):
        user_department = self.request.user.department
        search_input_text = self.request.GET.get("search", "")
        tasks = Task.objects.filter(category__department=user_department)
        if search_input_text:
            tasks = tasks.filter(
                Q(name__icontains=search_input_text)
                | Q(step__name__icontains=search_input_text)
            )
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(department=self.request.user.department)
        search_input_text = self.request.GET.get("search", "")
        if search_input_text:
            task_ids = [task.id for task in context["task_list"]]
            categories = [
                category
                for category in categories
                if category.task_set.filter(id__in=task_ids).exists()
            ]
        context["category_list"] = categories
        context["search"] = search_input_text
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
            context["task_name"] = related_step.task.name
            context["step_name"] = related_step.name
            context["step_order"] = related_step.order
            context["related_documents"] = related_step.documents.exclude(
                id=self.object.id
            )
        else:
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


class BookmarkView(View):
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
