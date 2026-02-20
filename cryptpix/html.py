from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse

from .utils import sign_image_token

import json


def get_css():
    return """
<style>
  /* Canonical wrapper/surface */
  .cryptpix-media {
    width: 100%;
    height: 100%;
    position: relative;
    display: inline-block;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
    background-color: rgba(0, 0, 0, 0);
    z-index: 10;
  }

  .cryptpix-surface {
    width: 100%;
    height: 100%;
    position: relative;
    display: block;
  }

  /* Stack mode: two imgs positioned and aligned */
  .cryptpix-media[data-cp-mode="stack"] .cryptpix-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    image-rendering: pixelated;
  }

  /* Single mode: normal flow */
  .cryptpix-media[data-cp-mode="single"] .cryptpix-img {
    display: block;
    width: 100%;
    height: auto;
    object-fit: contain;
  }

  /* Lazy fade-in */
  img.cryptpix-img.lazy {
    opacity: 0;
    transition: opacity 1.2s ease-out;
    transform: translateZ(0);
  }

  img.cryptpix-img.lazy.loaded {
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


def add_img_classes(attrs: str) -> str:
    """Ensure canonical classes are present on all emitted <img> tags."""
    import re

    required = {"cryptpix-img", "lazy"}
    class_match = re.search(r'class=["\'](.*?)["\']', attrs)
    if class_match:
        classes = set(class_match.group(1).split())
        classes |= required
        # Preserve stable ordering
        ordered = []
        for c in ["cryptpix-img", "lazy"]:
            if c in classes:
                ordered.append(c)
                classes.remove(c)
        ordered.extend(sorted(classes))
        attrs = re.sub(r'class=["\'](.*?)["\']', f'class="{" ".join(ordered)}"', attrs)
    else:
        attrs = f'class="cryptpix-img lazy" {attrs}'.strip()

    return attrs


def _distortion_filter_style(use_distortion: bool, hue_rotation) -> str:
    """Returns the inline CSS filter that reverses the stored distortion."""
    if not use_distortion:
        return ""
    if hue_rotation in (None, "", 0, "0"):
        return "filter: invert(100%);"
    return f"filter: invert(100%) hue-rotate(-{hue_rotation}deg);"


def _security_level(*, use_split: bool, use_distortion: bool) -> str:
    if use_split:
        return "high"
    if use_distortion:
        return "medium"
    return "low"


def _render_wrapper_open(
    *,
    image_id,
    mode: str,
    security: str,
    natural_width=None,
    natural_height=None,
    wrapper_attrs: str = "",
) -> str:
    natural_attrs = ""
    if natural_width is not None:
        natural_attrs += f' data-natural-width="{natural_width}"'
    if natural_height is not None:
        natural_attrs += f' data-natural-height="{natural_height}"'

    # wrapper_attrs is expected to already be a string of attributes, e.g. 'id="..." data-x="..."'
    wrapper_attrs = (wrapper_attrs or "").strip()
    wrapper_attrs = f" {wrapper_attrs}" if wrapper_attrs else ""

    return (
        f'<div class="cryptpix-media" data-cp-mode="{mode}" data-cp-security="{security}" '
        f'data-cp-image-id="{image_id}"{natural_attrs}{wrapper_attrs}>'
        f'<div class="cryptpix-surface">'
    )


def render_single_image(
    image_id,
    request,
    *,
    layer=1,
    use_distortion=False,
    hue_rotation=None,
    img_attrs="",
    wrapper_attrs="",
    natural_width=None,
    natural_height=None,
):
    """Render a single secure image."""
    img_attrs = add_img_classes(img_attrs)

    secure_id = f"{image_id}_{layer}"
    style = _distortion_filter_style(use_distortion, hue_rotation)
    style_attr = f' style="{style}"' if style else ""

    security = _security_level(use_split=False, use_distortion=bool(use_distortion))
    wrapper_open = _render_wrapper_open(
        image_id=image_id,
        mode="single",
        security=security,
        natural_width=natural_width,
        natural_height=natural_height,
        wrapper_attrs=wrapper_attrs,
    )

    html = f"""
{wrapper_open}
  <img
    src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
    data-src="{escape(get_secure_image_url(secure_id, request))}"
    data-cp-layer="{layer}"
    loading="lazy"{style_attr} {img_attrs}>
</div></div>
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
    wrapper_attrs="",
    width_attr=None,
    height_attr=None,
    breakpoints=None,
    parent_size=None,
):
    """Render the two-layer split stack."""
    breakpoints_json = json.dumps(breakpoints or [])

    # Both images must share the same canonical class contract.
    top_img_attrs = add_img_classes(top_img_attrs)

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
    style_attr = f' style="{style}"' if style else ""

    security = _security_level(use_split=True, use_distortion=bool(use_distortion))
    wrapper_open = _render_wrapper_open(
        image_id=image_id,
        mode="stack",
        security=security,
        natural_width=width,
        natural_height=height,
        wrapper_attrs=wrapper_attrs,
    )

    html = f"""
{wrapper_open}
  <img
    src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
    data-src="{escape(get_secure_image_url(image_id_1, request))}"
    data-cp-layer="1"
    loading="lazy"{style_attr} class="cryptpix-img lazy">
  <img
    src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
    data-src="{escape(get_secure_image_url(image_id_2, request))}"
    data-cp-layer="2"
    loading="lazy"{style_attr} {top_img_attrs}>
  <div class="cryptpix-meta" {" ".join(meta_attrs)} hidden></div>
</div></div>
"""
    return mark_safe(html)