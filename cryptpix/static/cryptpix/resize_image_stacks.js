

function resizeImageStacks() {

  // Helper function to parse dimension (pixels or percentage)
  function parseDimension(value, parentSize) {
    if (!value) return null;

    if (typeof value === "number") return value;

    const str = value.toString().trim();

    if (str.endsWith("%")) {
      const percent = parseFloat(str.replace("%", ""));
      if (isNaN(percent)) return null;
      return Math.floor(parentSize * (percent / 100));
    }

    if (str.endsWith("px")) {
      const px = parseInt(str.replace("px", ""), 10);
      return isNaN(px) ? null : px;
    }

    const num = parseInt(str, 10);
    return isNaN(num) ? null : num;
  }

  document
    .querySelectorAll('.cryptpix-media[data-cp-mode="stack"]')
    .forEach(function (stack) {

      const tileMeta = stack.querySelector(".cryptpix-meta");
      if (!tileMeta) {
        console.warn("No cryptpix-meta found in stack:", stack);
        return;
      }

      const tileSize = parseInt(tileMeta.dataset.tileSize, 10);
      if (isNaN(tileSize) || tileSize <= 0) {
        console.warn("Invalid tile size in cryptpix-meta:", tileMeta);
        return;
      }

      const naturalWidth = parseInt(stack.getAttribute("data-natural-width"), 10);
      const naturalHeight = parseInt(stack.getAttribute("data-natural-height"), 10);

      if (isNaN(naturalWidth) || isNaN(naturalHeight)) {
        console.warn("Invalid natural width/height on cryptpix wrapper:", stack);
        return;
      }

      const isParentSize = tileMeta.dataset.parentSize === "true";

      // Use #photo-container as parent when requested
      const parentContainer = isParentSize
        ? stack.closest("#photo-container")
        : null;

      const parentWidth = parentContainer
        ? parentContainer.clientWidth
        : stack.parentElement
        ? stack.parentElement.clientWidth
        : null;

      if (!parentWidth) {
        console.warn("Unable to determine parent width for stack:", stack);
        return;
      }

      let targetWidth = parentWidth;
      let targetHeight = Math.floor(
        (naturalHeight / naturalWidth) * targetWidth
      );

      // Explicit width/height overrides from meta
      const widthAttr = tileMeta.dataset.width;
      const heightAttr = tileMeta.dataset.height;

      if (widthAttr) {
        const parsedWidth = parseDimension(widthAttr, parentWidth);
        if (parsedWidth) {
          targetWidth = parsedWidth;
          targetHeight = Math.floor(
            (naturalHeight / naturalWidth) * targetWidth
          );
        }
      }

      if (heightAttr) {
        const parsedHeight = parseDimension(heightAttr, parentWidth);
        if (parsedHeight) {
          targetHeight = parsedHeight;
          targetWidth = Math.floor(
            (naturalWidth / naturalHeight) * targetHeight
          );
        }
      }

      // Snap to tile grid
      const scaledWidth =
        Math.round(targetWidth / tileSize) * tileSize;
      const scaledHeight =
        Math.round(targetHeight / tileSize) * tileSize;

      stack.style.width = `${scaledWidth}px`;
      stack.style.height = `${scaledHeight}px`;
    });
}

// Optional: auto-run on load + resize
//window.addEventListener("load", resizeImageStacks);
//window.addEventListener("resize", resizeImageStacks);

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



/* ============================================================= */
/* 1. LAZY LOADER – fixed, reliable, forces re-entry after pause */
/* ============================================================= */
class LazyLoader {
  constructor() {
    this.observer = new IntersectionObserver(
      this.handleIntersect.bind(this),
      { rootMargin: '200px' }
    );
    this.tracked = new Set();   // all images we are watching
  }

  observe(img) {
    if (!img.dataset.src || img.classList.contains('loaded')) return;
    if (!this.tracked.has(img)) {
      this.tracked.add(img);
      this.observer.observe(img);
    }
  }

  unobserve(img) {
    this.tracked.delete(img);
    this.observer.unobserve(img);
  }

  unobserveAll() {
    this.tracked.forEach(img => this.observer.unobserve(img));
  }

  // CRITICAL: Forces observer to re-check all entries
    reconnect() {
      this.observer.disconnect();
      setTimeout(() => {
        this.tracked.forEach(img => {
          if (!img.classList.contains('loaded')) {
            this.observer.observe(img);  // observe ALL
          }
        });
      }, 0);
    }

  handleIntersect(entries) {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      this.loadImage(entry.target);
    });
  }

  loadImage(img) {
    const src = img.dataset.src;
    img.src = src;

    const poll = () => {
      if (img.complete && img.naturalWidth > 0) {
        img.classList.add('loaded');
        this.unobserve(img);
      } else {
        requestAnimationFrame(poll);
      }
    };
    poll();
  }
}

/* ============================================================= */
/* 2. SCROLL SPEED – measures px/s, emits fast/slow events     */
/* ============================================================= */
class ScrollSpeed {
  constructor(threshold = 3000) {
    this.threshold = threshold;
    this.lastY = window.scrollY;
    this.lastT = performance.now();
    this.isFast = false;
    this.callbacks = [];
  }

  start() {
    this.loop();
  }

  on(event, cb) {
    this.callbacks.push({ event, cb });
  }

  emit(event, data) {
    this.callbacks.forEach(c => c.event === event && c.cb(data));
  }

  loop = () => {
    const now = performance.now();
    const y = window.scrollY;
    const dt = now - this.lastT || 1;
    const dy = Math.abs(y - this.lastY);
    const speed = dy / (dt / 1000);

    const wasFast = this.isFast;
    this.isFast = speed > this.threshold;

    if (!wasFast && this.isFast) this.emit('fast');
    if (wasFast && !this.isFast) this.emit('slow');

    this.lastY = y;
    this.lastT = now;
    requestAnimationFrame(this.loop);
  };
}

/* ============================================================= */
/* 3. SCROLL CONTROLLER – pauses/resumes loader on fling       */
/* ============================================================= */
class ScrollController {
  constructor(loader, speed, settleMs = 180) {
    this.loader = loader;
    this.speed = speed;
    this.settleMs = settleMs;
    this.settleTimer = null;
    this.paused = false;
  }

  start() {
    this.speed.on('fast', () => this.pause());
    this.speed.on('slow', () => this.scheduleResume());
  }

  pause() {
    if (this.paused) return;
    this.paused = true;
    this.loader.unobserveAll();
    clearTimeout(this.settleTimer);
  }

  scheduleResume() {
    clearTimeout(this.settleTimer);
    this.settleTimer = setTimeout(() => {
      this.resume();
    }, this.settleMs);
  }

  resume() {
    if (!this.paused) return;
    this.paused = false;
    this.observeVisible();
    this.loader.reconnect();  // Forces IntersectionObserver to re-check
  }

    observeVisible() {
      const vh = window.innerHeight;
      const top = window.scrollY;
      const bot = top + vh;
      const buf = 300;

      let observed = 0;
      document.querySelectorAll('img.lazy').forEach(img => {
        if (img.classList.contains('loaded')) return;

        // ADD TO TRACKED (even if not visible)
        if (!this.loader.tracked.has(img)) {
          this.loader.tracked.add(img);
        }

        const rect = img.getBoundingClientRect();
        const imgTop = rect.top + window.scrollY;
        const imgBottom = imgTop + rect.height;

        if (imgBottom > top - buf && imgTop < bot + buf) {
          this.loader.observer.observe(img);
          observed++;
        }
      });

      //console.log(`→ Re-observed ${observed} visible images (total tracked: ${this.loader.tracked.size})`);
    }
}

/* ============================================================= */
/* 4. BOOTSTRAP – wire everything together                     */
/* ============================================================= */
document.addEventListener('DOMContentLoaded', () => {
  const loader = new LazyLoader();
  const speed = new ScrollSpeed(3000);
  const controller = new ScrollController(loader, speed, 180);

  // Observe ALL lazy images
  const lazyImages = document.querySelectorAll('img.lazy');
  console.log(`Found ${lazyImages.length} lazy images on load`);
  lazyImages.forEach(img => loader.observe(img));

  // Start systems
  speed.start();
  controller.start();

  // Initial visible load
  controller.observeVisible();

  // Debug helper
  window._debugLazy = { loader, speed, controller };
});




