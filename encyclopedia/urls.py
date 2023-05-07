from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("wiki/search/entry", views.search_entry, name="search_entry"),
    path("wiki/create/new_entry", views.create_new_entry, name="create_new_entry"),
    path("wiki/edit/<str:title>", views.edit_entry, name="edit_entry"),
    path("wiki/random/entry", views.random_entry, name="random_entry")
]
