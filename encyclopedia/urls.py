from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.wiki, name="wiki"),
    path("newpage/", views.create, name="newpage"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.rand_page, name="random")
]
