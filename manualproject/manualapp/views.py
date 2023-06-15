from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Document, Step, Task


class MyLoginView(LoginView):
    template_name = "login.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user_department = self.request.user.department
        return Task.objects.filter(category__department=user_department)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "document_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
