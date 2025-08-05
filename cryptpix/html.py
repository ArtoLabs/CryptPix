from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

from .utils import sign_image_token

import json


def get_css():
    return """
<style>
  .image-stack {
    width: 100%;
    height: 100%;
    position: relative;
    display: inline-block;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
  }
  .image-stack img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    image-rendering: pixelated;
  }
</style>
"""


def get_secure_image_url(image_id, request):
    # Ensure session key exists
    if not request.session.session_key:
        request.session.create()
        # print(f"DEBUG - Created new session key: {request.session.session_key}")
    # Generate token with logging
    token = sign_image_token(image_id, request.session.session_key)
    url = reverse('secure-image', args=[token])
    return url


def render_image_stack(image_id, request, tile_size, width, height, hue_rotation, top_img_attrs="", width_attr=None, height_attr=None, breakpoints=None, parent_size=None):
    breakpoints_json = json.dumps(breakpoints or [])

    # Construct meta attributes with single quotes
    meta_attrs = [
        f"data-tile-size='{tile_size}'",
        f"data-breakpoints='{breakpoints_json}'"
    ]
    if width_attr is not None:
        meta_attrs.append(f"data-width='{width_attr}'")
    if height_attr is not None:
        meta_attrs.append(f"data-height='{height_attr}'")
    if parent_size is not None:
        meta_attrs.append(f"data-parent-size='{parent_size}'")  # Add data-parent-size

    # Build the HTML as a plain string
    image_id_1 = str(image_id) + '_1'
    image_id_2 = str(image_id) + '_2'
    html = f"""
<div class="image-stack">
  <img src="{escape(get_secure_image_url(image_id_1, request))}" style="filter: invert(100%) hue-rotate(-{hue_rotation}deg);">
  <img src="{escape(get_secure_image_url(image_id_2, request))}" style="filter: invert(100%) hue-rotate(-{hue_rotation}deg);" {top_img_attrs} data-natural-width={width} data-natural-height={height}>
  <div class="tile-meta" {" ".join(meta_attrs)} hidden></div>
</div>
"""
    return mark_safe(html)