from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.urls import path
from django.template.response import TemplateResponse
import json
from datetime import timedelta
from django.utils import timezone

from .models import Post, Image, PageView


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'markdown_code', 'uploaded_at')
    readonly_fields = ('image_preview_large', 'markdown_code_field')
    ordering = ('-uploaded_at',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 400px; max-height: 300px;" />', obj.image.url)
        return "-"
    image_preview_large.short_description = "Preview"

    def markdown_code(self, obj):
        if obj.image:
            return f"![{obj.title}]({obj.image.url})"
        return "-"
    markdown_code.short_description = "Markdown"

    def markdown_code_field(self, obj):
        if obj.image:
            code = f"![{obj.title}]({obj.image.url})"
            return format_html(
                '<input type="text" value="{}" readonly style="width: 100%; padding: 8px; font-family: monospace;" onclick="this.select();" />',
                code
            )
        return "-"
    markdown_code_field.short_description = "Copy this Markdown"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'is_about_page', 'view_count', 'created_at')
    list_filter = ('published', 'is_about_page', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('view_count',)
    ordering = ('-created_at',)


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'viewed_at', 'country', 'referrer_short')
    list_filter = ('post', 'country', 'viewed_at')
    readonly_fields = ('post', 'viewed_at', 'referrer', 'country', 'ip_hash')
    ordering = ('-viewed_at',)
    date_hierarchy = 'viewed_at'

    def referrer_short(self, obj):
        if obj.referrer:
            return obj.referrer[:50] + '...' if len(obj.referrer) > 50 else obj.referrer
        return "-"
    referrer_short.short_description = "Referrer"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_site.admin_view(self.analytics_view), name='pageview_analytics'),
        ]
        return custom_urls + urls

    def analytics_view(self, request):
        # Get data for last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Views per day
        daily_views = (
            PageView.objects
            .filter(viewed_at__gte=thirty_days_ago)
            .annotate(date=TruncDate('viewed_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        # Views by country
        country_views = (
            PageView.objects
            .filter(viewed_at__gte=thirty_days_ago)
            .exclude(country__isnull=True)
            .values('country')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Views by post
        post_views = (
            PageView.objects
            .filter(viewed_at__gte=thirty_days_ago)
            .values('post__title')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Top referrers
        referrer_views = (
            PageView.objects
            .filter(viewed_at__gte=thirty_days_ago)
            .exclude(referrer__isnull=True)
            .values('referrer')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        context = {
            **self.admin_site.each_context(request),
            'title': 'Analytics Dashboard',
            'daily_labels': json.dumps([v['date'].strftime('%b %d') for v in daily_views]),
            'daily_data': json.dumps([v['count'] for v in daily_views]),
            'country_labels': json.dumps([v['country'] for v in country_views]),
            'country_data': json.dumps([v['count'] for v in country_views]),
            'post_labels': json.dumps([v['post__title'][:30] for v in post_views]),
            'post_data': json.dumps([v['count'] for v in post_views]),
            'referrer_data': list(referrer_views),
            'total_views': PageView.objects.filter(viewed_at__gte=thirty_days_ago).count(),
            'unique_countries': PageView.objects.filter(viewed_at__gte=thirty_days_ago).exclude(country__isnull=True).values('country').distinct().count(),
        }

        return TemplateResponse(request, 'admin/blog/pageview/analytics.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_analytics_link'] = True
        return super().changelist_view(request, extra_context=extra_context)
