from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from blog.forms import PostForm
from blog.models import Posts


# Create your views here.

class CreatePostView(CreateView):
    model = Posts
    form_class = PostForm
    template_name = "blog/postCreate.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ListPostsView(ListView):
    model = Posts
    template_name = "blog/postList.html"
    context_object_name = "posts"
