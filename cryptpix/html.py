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
  const allowedDivisors = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16];

  const monitorWidth = screen.width;
  const monitorHeight = screen.height;

  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;

  const percentOfMonitorWidth = windowWidth / monitorWidth;
  const percentOfMonitorHeight = windowHeight / monitorHeight;

  document.querySelectorAll('.image-stack').forEach(function(stack) {
    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) return;

    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);

    let chosenDivisor = 1;

    for (const divisor of allowedDivisors) {
      const scaledWidth = naturalWidth / divisor;
      const scaledHeight = naturalHeight / divisor;

      if (
        scaledWidth <= windowWidth &&
        scaledHeight <= windowHeight
      ) {
        chosenDivisor = divisor;
      } else {
        break;
      }
    }

    const newWidth = Math.floor(naturalWidth / chosenDivisor);
    const newHeight = Math.floor(naturalHeight / chosenDivisor);

    stack.style.width = newWidth + 'px';
    stack.style.height = newHeight + 'px';
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

