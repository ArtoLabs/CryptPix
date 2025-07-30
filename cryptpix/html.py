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

  const monitorWidth = window.screen.width;
  const windowWidth = window.innerWidth;
  const percentOfMonitor = windowWidth / monitorWidth;

  console.log(`- Monitor width: ${monitorWidth}px`);
  console.log(`- Window width: ${windowWidth}px`);
  console.log(`- Window is ${(percentOfMonitor * 100).toFixed(1)}% of monitor width`);

  const tileSize = 40; // Change this to your checkerboard tile size

  // Step 1: Build list of scale factors that keep tiles aligned
  const allowedScales = [];
  for (let divisor = 1; divisor <= tileSize; divisor++) {
    const scale = 1 / divisor;
    const scaledTile = tileSize * scale;

    // Only include if tile ends up an integer size
    if (Math.abs(scaledTile - Math.round(scaledTile)) < 0.01) {
      allowedScales.push(scale);
    }
  }

  // Sort largest to smallest
  allowedScales.sort((a, b) => b - a);

  // Step 2: Pick the largest allowed scale <= current percent of monitor
  const chosenScale = allowedScales.find(scale => scale <= percentOfMonitor) || allowedScales.at(-1);

  console.log(`- Chosen scale factor: ${chosenScale} (tile size becomes ${tileSize * chosenScale}px)`);

  document.querySelectorAll('.image-stack').forEach(function(stack, index) {
    console.log(`Processing stack #${index}`);

    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) {
      console.log(`- Stack #${index} has no image with required attributes`);
      return;
    }

    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);

    const newWidth = Math.floor(naturalWidth * chosenScale);
    const newHeight = Math.floor(naturalHeight * chosenScale);

    console.log(`- Natural dimensions: ${naturalWidth}x${naturalHeight}`);
    console.log(`- New dimensions: ${newWidth}x${newHeight} (scale=${chosenScale})`);

    stack.style.width = `${newWidth}px`;
    stack.style.height = `${newHeight}px`;
    stack.style.imageRendering = 'pixelated';

    // Optional debug info
    const computedStyle = window.getComputedStyle(stack);
    console.log(`- Applied style: width=${stack.style.width}, height=${stack.style.height}`);
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

def render_image_stack(url1, url2, tile_size, top_img_attrs=""):
    return format_html("""
<div class="image-stack">
  <img src="{}" alt="Layer 1">
  <img src="{}" {} >
  <div class="tile-meta" data-tile-size="{}" hidden></div>
</div>
""", url1, url2, top_img_attrs, tile_size)


