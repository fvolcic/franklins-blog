from django.db import models
from django.utils import timezone


class Image(models.Model):
    title = models.CharField(max_length=200, help_text="Descriptive name for the image")
    image = models.ImageField(upload_to='images/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(help_text="Write your post in Markdown format")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    is_about_page = models.BooleanField(
        default=False,
        help_text="Check this to make this post the About Me page (only one should be checked)"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
