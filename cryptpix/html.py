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
  
  // Get screen width and window width
  const monitorWidth = window.screen.width;
  const windowWidth = window.innerWidth;
  const percentOfMonitor = windowWidth / monitorWidth;
  
  console.log(`- Monitor width: ${monitorWidth}px`);
  console.log(`- Window width: ${windowWidth}px`);
  console.log(`- Window is ${(percentOfMonitor * 100).toFixed(1)}% of monitor width`);
  
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
    
    // Find the best integer divisor based on monitor percentage
    let divisor;
    if (percentOfMonitor > 0.75) {
      divisor = 1;      // 100% size
    } else if (percentOfMonitor > 0.4) {
      divisor = 2;      // 50% size
    } else if (percentOfMonitor > 0.25) {
      divisor = 4;      // 33% size
    } else {
      divisor = 6;      // 25% size or smaller
    }
    
    console.log(`- Window percentage (${(percentOfMonitor * 100).toFixed(1)}%) leads to divisor of: ${divisor}`);
    
    // Calculate new dimensions
    const newWidth = Math.floor(naturalWidth / divisor);
    const newHeight = Math.floor(naturalHeight / divisor);
    console.log(`- New dimensions: ${newWidth}x${newHeight} (1/${divisor} of original)`);
    
    stack.style.width = newWidth + 'px';
    stack.style.height = newHeight + 'px';
    
    // Verify the style was actually applied
    console.log(`- Applied style: width=${stack.style.width}, height=${stack.style.height}`);
    
    // Check if any computed styles are overriding our changes
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

