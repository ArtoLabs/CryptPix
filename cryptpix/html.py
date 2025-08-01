from django.utils.html import escape, format_html
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

def render_image_stack(url1, url2, tile_size, top_img_attrs="", width=None, height=None, breakpoints=None):
    breakpoints_json = json.dumps(breakpoints or [])
    width_attr = f'data-width="{width}"' if width is not None else ''
    height_attr = f'data-height="{height}"' if height is not None else ''
    return format_html("""
<div class="image-stack">
  <img src="{}" alt="Layer 1">
  <img src="{}" {} >
  <div class="tile-meta" data-tile-size="{}" data-breakpoints='{}' {} {} hidden></div>
</div>
""", url1, url2, top_img_attrs, tile_size, breakpoints_json, width_attr, height_attr)