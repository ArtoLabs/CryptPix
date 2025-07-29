from django.utils.html import mark_safe

class CryptPixAdminMixin:
    readonly_fields = ('image_layer_1_preview', 'image_layer_2_preview')

    def image_layer_1_preview(self, obj):
        if getattr(obj, 'image_layer_1', None):
            return mark_safe(f'<img src="{obj.image_layer_1.url}" width="200" />')
        return "No Layer 1 Image"
    image_layer_1_preview.short_description = 'Layer 1 Preview'

    def image_layer_2_preview(self, obj):
        if getattr(obj, 'image_layer_2', None):
            return mark_safe(f'<img src="{obj.image_layer_2.url}" width="200" />')
        return "No Layer 2 Image"
    image_layer_2_preview.short_description = 'Layer 2 Preview'
