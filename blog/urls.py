"""
URL mapping for application.
"""

from django.urls import path
from .views import BlogListView, BlogDetailView, BlogDeleteView
from .views import suma, edit_blog


urlpatterns = [
    path("post/suma/", suma, name="suma"), 
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", edit_blog, name="post_edit"),
    path("", BlogListView.as_view(), name="home"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
]

