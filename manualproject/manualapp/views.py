from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import ListView

from .models import Document


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, "manualapp/document_list.html", {"documents": documents})
