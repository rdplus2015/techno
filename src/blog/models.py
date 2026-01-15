from django.conf import settings
from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
        name = models.CharField(max_length=50)
        slug = models.SlugField()


class PostComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

class Posts(models.Model):
        author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name="Posts", 
                                   related_query_name="post")

        image = models.ImageField()
        title = models.CharField(max_length=255)
        slug = models.SlugField()
        category = models.ManyToManyField(
            Category,
            null=True,
            blank=True
        )
        comments = models.ForeignKey(
            PostComment,on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="comments", )

        status = models.BooleanField(default=False)
        create_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        description = models.TextField()
        content = models.TextField

        def __str__(self):
                return self.title

        class Meta:
            verbose_name = 'Article'
            ordering = ['pk', 'date', 'status']


        def save(self, *args, **margs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **margs)