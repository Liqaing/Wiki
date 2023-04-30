from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<int:title>", views.entry_page, name="entry_page"),
    path("wiki/entry", views.search_entry, name="search_entry")
]
