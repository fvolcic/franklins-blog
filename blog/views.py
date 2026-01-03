from django.shortcuts import render, get_object_or_404, redirect
import markdown

from .models import Post


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
