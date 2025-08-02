from django.utils.html import escape, format_html
import json
from django.utils.safestring import mark_safe

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

def get_js():
    return """
<script>
function resizeImageStacks() {
  document.querySelectorAll('.image-stack').forEach(function(stack) {
    const tileMeta = stack.querySelector('.tile-meta');
    if (!tileMeta) return;

    const tileSize = parseInt(tileMeta.dataset.tileSize, 10);
    if (isNaN(tileSize)) return;

    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) return;

    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);
    if (isNaN(naturalWidth) || isNaN(naturalHeight)) return;

    const breakpoints = JSON.parse(tileMeta.dataset.breakpoints || '[]');
    const currentWidth = window.innerWidth;

    let targetWidth = naturalWidth;
    let targetHeight = naturalHeight;

    // Check for user-defined width and height
    if (tileMeta.dataset.width && tileMeta.dataset.height) {
      targetWidth = parseInt(tileMeta.dataset.width, 10);
      targetHeight = parseInt(tileMeta.dataset.height, 10);
    } else {
      // Apply breakpoints if defined
      for (const bp of breakpoints) {
        if (currentWidth <= bp.maxWidth) {
          targetWidth = bp.width;
          targetHeight = bp.height;
          break;
        }
      }
    }

    // Quantize dimensions to the nearest tile size multiple
    const scaledWidth = Math.round(targetWidth / tileSize) * tileSize;
    const scaledHeight = Math.round(targetHeight / tileSize) * tileSize;

    stack.style.width = `${scaledWidth}px`;
    stack.style.height = `${scaledHeight}px`;
  });
}

window.addEventListener('DOMContentLoaded', resizeImageStacks);
window.addEventListener('resize', resizeImageStacks);
</script>
"""


def render_image_stack(url1, url2, tile_size, width, height, hue_rotation, top_img_attrs="", width_attr=None, height_attr=None, breakpoints=None):
    breakpoints_json = json.dumps(breakpoints or [])

    # Construct meta attributes with single quotes
    meta_attrs = [
        f"data-tile-size='{tile_size}'",  # Changed to single quotes
        f"data-breakpoints='{breakpoints_json}'"  # Already uses single quotes
    ]
    if width_attr is not None:
        meta_attrs.append(f"data-width='{width_attr}'")  # Changed to single quotes
    if height_attr is not None:
        meta_attrs.append(f"data-height='{height_attr}'")  # Changed to single quotes

    # Build the HTML as a plain string
    html = f"""
<div class="image-stack">
  <img src="{escape(url1)}" style="filter: invert(100%) hue-rotate(-{escape(hue_rotation)}deg);">
  <img src="{escape(url2)}" style="filter: invert(100%) hue-rotate(-{escape(hue_rotation)}deg);" {top_img_attrs} data-natural-width={escape(width)} data-natural-height={escape(height)}>
  <div class="tile-meta" {" ".join(meta_attrs)} hidden></div>
</div>
"""
    return mark_safe(html)