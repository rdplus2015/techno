from django.urls import path
from blog.views import (
    CreatePostView, ListPostsView, CreateCategoryView, PostDetailView,
    DeletePostView, ListCategoryView, UpdateCategoryView, DeleteCategoryView,
    UpdatePostView, CreateCommentView, DeleteCommentView, ToggleSavePostView,
    SavedPostsListView, CreatedPostsListView
)

urlpatterns = [
    # --- BLOG POSTS ---
    # Public home page listing all posts
    path('', ListPostsView.as_view(), name='index'),

    # Detailed view of a specific post using its unique slug
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="postdetail"),

    # Creation, update, and deletion of posts
    path('createpost/', CreatePostView.as_view(), name='createpost'),
    path('updatepost/<int:pk>/edit/', UpdatePostView.as_view(), name='updatepost'),
    path('deletepost/<slug:slug>/', DeletePostView.as_view(), name='deletepost'),

    # List of posts created specifically by the logged-in user
    path('createdPosts/', CreatedPostsListView.as_view(), name='createdposts'),

    # --- CATEGORIES ---
    # List all categories and management (create/update/delete)
    path('categories/', ListCategoryView.as_view(), name='listecategories'),
    path('createcategory/', CreateCategoryView.as_view(), name='createcategory'),
    path('updatecategory/<int:pk>/edit/', UpdateCategoryView.as_view(), name='updatecategory'),
    path('deletecategory/<int:pk>/', DeleteCategoryView.as_view(), name='deletecategory'),

    # --- COMMENTS ---
    # Create a comment linked to a post slug
    path('testcomment/<slug:post_slug>/', CreateCommentView.as_view(), name='testcomment'),

    # Delete a comment using its primary key (ID)
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='deletecomment'),

    # --- SAVED POSTS / FAVORITES ---
    # Toggle functionality to save or unsave a post
    path('post/<slug:slug>/save/', ToggleSavePostView.as_view(), name='savepost'),

    # View to display all posts saved by the user
    path('savedposts/', SavedPostsListView.as_view(), name='savedposts'),
]