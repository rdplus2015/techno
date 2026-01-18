from django.urls import path
from django.views.generic import ListView

from blog.views import CreatePostView, ListPostsView, CreateCategoryView, PostDetailView, DeletePostView, \
    ListCategoryView, UpdateCategoryView, DeleteCategoryView, UpdatePostView

urlpatterns = [
    # Post URLS
    path('', ListPostsView.as_view(), name='index'),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="postdetail"),
    path('createpost/', CreatePostView.as_view(), name='createpost'),
    path('deletepost/<slug:slug>/', DeletePostView.as_view(), name='deletepost'),
    path('updatepost/<int:pk>/edit/', UpdatePostView.as_view(), name='updatepost'),
    path('deletepost/<slug:slug>/', DeletePostView.as_view(), name='deletepost'),

    # Category URLS
    path('createcategory/', CreateCategoryView.as_view(), name='createcategory'),
    path('categories/', ListCategoryView.as_view(), name='listecategories'),
    path('updatecategory/<int:pk>/edit/', UpdateCategoryView.as_view(), name='updatecategory'),
    path('deletecategory/<int:pk>/', DeleteCategoryView.as_view(), name='deletecatgory'),
]
