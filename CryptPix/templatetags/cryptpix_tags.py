from django import template
from cryptpix.html import get_css, get_js, render_image_stack

register = template.Library()

@register.simple_tag
def cryptpix_css():
    """Injects the required <style> block for image layering."""
    return get_css()

@register.simple_tag
def cryptpix_js():
    """Injects the required <script> block to size image containers."""
    return get_js()

@register.simple_tag
def cryptpix_image(layer1_url, layer2_url):
    """Renders the image stack <div> given two image URLs."""
    return render_image_stack(layer1_url, layer2_url)
