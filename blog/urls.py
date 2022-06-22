"""
URL mapping for application.
"""

from django.urls import path
from .views import BlogListView, BlogDetailView, BlogDeleteView
from .views import suma, edit_suma, molecule, edit_smiles

urlpatterns = [
    path("post/molecule/", molecule, name="molecule"),
    path("post/suma/", suma, name="suma"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit_suma/", edit_suma, name="suma_edit"),
    path("post/<int:pk>/edit_smiles/", edit_smiles, name="smiles_edit"),
    path("post/", BlogListView.as_view(), name="home"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
]
