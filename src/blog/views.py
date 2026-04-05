from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from blog.forms import PostForm, PostCommentForm
from blog.models import Posts, Category, PostComment, SavedPost
from techno.mixims import TechnoLoginRequiredMixin


# --- CATEGORY CRUD VIEWS ---

class CreateCategoryView(TechnoLoginRequiredMixin, CreateView):
    """View to create a new category. Restricts name field and assigns current user as author."""
    model = Category
    fields = ["name"]
    template_name = "blog/admin/categoryCreate.html"
    success_url = reverse_lazy("listecategories")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ListCategoryView(TechnoLoginRequiredMixin, ListView):
    """Displays a list of categories created by the authenticated user."""
    model = Category
    template_name = "blog/admin/categoryList.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user).order_by("name")


class UpdateCategoryView(TechnoLoginRequiredMixin, UpdateView):
    """View to update an existing category. Ensures only the author can edit."""
    model = Category
    template_name = "blog/admin/categoryUpdate.html"
    fields = ["name"]
    success_url = reverse_lazy("listecategories")

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)


class DeleteCategoryView(TechnoLoginRequiredMixin,DeleteView):
    """View to delete a category with author-only permission."""
    model = Category
    template_name = "blog/admin/categoryDelete.html"
    success_url = reverse_lazy("listecategories")

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)


# --- POST CRUD VIEWS ---

class CreatePostView(TechnoLoginRequiredMixin, CreateView):
    """Handles blog post creation using a custom PostForm."""
    model = Posts
    form_class = PostForm
    template_name = "blog/admin/postCreate.html"
    success_url = reverse_lazy("index")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ListPostsView(ListView):
    """Public view to list all blog posts."""
    model = Posts
    template_name = "blog/postList.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Posts.objects.filter(status=True)


class PostDetailView(DetailView):
    """Displays a single post content and injects the comment form/list into the context."""
    model = Posts
    template_name = "blog/postView.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = PostCommentForm()
        context['comments'] = self.object.comments.all()
        return context


class UpdatePostView(TechnoLoginRequiredMixin, UpdateView):
    """Updates a post, restricted to the original author."""
    model = Posts
    template_name = "blog/admin/postUpdate.html"
    form_class = PostForm
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)


class DeletePostView(TechnoLoginRequiredMixin, DeleteView):
    """Deletes a post, restricted to the original author."""
    model = Posts
    template_name = "blog/admin/postDelete.html"
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)


# --- COMMENT VIEWS ---

class CreateCommentView(TechnoLoginRequiredMixin, CreateView):
    """Handles comment submission linked to a specific post via its slug."""
    model = PostComment
    form_class = PostCommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Posts.objects.get(slug=self.kwargs['post_slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('postdetail', kwargs={'slug': self.kwargs['post_slug']})


class DeleteCommentView(TechnoLoginRequiredMixin, DeleteView):
    """Allows users to delete their own comments."""
    model = PostComment
    template_name = "blog/commentDelete.html"

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('postdetail', kwargs={'slug': self.object.post.slug})


# --- INTERACTION & FAVORITES VIEWS ---

class ToggleSavePostView(TechnoLoginRequiredMixin, View):
    """Toggles a post between saved and unsaved status for the current user."""
    def post(self, request, slug):
        post_obj = get_object_or_404(Posts, slug=slug)
        saved_post_qs = SavedPost.objects.filter(user=request.user, post=post_obj)

        if saved_post_qs.exists():
            saved_post_qs.delete()
        else:
            SavedPost.objects.create(user=request.user, post=post_obj)

        return redirect('postdetail', slug=slug)


class SavedPostsListView(TechnoLoginRequiredMixin, ListView):
    """Displays all posts previously saved by the user."""
    model = Posts
    template_name = "blog/savedPosts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Posts.objects.filter(saved_by=self.request.user)


class CreatedPostsListView(TechnoLoginRequiredMixin, ListView):
    """Admin-style view listing only posts created by the logged-in user."""
    model = Posts
    template_name = "blog/admin/createdPosts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)