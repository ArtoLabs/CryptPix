def get_css():
    return """
<style>
  .image-stack {
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
    height: auto;
    object-fit: cover;
  }
</style>
"""

def get_js():
    return """
<script>
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.image-stack').forEach(function(stack) {
      const img = new Image();
      img.onload = function() {
        stack.style.width = this.width + 'px';
        stack.style.height = this.height + 'px';
      };
      img.src = stack.querySelector('img').src;
    });
  });
</script>
"""

def render_image_stack(url1, url2):
    return f"""
<div class="image-stack">
  <img src="{url1}" alt="Layer 1">
  <img src="{url2}" alt="Layer 2">
</div>
"""

def render_full_html(url1, url2):
    return get_css() + get_js() + render_image_stack(url1, url2)
