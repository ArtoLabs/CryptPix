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
  const monitorWidth = window.screen.width;
  const windowWidth = window.innerWidth;
  const percentOfMonitor = windowWidth / monitorWidth;

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

    const scaledWidth = naturalWidth * percentOfMonitor;
    const scaledHeight = naturalHeight * percentOfMonitor;

    const roundedWidth = tileSize * Math.round(scaledWidth / tileSize);
    const roundedHeight = tileSize * Math.round(scaledHeight / tileSize);

    stack.style.width = `${roundedWidth}px`;
    stack.style.height = `${roundedHeight}px`;
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


