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
  // Helper function to parse dimension (pixels or percentage)
  function parseDimension(value, baseDimension, isParentSize, parentDimension) {
    if (!value) return baseDimension;
    if (value.endsWith('%') && isParentSize) {
      if (parentDimension === 0) {
        console.warn('Parent dimension is 0; falling back to base dimension:', baseDimension);
        return baseDimension;
      }
      const percentage = parseFloat(value) / 100;
      return Math.round(parentDimension * percentage);
    }
    if (value.endsWith('%')) {
      const percentage = parseFloat(value) / 100;
      return Math.round(baseDimension * percentage);
    }
    return parseInt(value, 10);
  }

  // Helper function to find a parent with non-zero dimensions
  function findSizedParent(element) {
    let parent = element.parentElement;
    while (parent) {
      if (parent.clientWidth > 0 && parent.clientHeight > 0) {
        console.log('Found sized parent:', parent, 'width:', parent.clientWidth, 'height:', parent.clientHeight);
        return parent;
      }
      parent = parent.parentElement;
    }
    console.warn('No parent with non-zero dimensions found; falling back to document body');
    return document.body; // Fallback to document body
  }

  document.querySelectorAll('.image-stack').forEach(function(stack) {
    const tileMeta = stack.querySelector('.tile-meta');
    if (!tileMeta) {
      console.warn('No tile-meta found in image-stack:', stack);
      return;
    }

    const tileSize = parseInt(tileMeta.dataset.tileSize, 10);
    if (isNaN(tileSize)) {
      console.warn('Invalid tileSize in tile-meta:', tileMeta.dataset.tileSize);
      return;
    }

    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) {
      console.warn('No image with data-natural-width/height found in image-stack:', stack);
      return;
    }

    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);
    if (isNaN(naturalWidth) || isNaN(naturalHeight)) {
      console.warn('Invalid natural width/height in image:', topImg);
      return;
    }

    const isParentSize = tileMeta.dataset.parentSize === 'true';
    // Find parent with non-zero dimensions
    const parentContainer = isParentSize ? findSizedParent(stack) : null;
    const parentWidth = isParentSize ? parentContainer.clientWidth : naturalWidth;
    const parentHeight = isParentSize ? parentContainer.clientHeight : naturalHeight;

    if (isParentSize && (parentWidth === 0 || parentHeight === 0)) {
      console.warn('Selected parent container has zero width or height:', parentContainer);
    }

    const breakpoints = JSON.parse(tileMeta.dataset.breakpoints || '[]');
    const currentWidth = window.innerWidth;

    let targetWidth = naturalWidth;
    let targetHeight = naturalHeight;

    // Check for user-defined width and height
    if (tileMeta.dataset.width) {
      targetWidth = parseDimension(tileMeta.dataset.width, naturalWidth, isParentSize, parentWidth);
      // If height is missing or blank, use width value
      targetHeight = parseDimension(
        tileMeta.dataset.height || tileMeta.dataset.width,
        naturalHeight,
        isParentSize,
        parentHeight
      );
    } else {
      // Apply breakpoints if defined
      for (const bp of breakpoints) {
        if (currentWidth <= bp.maxWidth && bp.width) {
          targetWidth = parseDimension(bp.width, naturalWidth, isParentSize, parentWidth);
          // If breakpoint height is missing or blank, use breakpoint width
          targetHeight = parseDimension(
            bp.height || bp.width,
            naturalHeight,
            isParentSize,
            parentHeight
          );
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


def render_image_stack(url1, url2, tile_size, width, height, hue_rotation, top_img_attrs="", width_attr=None, height_attr=None, breakpoints=None, parent_size=None):
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
    html = f"""
<div class="image-stack">
  <img src="{escape(url1)}" style="filter: invert(100%) hue-rotate(-{escape(hue_rotation)}deg);">
  <img src="{escape(url2)}" style="filter: invert(100%) hue-rotate(-{escape(hue_rotation)}deg);" {top_img_attrs} data-natural-width={escape(width)} data-natural-height={escape(height)}>
  <div class="tile-meta" {" ".join(meta_attrs)} hidden></div>
</div>
"""
    return mark_safe(html)