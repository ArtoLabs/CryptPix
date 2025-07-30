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
function resizeImageStacks(gridStep = 4) {
  document.querySelectorAll('.image-stack').forEach(stack => {
    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) return;
    const W = parseInt(topImg.dataset.naturalWidth);
    const H = parseInt(topImg.dataset.naturalHeight);
    const percent = window.innerWidth / screen.width;
    let w = Math.min(W, W * percent);
    let h = Math.min(H, H * percent);

    // Round to integer
    w = Math.round(w);
    h = Math.round(h);

    // Snap to shared gridStep multiple
    w = w - (w % gridStep);
    h = h - (h % gridStep);

    // Enforce minimum 1 × gridStep
    w = Math.max(w, gridStep);
    h = Math.max(h, gridStep);

    stack.style.width = w + 'px';
    stack.style.height = h + 'px';
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

