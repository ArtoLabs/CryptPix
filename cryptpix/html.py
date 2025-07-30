from django.utils.html import escape, format_html


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
  }
</style>
"""

def get_js():
    return """
<script>
function resizeImageStacks() {
  document.querySelectorAll('.image-stack').forEach(function(stack) {
    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) return;

    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);

    const windowWidth = window.innerWidth;
    const scalePercent = windowWidth / naturalWidth;
    const newWidth = windowWidth;
    const newHeight = naturalHeight * scalePercent;

    stack.style.width = newWidth + 'px';
    stack.style.height = newHeight + 'px';
  });
}

window.addEventListener('DOMContentLoaded', resizeImageStacks);
window.addEventListener('resize', resizeImageStacks);
</script>
"""

def render_image_stack(url1, url2, top_img_attrs=""):
    return format_html("""
<div class="image-stack">
  <img src="{}" alt="Layer 1">
  <img src="{}" {} >
</div>
""", url1, url2, top_img_attrs)

