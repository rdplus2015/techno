from django.urls import path
from django.views.generic import ListView

from blog.views import CreatePostView, ListPostsView, CreateCategoryView, PostDetailView, DeletePostView, \
    ListCategoryView

urlpatterns = [
    # Post URLS
    path('', ListPostsView.as_view(), name='index'),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="postdetail"),
    path('createpost/', CreatePostView.as_view(), name='createpost'),
    path('deletepost/<slug:slug>/', DeletePostView.as_view(), name='deletepost'),

    # Category URLS
    path('createcategory/', CreateCategoryView.as_view(), name='createcategory'),
    path('categories', ListCategoryView.as_view(), name='listecategories'),
    path('createcategory/<int:pk>/edit/', CreateCategoryView.as_view(), name='updatecategory'),
]
