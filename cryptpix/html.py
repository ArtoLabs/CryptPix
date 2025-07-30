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
  console.log('⚠️ resizeImageStacks called');
  
  const TILE_SIZE = 48;
  const VALID_DIVISORS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 48];

  const monitorWidth = window.screen.width;
  const windowWidth = window.innerWidth;
  const percentOfMonitor = windowWidth / monitorWidth;

  console.log(`- Monitor width: ${monitorWidth}px`);
  console.log(`- Window width: ${windowWidth}px`);
  console.log(`- Window is ${(percentOfMonitor * 100).toFixed(1)}% of monitor width`);
  
  // Choose closest divisor based on current % of monitor
  function getBestDivisor() {
    // Invert logic: closer to 1 means bigger image, closer to 48 means smaller
    const idealScale = percentOfMonitor; // e.g., 0.5 = want half-size
    const idealDivisor = 1 / idealScale;

    // Find closest valid divisor to the ideal one
    let bestDivisor = VALID_DIVISORS[0];
    let smallestDiff = Math.abs(bestDivisor - idealDivisor);

    for (const divisor of VALID_DIVISORS) {
      const diff = Math.abs(divisor - idealDivisor);
      if (diff < smallestDiff) {
        bestDivisor = divisor;
        smallestDiff = diff;
      }
    }

    return bestDivisor;
  }

  const divisor = getBestDivisor();
  console.log(`- Selected divisor: ${divisor}`);

  document.querySelectorAll('.image-stack').forEach(function(stack, index) {
    console.log(`Processing stack #${index}`);
    
    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) {
      console.log(`- Stack #${index} has no image with required attributes`);
      return;
    }
    
    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);
    console.log(`- Natural dimensions: ${naturalWidth}x${naturalHeight}`);
    
    // Calculate new dimensions based on selected divisor
    const newWidth = Math.floor(naturalWidth / divisor);
    const newHeight = Math.floor(naturalHeight / divisor);
    console.log(`- New dimensions: ${newWidth}x${newHeight} (1/${divisor} of original)`);
    
    stack.style.width = newWidth + 'px';
    stack.style.height = newHeight + 'px';

    // Check result
    const computedStyle = window.getComputedStyle(stack);
    console.log(`- Computed style: width=${computedStyle.width}, height=${computedStyle.height}`);
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

