from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from blog.forms import PostForm
from blog.models import Posts, Category


# Create your views here.
# Category crud
class CreateCategoryView(CreateView):
    model = Category
    fields = ["name"] # Use field instead pf a form
    template_name = "blog/categorycreate.html"
    success_url = reverse_lazy("createpost")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateCategoryView(UpdateView):
    model = Category
    template_name = "blog/categoryupdate.html"


class CreatePostView(CreateView):
    model = Posts
    form_class = PostForm
    template_name = "blog/postCreate.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    pass


class ListPostsView(ListView):
    model = Posts
    template_name = "blog/postList.html"
    context_object_name = "posts"
