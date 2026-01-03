from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Image


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
    list_display = ('title', 'slug', 'published', 'is_about_page', 'created_at')
    list_filter = ('published', 'is_about_page', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
