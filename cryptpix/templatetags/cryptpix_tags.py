from django import template
from django.template.base import TokenType
from django.utils.html import format_html_join
from cryptpix.html import get_css, get_js, render_image_stack
from django.utils.safestring import mark_safe
from django.utils.html import escape
import json

register = template.Library()

@register.simple_tag
def cryptpix_css():
    return mark_safe(get_css())

@register.simple_tag
def cryptpix_js():
    return mark_safe(get_js())

@register.tag
def cryptpix_image(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            f"'{tag_name}' tag requires at least 1 argument: photo instance"
        )

    photo_var = parser.compile_filter(bits[1])
    raw_attrs = bits[2:]

    attrs = {}
    for bit in raw_attrs:
        if "=" not in bit:
            raise template.TemplateSyntaxError(
                f"Malformed attribute assignment: {bit}"
            )
        key, val = bit.split("=", 1)
        attrs[key] = parser.compile_filter(val)

    return CryptPixImageNode(photo_var, attrs)

class CryptPixImageNode(template.Node):
    def __init__(self, photo_var, attrs):
        self.photo_var = photo_var
        self.attrs = attrs

    def render(self, context):
        photo = self.photo_var.resolve(context)
        url1 = getattr(photo, "image_layer_1").url
        url2 = getattr(photo, "image_layer_2").url
        tile_size = getattr(photo, "tile_size")
        width = getattr(photo, "image_width", None)
        height = getattr(photo, "image_height", None)

        # Allow override via tag attributes
        width_attr = self.attrs.get('width')
        height_attr = self.attrs.get('height')
        breakpoints = self.attrs.get('breakpoints')

        if width_attr:
            width_attr = width_attr.resolve(context)
        if height_attr:
            height_attr = height_attr.resolve(context)
        if breakpoints:
            breakpoints = json.loads(breakpoints.resolve(context))

        top_img_attrs = []
        for key, val in self.attrs.items():
            if key not in ['width', 'height', 'breakpoints']:
                resolved_val = val.resolve(context)
                top_img_attrs.append(f'{key}="{escape(resolved_val)}"')

        top_img_attrs_str = " ".join(top_img_attrs)

        return render_image_stack(
            url1, url2, tile_size, width, height,
            top_img_attrs=mark_safe(top_img_attrs_str),
            width_attr=width_attr, height_attr=height_attr, breakpoints=breakpoints
        )