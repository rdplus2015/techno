from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from blog.forms import PostForm
from blog.models import Posts, Category


# Create your views here.

# Categories crud
class CreateCategoryView(CreateView):
    model = Category
    fields = ["name"] # Use field instead pf a form
    template_name = "blog/categoryCreate.html"
    success_url = reverse_lazy("listecategories")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ListCategoryView(ListView):
    model = Category
    fields = ["name"]
    template_name = "blog/categoryList.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user).order_by("name")


class UpdateCategoryView(UpdateView):
    model = Category
    template_name = "blog/categoryUpdate.html"
    fields = ["name"]
    success_url = reverse_lazy("listecategories")

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteCategoryView(DeleteView):
    model = Category
    template_name = "blog/categoryDelete.html"
    success_url = reverse_lazy("listecategories")

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)


# Posts view
class CreatePostView(CreateView):
    model = Posts
    form_class = PostForm
    template_name = "blog/postCreate.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ListPostsView(ListView):
    model = Posts
    template_name = "blog/postList.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Posts
    template_name = "blog/postView.html"
    context_object_name = "post"


class UpdatePostView(UpdateView):
    model = Posts
    template_name = "blog/postUpdate.html"
    form_class = PostForm
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeletePostView(DeleteView):
    model = Posts
    template_name = "blog/postDelete.html"
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)


