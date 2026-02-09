from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse

from .utils import sign_image_token

import json


def get_css():
    return """
<style>
  /* ============================================================= */
  /* CryptPix image stack (defensive, single paint surface)         */
  /* ============================================================= */
  .image-stack {
    /* Make the element stand on its own in any layout */
    display: block !important;
    position: relative !important;
    overflow: hidden !important;
    isolation: isolate !important;

    /* Neutralize common host CSS footguns */
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    line-height: 0 !important;
    font-size: 0 !important;
    box-sizing: content-box !important;

    /* Background-layer rendering (two layers, one element) */
    background-color: rgba(0, 0, 0, 0) !important;
    background-repeat: no-repeat, no-repeat !important;
    background-position: 0 0, 0 0 !important;
    background-size: 100% 100%, 100% 100% !important;

    /* Let the browser do normal sampling; avoid forced pixelation */
    image-rendering: auto !important;
  }

  /* Keep lazy-fade styles for compatibility (CryptPix JS uses IMG) */
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
    return reverse('secure-image', args=[token])


def add_lazy_class(attrs: str) -> str:
    """Ensure that the 'lazy' class is added to attrs' class attribute."""
    import re

    class_match = re.search(r'class=["\'](.*?)["\']', attrs)
    if class_match:
        classes = class_match.group(1).split()
        if 'lazy' not in classes:
            classes.append('lazy')
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
    """
    Render CryptPix layers as CSS background images on a single element.

    This avoids per-element rasterization drift (stacked <img> elements) and
    gives the resizing script a stable, defensive hook via data attributes.
    """

    breakpoints_json = json.dumps(breakpoints or [])

    # Preserve API: callers have been passing attributes intended for the top <img>.
    # With background rendering, apply those attributes to the container instead.
    container_attrs = (top_img_attrs or "").strip()

    # Construct meta attributes with single quotes
    meta_attrs = [
        f"data-tile-size='{tile_size}'",
        f"data-breakpoints='{breakpoints_json}'",
        f"data-natural-width='{width}'",
        f"data-natural-height='{height}'",
    ]
    if width_attr is not None:
        meta_attrs.append(f"data-width='{width_attr}'")
    if height_attr is not None:
        meta_attrs.append(f"data-height='{height_attr}'")
    if parent_size is not None:
        meta_attrs.append(f"data-parent-size='{parent_size}'")

    image_id_1 = f"{image_id}_1"
    image_id_2 = f"{image_id}_2"
    url1 = escape(get_secure_image_url(image_id_1, request))
    url2 = escape(get_secure_image_url(image_id_2, request))

    # One filter pass on the container, not per-layer.
    filter_style = f"filter: invert(100%) hue-rotate(-{hue_rotation}deg);"

    # Two background layers, pinned to the same box.
    background_style = f"background-image: url('{url1}'), url('{url2}');"

    # Give the element intrinsic sizing so it won't collapse before JS runs.
    # The consuming project can still size it via CSS; our JS will later snap.
    ratio_style = f"aspect-ratio: {width}/{height}; width: 100%;"

    html = f"""
<div class="image-stack" style="{background_style} {filter_style} {ratio_style}" {container_attrs}>
  <div class="tile-meta" {' '.join(meta_attrs)} hidden></div>
</div>
"""
    return mark_safe(html)
