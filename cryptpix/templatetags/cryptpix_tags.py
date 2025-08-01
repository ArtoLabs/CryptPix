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

        width = self.attrs.get('width')
        height = self.attrs.get('height')
        breakpoints = self.attrs.get('breakpoints')

        if width:
            width = width.resolve(context)
        if height:
            height = height.resolve(context)
        if breakpoints:
            breakpoints = json.loads(breakpoints.resolve(context))

        top_img_attrs = []
        for key, val in self.attrs.items():
            if key not in ['width', 'height', 'breakpoints']:
                resolved_val = val.resolve(context)
                top_img_attrs.append(f'{key}="{escape(resolved_val)}"')

        top_img_attrs_str = " ".join(top_img_attrs)

        return render_image_stack(url1, url2, tile_size, top_img_attrs=mark_safe(top_img_attrs_str),
                                width=width, height=height, breakpoints=breakpoints)