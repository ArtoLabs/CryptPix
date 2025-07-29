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
    print(token)
    
    """
    Usage:
    {% cryptpix_image layer1_url layer2_url id="photo" class="img-fluid" alt="Photo" %}
    Only the second image (top layer) gets these attributes.
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 3:
        raise template.TemplateSyntaxError(
            f"'{tag_name}' tag requires at least 2 arguments: layer1_url and layer2_url"
        )

    layer1_var = parser.compile_filter(bits[1])
    layer2_var = parser.compile_filter(bits[2])
    remaining_bits = bits[3:]
    attrs = token_kwargs(remaining_bits, parser, support_legacy=False)

    return CryptPixImageNode(layer1_var, layer2_var, attrs)


class CryptPixImageNode(template.Node):
    def __init__(self, layer1_var, layer2_var, attrs):
        self.layer1_var = layer1_var
        self.layer2_var = layer2_var
        self.attrs = attrs

    def render(self, context):
        url1 = self.layer1_var.resolve(context)
        url2 = self.layer2_var.resolve(context)

        # Render attributes as HTML
        attr_pairs = []
        for key, val in self.attrs.items():
            resolved_val = val.resolve(context)
            attr_pairs.append(f'{key}="{resolved_val}"')

        return render_image_stack(url1, url2, top_img_attrs=attrs_str)
