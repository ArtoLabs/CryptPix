from django import template
from django.template.base import TokenType
from django.template.defaulttags import token_kwargs
from django.utils.html import format_html_join
from cryptpix.html import get_css, get_js, render_image_stack
from django.utils.safestring import mark_safe
from django.utils.html import escape


register = template.Library()

@register.simple_tag
def cryptpix_css():
    """Injects the required <style> block for image layering."""
    return mark_safe(get_css())

@register.simple_tag
def cryptpix_js():
    """Injects the required <script> block to size image containers."""
    return mark_safe(get_js())

@register.tag
def cryptpix_image(parser, token):
    """
    Usage:
    {% cryptpix_image layer1_url layer2_url tile_size id="photo" class="img-fluid" alt="Photo" data-natural-width=photo.image.width %}
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            f"'{tag_name}' tag requires at least 3 arguments: layer1_url, layer2_url, tile_size"
        )

    layer1_var = parser.compile_filter(bits[1])
    layer2_var = parser.compile_filter(bits[2])
    tile_size_var = parser.compile_filter(bits[3])
    raw_attrs = bits[4:]

    attrs = {}
    for bit in raw_attrs:
        if "=" not in bit:
            raise template.TemplateSyntaxError(
                f"Malformed attribute assignment: {bit}"
            )
        key, val = bit.split("=", 1)
        attrs[key] = parser.compile_filter(val)

    return CryptPixImageNode(layer1_var, layer2_var, tile_size_var, attrs)


class CryptPixImageNode(template.Node):
    def __init__(self, layer1_var, layer2_var, tile_size_var, attrs):
        self.layer1_var = layer1_var
        self.layer2_var = layer2_var
        self.tile_size_var = tile_size_var
        self.attrs = attrs

    def render(self, context):
        url1 = self.layer1_var.resolve(context)
        url2 = self.layer2_var.resolve(context)
        tile_size = self.tile_size_var.resolve(context)

        attr_pairs = []
        for key, val in self.attrs.items():
            resolved_val = val.resolve(context)
            attr_pairs.append(f'{key}="{escape(resolved_val)}"')

        attrs_str = " ".join(attr_pairs)

        return render_image_stack(url1, url2, tile_size, top_img_attrs=mark_safe(attrs_str))
