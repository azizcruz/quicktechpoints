import os
import uuid
from django.db import models
from django.utils.text import slugify


def article_image_file_path(instance, filename):
    """Generate file path for article image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('', filename)

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    is_published_to_facebook = models.BooleanField(default=False)
    is_published_to_twitter = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    keywords = models.CharField(max_length=255, blank=True)
    tag = models.ManyToManyField('Tag', related_name='articles')
    image = models.ImageField(upload_to=article_image_file_path)
    likes = models.TextField(blank=True)
    dislikes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        # Replace <p> tags with <br> tags
        no_p = self.body.replace('<p>', '').replace('</p>', '')
        self.body = no_p
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
