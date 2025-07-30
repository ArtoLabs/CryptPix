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
  // Get screen width and window width
  const monitorWidth = window.screen.width;
  const windowWidth = window.innerWidth;
  const percentOfMonitor = windowWidth / monitorWidth;
  
  console.log(`- Window is ${(percentOfMonitor * 100).toFixed(1)}% of monitor width`);
  
  document.querySelectorAll('.image-stack').forEach(function(stack, index) {
    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) return;
    
    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);
    
    // Calculate the scale factor based on percentage, but maintain integer scaling
    // This finds the largest integer divisor where image fits in current window
    const idealScale = percentOfMonitor;
    
    // Find largest integer scale factor that doesn't exceed ideal scale
    // Limit to a reasonable range (1/10 to 1x)
    let scaleFactor = 1;
    for (let i = 1; i <= 10; i++) {
      if (1/i <= idealScale) {
        scaleFactor = 1/i;
        break;
      }
    }
    
    console.log(`- Ideal scale: ${idealScale.toFixed(2)}, using integer scale: ${scaleFactor}`);
    
    // Apply integer scaling
    const newWidth = Math.round(naturalWidth * scaleFactor);
    const newHeight = Math.round(naturalHeight * scaleFactor);
    
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

