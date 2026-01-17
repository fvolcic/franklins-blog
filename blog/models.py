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
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/', blank=True, null=True, help_text="Optional thumbnail for blog list")
    content = models.TextField(help_text="Write your post in Markdown format")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    is_about_page = models.BooleanField(
        default=False,
        help_text="Check this to make this post the About Me page (only one should be checked)"
    )
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes


class PageView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='page_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    referrer = models.URLField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    ip_hash = models.CharField(max_length=64, blank=True, null=True, help_text="Hashed IP for deduplication")

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.post.title} - {self.viewed_at}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
