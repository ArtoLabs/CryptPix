from django.utils.html import mark_safe


class CryptPixAdminMixin:
    """
    Drop-in mixin for ModelAdmin classes.

    Shows:
      - the two save-time toggles (editable in admin)
      - read-only metadata and previews
    """

    readonly_fields = (
        "tile_size",
        "image_width",
        "image_height",
        "hue_rotation",
        "image_layer_1_preview",
        "image_layer_2_preview",
    )

    def display_thumbnail(self, obj):
        # Kept for backward compatibility with existing admins that reference it.
        if getattr(obj, "image", None):
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No Image"

    display_thumbnail.short_description = "Thumbnail"

    def image_layer_1_preview(self, obj):
        if getattr(obj, "image_layer_1", None):
            try:
                url = obj.image_layer_1.url
            except Exception:
                return "Layer 1 not available"
            return mark_safe(f'<img src="{url}" width="200" />')
        return "No Layer 1 Image"

    image_layer_1_preview.short_description = "Layer 1 Preview"

    def image_layer_2_preview(self, obj):
        if getattr(obj, "image_layer_2", None):
            try:
                url = obj.image_layer_2.url
            except Exception:
                return "Layer 2 not available"
            return mark_safe(f'<img src="{url}" width="200" />')
        return "No Layer 2 Image"

    image_layer_2_preview.short_description = "Layer 2 Preview"
