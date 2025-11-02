

function resizeImageStacks() {

  // Helper function to parse dimension (pixels or percentage)
  function parseDimension(value, baseDimension, isParentSize, parentDimension) {
    if (!value || typeof value !== 'string') {
      console.log('Invalid or missing value, using baseDimension:', baseDimension);
      return baseDimension;
    }
    const trimmedValue = value.trim();
    if (trimmedValue.endsWith('%') && isParentSize) {
      if (parentDimension === 0) {
        console.warn('Parent dimension is 0; falling back to base dimension:', baseDimension);
        return baseDimension;
      }
      const percentage = parseFloat(trimmedValue) / 100;
      if (isNaN(percentage)) {
        console.warn('Invalid percentage value:', trimmedValue);
        return baseDimension;
      }
      const result = Math.round(parentDimension * percentage);
      return result;
    }
    if (trimmedValue.endsWith('%')) {
      const percentage = parseFloat(trimmedValue) / 100;
      if (isNaN(percentage)) {
        console.warn('Invalid percentage value:', trimmedValue);
        return baseDimension;
      }
      const result = Math.round(baseDimension * percentage);
      return result;
    }
    const result = parseInt(trimmedValue, 10);
    if (isNaN(result)) {
      console.warn('Invalid pixel value:', trimmedValue);
      return baseDimension;
    }
    return result;
  }

  document.querySelectorAll('.image-stack').forEach(function(stack) {
    console.log('Processing image-stack:', stack);

    const tileMeta = stack.querySelector('.tile-meta');
    if (!tileMeta) {
      console.warn('No tile-meta found in image-stack:', stack);
      return;
    }

    const tileSize = parseInt(tileMeta.dataset.tileSize, 10);
    if (isNaN(tileSize)) {
      console.warn('Invalid tileSize in tile-meta:', tileMeta.dataset.tileSize);
      return;
    }

    const topImg = stack.querySelector('img[data-natural-width][data-natural-height]');
    if (!topImg) {
      console.warn('No image with data-natural-width/height found in image-stack:', stack);
      return;
    }

    const naturalWidth = parseInt(topImg.getAttribute('data-natural-width'), 10);
    const naturalHeight = parseInt(topImg.getAttribute('data-natural-height'), 10);
    if (isNaN(naturalWidth) || isNaN(naturalHeight)) {
      console.warn('Invalid natural width/height in image:', topImg);
      return;
    }


    const isParentSize = tileMeta.dataset.parentSize === 'true';

    // Use #photo-container as parent
    const parentContainer = isParentSize ? stack.closest('#photo-container') : null;

    const parentWidth = isParentSize ? parentContainer.getBoundingClientRect().width : naturalWidth;
    const parentHeight = isParentSize ? parentContainer.getBoundingClientRect().height : naturalHeight;

    const breakpoints = JSON.parse(tileMeta.dataset.breakpoints || '[]');

    const currentWidth = window.innerWidth;


    let targetWidth = naturalWidth;
    let targetHeight = naturalHeight;

    // Check for user-defined width and height
    const widthAttr = tileMeta.dataset.width || (isParentSize ? '100%' : null);
    const heightAttr = tileMeta.dataset.height;


    if (widthAttr) {
      targetWidth = parseDimension(widthAttr, naturalWidth, isParentSize, parentWidth);
      // Calculate height proportionally based on targetWidth and aspect ratio
      const aspectRatio = naturalHeight / naturalWidth;
      targetHeight = Math.round(targetWidth * aspectRatio);
    } else {
      // Apply breakpoints if defined
      for (const bp of breakpoints) {
        if (currentWidth <= bp.maxWidth && bp.width) {
          targetWidth = parseDimension(bp.width, naturalWidth, isParentSize, parentWidth);
          // Calculate height proportionally based on targetWidth and aspect ratio
          const aspectRatio = naturalHeight / naturalWidth;
          targetHeight = Math.round(targetWidth * aspectRatio);
          break;
        }
      }
    }
    console.log('Target dimensions:', { targetWidth, targetHeight });

    // Quantize dimensions to the nearest tile size multiple
    const scaledWidth = Math.round(targetWidth / tileSize) * tileSize;
    const scaledHeight = Math.round(targetHeight / tileSize) * tileSize;
    stack.style.width = `${scaledWidth}px`;
    stack.style.height = `${scaledHeight}px`;
  });
}

window.addEventListener('DOMContentLoaded', () => {
  requestAnimationFrame(() => {
    resizeImageStacks();
  });
});
window.addEventListener('resize', () => {
  resizeImageStacks();
});

// Prevent right-clicking only on images
document.addEventListener('contextmenu', function(event) {
  // Check if the clicked element is an image
  if (event.target.tagName === 'IMG') {
    event.preventDefault();
    return false;
  }
  // Allow context menu on all other elements
}, false);

// Optional: Add a message when users attempt to right-click on images
document.addEventListener('mousedown', function(event) {
  if (event.button === 2 && event.target.tagName === 'IMG') { // Right mouse button on image
    console.log('Right-clicking on images is disabled');
    return false;
  }
}, false);


document.addEventListener("DOMContentLoaded", () => {
    const lazyImages = document.querySelectorAll("img.lazy");

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const img = entry.target;

            // Swap in the real src
            const realSrc = img.dataset.src;
            img.src = realSrc;

            // Poll until the real image is decoded
            const checkLoaded = () => {
                if (img.complete && img.naturalWidth > 1) {  // >1 = not 1x1 placeholder
                    console.log("REAL IMAGE DECODED — FADING IN");
                    img.classList.add("loaded");
                    obs.unobserve(img);
                } else {
                    requestAnimationFrame(checkLoaded);
                }
            };

            checkLoaded();
            obs.unobserve(img);
        });
    });

    lazyImages.forEach(img => observer.observe(img));
});



