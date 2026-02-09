from django.utils.html import escape
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
    background-color: rgba(0, 0, 0, 0);
    z-index: 10;

    /* Key: render both layers as backgrounds of ONE element */
    background-repeat: no-repeat, no-repeat;
    background-position: center center, center center;
    background-size: contain, contain;

    /* Avoid pixelation hacks */
    image-rendering: auto;
  }

  /* Keep these in case other parts of the site still rely on them.
     (CryptPix rendering below no longer uses <img> tags.) */
  img.lazy {
    opacity: 0;
    transition: opacity 1.2s ease-out;
    transform: translateZ(0);
  }
  img.lazy.loaded {
    opacity: 1;
  }
</style>
"""


def get_secure_image_url(image_id, request):
    # Ensure session key exists
    if not request.session.session_key:
        request.session.create()
    token = sign_image_token(image_id, request.session.session_key)
    url = reverse("secure-image", args=[token])
    return url


def add_lazy_class(attrs: str) -> str:
    """
    Ensure that the 'lazy' class is added to the class attribute in attrs.
    If no class attribute exists, add one.
    """
    import re

    class_match = re.search(r'class=["\'](.*?)["\']', attrs)
    if class_match:
        classes = class_match.group(1).split()
        if "lazy" not in classes:
            classes.append("lazy")
        attrs = re.sub(
            r'class=["\'](.*?)["\']',
            f'class="{" ".join(classes)}"',
            attrs,
        )
    else:
        attrs = f'class="lazy" {attrs}'.strip()

    return attrs


def render_image_stack(
    image_id,
    request,
    tile_size,
    width,
    height,
    hue_rotation,
    top_img_attrs="",
    width_attr=None,
    height_attr=None,
    breakpoints=None,
    parent_size=None,
):
    breakpoints_json = json.dumps(breakpoints or [])

    # Preserve existing behavior: caller may pass attributes intended for the top <img>.
    # We now apply them to the container <div> instead (compatibility, minimal disruption).
    container_attrs = top_img_attrs.strip()

    meta_attrs = [
        f"data-tile-size='{tile_size}'",
        f"data-breakpoints='{breakpoints_json}'",
    ]
    if width_attr is not None:
        meta_attrs.append(f"data-width='{width_attr}'")
    if height_attr is not None:
        meta_attrs.append(f"data-height='{height_attr}'")
    if parent_size is not None:
        meta_attrs.append(f"data-parent-size='{parent_size}'")

    image_id_1 = str(image_id) + "_1"
    image_id_2 = str(image_id) + "_2"

    url1 = escape(get_secure_image_url(image_id_1, request))
    url2 = escape(get_secure_image_url(image_id_2, request))

    # One paint context: both layers as CSS backgrounds on the same element.
    # Filter is applied ONCE to the container, not per-layer.
    html = f"""
<div class="image-stack"
     style="
        background-image: url('{url1}'), url('{url2}');
        filter: invert(100%) hue-rotate(-{hue_rotation}deg);
     "
     {container_attrs}>
  <div class="tile-meta" {" ".join(meta_attrs)} hidden></div>
</div>
"""
    return mark_safe(html)
