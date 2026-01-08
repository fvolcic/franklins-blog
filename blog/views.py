from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import F
import markdown
import hashlib
import urllib.request
import json

from .models import Post, PageView


def home(request):
    """Redirect to the About Me page."""
    try:
        about_post = Post.objects.get(is_about_page=True, published=True)
        return redirect('post_detail', slug=about_post.slug)
    except Post.DoesNotExist:
        return redirect('blog_list')


def blog_list(request):
    """Show all published blog posts (excluding the about page)."""
    posts = Post.objects.filter(published=True, is_about_page=False)
    return render(request, 'blog/blog_list.html', {'posts': posts})


def post_detail(request, slug):
    """Show a single blog post rendered from Markdown."""
    post = get_object_or_404(Post, slug=slug, published=True)

    md = markdown.Markdown(extensions=['fenced_code', 'codehilite', 'tables', 'toc'])
    content_html = md.convert(post.content)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'content_html': content_html,
    })


def get_client_ip(request):
    """Get client IP from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_country_from_ip(ip):
    """Get country from IP using ip-api.com (free, no signup)."""
    try:
        url = f"http://ip-api.com/json/{ip}?fields=country"
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            return data.get('country')
    except Exception:
        return None


def hash_ip(ip):
    """Hash IP for privacy-preserving deduplication."""
    return hashlib.sha256(ip.encode()).hexdigest()[:32]


@require_POST
def track_view(request, slug):
    """Track a page view with referrer and country."""
    try:
        post = Post.objects.get(slug=slug, published=True)

        # Get client info
        ip = get_client_ip(request)
        ip_hashed = hash_ip(ip) if ip else None
        referrer = request.META.get('HTTP_REFERER', '')[:500] or None
        country = get_country_from_ip(ip) if ip else None

        # Create PageView record
        PageView.objects.create(
            post=post,
            referrer=referrer,
            country=country,
            ip_hash=ip_hashed
        )

        # Update cached view count
        Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        post.refresh_from_db()

        return JsonResponse({'success': True, 'view_count': post.view_count})
    except Post.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
