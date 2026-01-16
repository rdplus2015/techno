from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Category model.
    - name: human-readable label
    - slug: URL-friendly identifier (auto-generated if empty)
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """
        Automatically generate the slug from the name if not provided.
        """
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Posts(models.Model):
    """
    Posts model.
    - author: post author (nullable if the user is deleted)
    - category: many-to-many relationship with Category
    - saved_by: many-to-many relationship with User through SavedPost
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        related_query_name="post",
    )

    # Organize uploaded files under a dedicated directory
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    title = models.CharField(max_length=255)

    # blank=True allows auto-generation in save()
    # unique=True prevents URL collisions
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name="posts",
    )

    status = models.BooleanField(default=False)

    # Standard timestamp naming
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.TextField(blank=True)

    content = models.TextField()

    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="SavedPost",
        blank=True,
        related_name="saved_posts",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Article"
        ordering = ["-created_at", "pk", "status"]

    def save(self, *args, **kwargs):
        """
        Automatically generate the slug from the title if not provided.
        """
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PostComment(models.Model):
    """
    PostComment model.
    - One post can have multiple comments (one-to-many)
    """
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_comments",
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment({self.pk}) on Post({self.post_id})" # Comment(12) on Post(5)


class SavedPost(models.Model):
    """
    SavedPost join table.
    - Stores when a user saved a post
    - Prevents duplicate (user, post) pairs
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # the database constraint name : ERROR: duplicate key value violates unique_saved_post
            models.UniqueConstraint(fields=["user", "post"], name="unique_saved_post")
        ]

    def __str__(self) -> str:
        return f"SavedPost(user={self.user_id}, post={self.post_id})" # SavedPost(user=3, post=18)

