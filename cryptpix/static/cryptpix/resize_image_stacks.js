

function resizeImageStacks() {
  console.log('resizeImageStacks running at', new Date().toISOString());

  // Helper function to parse dimension (pixels or percentage)
  function parseDimension(value, baseDimension, isParentSize, parentDimension) {
    console.log('parseDimension called with:', { value, baseDimension, isParentSize, parentDimension });
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
      console.log('Calculated parent-based percentage dimension:', result);
      return result;
    }
    if (trimmedValue.endsWith('%')) {
      const percentage = parseFloat(trimmedValue) / 100;
      if (isNaN(percentage)) {
        console.warn('Invalid percentage value:', trimmedValue);
        return baseDimension;
      }
      const result = Math.round(baseDimension * percentage);
      console.log('Calculated natural percentage dimension:', result);
      return result;
    }
    const result = parseInt(trimmedValue, 10);
    if (isNaN(result)) {
      console.warn('Invalid pixel value:', trimmedValue);
      return baseDimension;
    }
    console.log('Parsed pixel dimension:', result);
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
    console.log('tileSize:', tileSize);

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
    console.log('Natural dimensions:', { naturalWidth, naturalHeight });

    const isParentSize = tileMeta.dataset.parentSize === 'true';
    console.log('isParentSize:', isParentSize);

    // Use #photo-container as parent
    const parentContainer = isParentSize ? stack.closest('#photo-container') : null;
    if (isParentSize && !parentContainer) {
      console.warn('No #photo-container found for image-stack:', stack);
      return;
    }

    const parentWidth = isParentSize ? parentContainer.getBoundingClientRect().width : naturalWidth;
    const parentHeight = isParentSize ? parentContainer.getBoundingClientRect().height : naturalHeight;
    console.log('Parent dimensions:', { parentWidth, parentHeight, parent: parentContainer });

    if (isParentSize && (parentWidth === 0 || parentHeight === 0)) {
      console.warn('Selected #photo-container has zero width or height:', parentContainer);
    }

    const breakpoints = JSON.parse(tileMeta.dataset.breakpoints || '[]');
    console.log('Breakpoints:', breakpoints);
    const currentWidth = window.innerWidth;
    console.log('Current window width:', currentWidth);

    let targetWidth = naturalWidth;
    let targetHeight = naturalHeight;

    // Check for user-defined width and height
    const widthAttr = tileMeta.dataset.width || (isParentSize ? '100%' : null);
    const heightAttr = tileMeta.dataset.height;
    console.log('Attributes:', { widthAttr, heightAttr });

    if (widthAttr) {
      console.log('Processing user-defined dimensions:', { width: widthAttr, height: heightAttr });
      targetWidth = parseDimension(widthAttr, naturalWidth, isParentSize, parentWidth);
      // Calculate height proportionally based on targetWidth and aspect ratio
      const aspectRatio = naturalHeight / naturalWidth;
      targetHeight = Math.round(targetWidth * aspectRatio);
      console.log('Proportional height calculated:', { targetWidth, aspectRatio, targetHeight });
    } else {
      // Apply breakpoints if defined
      for (const bp of breakpoints) {
        if (currentWidth <= bp.maxWidth && bp.width) {
          console.log('Applying breakpoint:', bp);
          targetWidth = parseDimension(bp.width, naturalWidth, isParentSize, parentWidth);
          // Calculate height proportionally based on targetWidth and aspect ratio
          const aspectRatio = naturalHeight / naturalWidth;
          targetHeight = Math.round(targetWidth * aspectRatio);
          console.log('Proportional height calculated for breakpoint:', { targetWidth, aspectRatio, targetHeight });
          break;
        }
      }
    }
    console.log('Target dimensions:', { targetWidth, targetHeight });

    // Quantize dimensions to the nearest tile size multiple
    const scaledWidth = Math.round(targetWidth / tileSize) * tileSize;
    const scaledHeight = Math.round(targetHeight / tileSize) * tileSize;
    console.log('Scaled dimensions:', { scaledWidth, scaledHeight });

    stack.style.width = `${scaledWidth}px`;
    stack.style.height = `${scaledHeight}px`;
    console.log('Applied styles to image-stack:', { width: stack.style.width, height: stack.style.height });
  });
}

window.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded fired at', new Date().toISOString());
  requestAnimationFrame(() => {
    console.log('requestAnimationFrame running resizeImageStacks');
    resizeImageStacks();
  });
});
window.addEventListener('resize', () => {
  console.log('Window resize event at', new Date().toISOString());
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
