from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from blog.forms import PostForm, PostCommentForm
from blog.models import Posts, Category, PostComment
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Posts, SavedPost


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On ajoute le formulaire vierge
        context['comment_form'] = PostCommentForm()
        # On récupère les commentaires liés à ce post
        context['comments'] = self.object.comments.all()  # Nécessite related_name='comments' dans le modèle
        return context



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



# comments
class CreateCommentView(CreateView):
    model = PostComment
    form_class = PostCommentForm

    def form_valid(self, form):
        # On lie l'auteur
        form.instance.author = self.request.user
        # On lie le post grâce à l'ID dans l'URL (ex: <int:post_id>)
        form.instance.post = Posts.objects.get(slug=self.kwargs['post_slug'])
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige vers le post après le commentaire
        return reverse_lazy('postdetail', kwargs={'slug': self.kwargs['post_slug']})


class DeleteCommentView(DeleteView):
    model = PostComment
    template_name = "blog/commentDelete.html"

    def get_queryset(self):
        # Sécurité : on ne peut supprimer que ses propres commentaires
        return self.model.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('postdetail', kwargs={'slug': self.object.post.slug})




class ToggleSavePostView(View):
    def post(self, request, slug):
        post_obj = get_object_or_404(Posts, slug=slug)
        # On cherche si l'objet existe
        saved_post_qs = SavedPost.objects.filter(user=request.user, post=post_obj)

        if saved_post_qs.exists():
            saved_post_qs.delete()  # On retire des favoris
        else:
            SavedPost.objects.create(user=request.user, post=post_obj)  # On ajoute

        return redirect('postdetail', slug=slug)

class SavedPostsListView(ListView):
    model = Posts
    template_name = "blog/savedPosts.html"
    context_object_name = "posts"

    def get_queryset(self):
        # On récupère les posts où l'utilisateur actuel est présent dans 'saved_by'
        return Posts.objects.filter(saved_by=self.request.user)

