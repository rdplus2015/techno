from django.urls import path
from django.views.generic import ListView

from blog.views import CreatePostView, ListPostsView

urlpatterns = [
    path('createpost/', CreatePostView.as_view(), name='createpost'),
    path('posts', ListPostsView.as_view(), name='posts'),
]
