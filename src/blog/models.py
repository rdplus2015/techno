from django.conf import settings
from django.db import models
from django.db.models import ManyToManyField


# Create your models here.

class Category(models.model):
        name = models.CharField(max_length=50)
        slug = models.SlugField()


class Posts(models.Model):
        author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                   on_delete=models.SET_NULL,
                                   null=True
                                   related_name="Posts", 
                                   related_query_name="post")
        
        title = models.CharField(max_length=255)
        slug = models.SlugField()
        category = models.ForeignKey(ManyToManyField(Category), 
                                     on_delete=models.SET_NULL,
                                     null = True)
        
        create_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
                return self.title
