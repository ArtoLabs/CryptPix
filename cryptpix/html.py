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
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
    background-color: rgba(0, 0, 0, 0);
    z-index: 10;
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

  /* Lazy fade-in */
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
        attrs = re.sub(r'class=["\'](.*?)["\']', f'class="{" ".join(classes)}"', attrs)
    else:
        attrs = f'class="lazy" {attrs}'.strip()

    return attrs


def _distortion_filter_style(use_distortion: bool, hue_rotation) -> str:
    """
    Returns the inline CSS filter that reverses the stored distortion.
    If distortion is not used, returns empty string.
    """
    if not use_distortion:
        return ""
    if hue_rotation in (None, "", 0, "0"):
        # If distortion is "enabled" but hue_rotation isn't present, still invert to be consistent.
        # Realistically hue_rotation should be set whenever use_distortion=True at save-time.
        return "filter: invert(100%);"
    return f"filter: invert(100%) hue-rotate(-{hue_rotation}deg);"


def render_single_image(
    image_id,
    request,
    *,
    layer=1,
    use_distortion=False,
    hue_rotation=None,
    img_attrs="",
    natural_width=None,
    natural_height=None,
):
    """
    Render a single secure image.

    layer:
      - 0 for original (rarely used in public rendering)
      - 1 for processed derivative (always exists per our contract)
    """
    img_attrs = add_lazy_class(img_attrs)

    secure_id = f"{image_id}_{layer}"
    style = _distortion_filter_style(use_distortion, hue_rotation)
    style_attr = f' style="{style}"' if style else ""

    natural_attrs = ""
    if natural_width is not None:
        natural_attrs += f' data-natural-width="{natural_width}"'
    if natural_height is not None:
        natural_attrs += f' data-natural-height="{natural_height}"'

    html = f"""
<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
     data-src="{escape(get_secure_image_url(secure_id, request))}"
     loading="lazy"{style_attr} {img_attrs}{natural_attrs}>
"""
    return mark_safe(html)


def render_image_stack(
    image_id,
    request,
    tile_size,
    width,
    height,
    hue_rotation,
    *,
    use_distortion=False,
    top_img_attrs="",
    width_attr=None,
    height_attr=None,
    breakpoints=None,
    parent_size=None,
):
    """
    Render the two-layer split stack.

    If use_distortion=True, applies the reversal filter.
    If use_distortion=False, no filter is applied.
    """
    breakpoints_json = json.dumps(breakpoints or [])
    top_img_attrs = add_lazy_class(top_img_attrs)

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

    style = _distortion_filter_style(use_distortion, hue_rotation)
    style_attr = f'style="{style}"' if style else ""

    html = f"""
<div class="image-stack">
  <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
       data-src="{escape(get_secure_image_url(image_id_1, request))}"
       loading="lazy" {style_attr} class="lazy">
  <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
       data-src="{escape(get_secure_image_url(image_id_2, request))}"
       loading="lazy" {style_attr} {top_img_attrs} data-natural-width="{width}" data-natural-height="{height}">
  <div class="tile-meta" {" ".join(meta_attrs)} hidden></div>
</div>
"""
    return mark_safe(html)
