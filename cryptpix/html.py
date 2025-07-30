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
  console.warn('Starting resizeImageStacks with gridStep:', gridStep);
  document.querySelectorAll('.image-stack').forEach(stack => {
    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) {
      console.warn('No top image with natural size found in stack:', stack);
      return;
    }
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

    console.debug('Resizing image stack:', {
      stack,
      naturalWidth: W,
      naturalHeight: H,
      percent,
      computedWidth: w,
      computedHeight: h
    });

    stack.style.width = w + 'px';
    stack.style.height = h + 'px';
    console.debug('Updated stack style:', stack.style.cssText);
  });
}

console.log('Setting up event listeners');
window.addEventListener('DOMContentLoaded', function() {
  console.log('DOMContentLoaded fired');
  
  // Debug DOM elements before calling function
  const stacks = document.querySelectorAll('.image-stack');
  console.log('Found image stacks:', stacks.length);
  
  stacks.forEach((stack, i) => {
    console.log(`Stack ${i}:`, stack);
    const imgs = stack.querySelectorAll('img');
    console.log(`  Images in stack ${i}:`, imgs.length);
    imgs.forEach((img, j) => {
      console.log(`  Image ${j} has data-natural-width:`, img.hasAttribute('data-natural-width'));
      console.log(`  Image ${j} has data-natural-height:`, img.hasAttribute('data-natural-height'));
    });
  });
  
  resizeImageStacks();
});
window.addEventListener('resize', function() {
  console.log('Resize event fired');
  resizeImageStacks();
});
console.log('Event listeners registered');
</script>
"""

def render_image_stack(url1, url2, top_img_attrs=""):
    return format_html("""
<div class="image-stack">
  <img src="{}" alt="Layer 1">
  <img src="{}" {} >
</div>
""", url1, url2, top_img_attrs)

