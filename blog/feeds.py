from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Franklin Volcic's Blog"
    link = "/blog/"
    description = "Latest blog posts from Franklin Volcic"

    def items(self):
        return Post.objects.filter(published=True, is_about_page=False)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # Return first 300 chars of content as description
        if len(item.content) > 300:
            return item.content[:300] + "..."
        return item.content

    def item_link(self, item):
        return reverse('post_detail', args=[item.slug])

    def item_pubdate(self, item):
        return item.created_at
