from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.jinja"


def logout_view(request):
    logout(request)
    return redirect("index")


def warmup(request):
    return HttpResponse(status=200)
