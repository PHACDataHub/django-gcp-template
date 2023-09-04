from django.urls import path

from . import magiclink_views, views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", magiclink_views.EmailLoginView.as_view(), name="email_login"),
    path("logout/", views.logout_view, name="logout"),
    path("_ah/warmup", views.warmup, name="warmup"),
]
