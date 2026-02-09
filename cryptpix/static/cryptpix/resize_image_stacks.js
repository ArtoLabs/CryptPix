/* ============================================================= */
/* CryptPix: resize_image_stacks.js                               */
/* Updated for: single-element background-layer rendering         */
/* ============================================================= */

(function () {
  let _resizeScheduled = false;

  function scheduleResize() {
    if (_resizeScheduled) return;
    _resizeScheduled = true;
    requestAnimationFrame(() => {
      _resizeScheduled = false;
      resizeImageStacks();
    });
  }

  function snapToDevicePixels(cssPx) {
    const dpr = window.devicePixelRatio || 1;
    return Math.round(cssPx * dpr) / dpr;
  }

  // Helper function to parse dimension (pixels or percentage)
  function parseDimension(value, baseDimension, isParentSize, parentDimension) {
    if (!value || typeof value !== "string") return baseDimension;

    const trimmedValue = value.trim();

    // Percent relative to parent container (only when explicitly enabled)
    if (trimmedValue.endsWith("%") && isParentSize) {
      const pct = parseFloat(trimmedValue) / 100;
      if (!isFinite(pct) || parentDimension === 0) return baseDimension;
      return Math.round(parentDimension * pct);
    }

    // Percent relative to natural dimension
    if (trimmedValue.endsWith("%")) {
      const pct = parseFloat(trimmedValue) / 100;
      if (!isFinite(pct)) return baseDimension;
      return Math.round(baseDimension * pct);
    }

    const px = parseInt(trimmedValue, 10);
    return isNaN(px) ? baseDimension : px;
  }

  function safeJsonParse(raw, fallback) {
    try {
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function getTileMeta(stack) {
    const tileMeta = stack.querySelector(".tile-meta");
    if (!tileMeta) return null;
    return tileMeta;
  }

  function getNaturalDims(tileMeta) {
    // New background-rendering path stores natural dimensions on tile-meta
    const nw = parseInt(tileMeta.dataset.naturalWidth, 10);
    const nh = parseInt(tileMeta.dataset.naturalHeight, 10);

    if (isFinite(nw) && isFinite(nh) && nw > 0 && nh > 0) {
      return { naturalWidth: nw, naturalHeight: nh };
    }

    // Back-compat: old markup stored natural dims on top IMG
    const stack = tileMeta.closest(".image-stack");
    if (!stack) return null;
    const topImg = stack.querySelector("img[data-natural-width][data-natural-height]");
    if (!topImg) return null;

    const oldW = parseInt(topImg.getAttribute("data-natural-width"), 10);
    const oldH = parseInt(topImg.getAttribute("data-natural-height"), 10);
    if (!isFinite(oldW) || !isFinite(oldH) || oldW <= 0 || oldH <= 0) return null;

    return { naturalWidth: oldW, naturalHeight: oldH };
  }

  function resizeImageStacks() {
    document.querySelectorAll(".image-stack").forEach(function (stack) {
      const tileMeta = getTileMeta(stack);
      if (!tileMeta) return;

      const dims = getNaturalDims(tileMeta);
      if (!dims) return;

      const naturalWidth = dims.naturalWidth;
      const naturalHeight = dims.naturalHeight;

      const isParentSize =
        String(tileMeta.dataset.parentSize).toLowerCase() === "true";

      // Prefer a stable parent container when parent sizing is enabled
      const parentContainer = isParentSize ? stack.closest("#photo-container") : null;

      const parentRect = parentContainer ? parentContainer.getBoundingClientRect() : null;
      const parentWidth = parentRect ? parentRect.width : naturalWidth;
      const parentHeight = parentRect ? parentRect.height : naturalHeight;

      const breakpoints = safeJsonParse(tileMeta.dataset.breakpoints || "[]", []);
      const currentWidth = window.innerWidth;

      const widthAttr = tileMeta.dataset.width || (isParentSize ? "100%" : null);
      const heightAttr = tileMeta.dataset.height || null;

      const aspectRatio = naturalHeight / naturalWidth;

      let targetWidth = naturalWidth;
      let targetHeight = naturalHeight;

      // 1) Explicit width wins
      if (widthAttr) {
        targetWidth = parseDimension(widthAttr, naturalWidth, isParentSize, parentWidth);
        targetHeight = Math.round(targetWidth * aspectRatio);
      } else {
        // 2) Breakpoints (width-based) next
        for (const bp of breakpoints) {
          if (currentWidth <= bp.maxWidth && bp.width) {
            targetWidth = parseDimension(bp.width, naturalWidth, isParentSize, parentWidth);
            targetHeight = Math.round(targetWidth * aspectRatio);
            break;
          }
        }
      }

      // 3) Optional explicit height override (keeps aspect)
      if (heightAttr) {
        targetHeight = parseDimension(heightAttr, naturalHeight, isParentSize, parentHeight);
        targetWidth = Math.round(targetHeight / aspectRatio);
      }

      // 4) Critical: snap the element box to the device pixel grid.
      // This prevents fractional box sizes that can cause sampling drift.
      const scaledWidth = snapToDevicePixels(targetWidth);
      const scaledHeight = snapToDevicePixels(targetHeight);

      stack.style.width = `${scaledWidth}px`;
      stack.style.height = `${scaledHeight}px`;
    });
  }

  /* ============================================================= */
  /* Resize wiring: window + ResizeObserver                        */
  /* ============================================================= */

  window.addEventListener("DOMContentLoaded", () => {
    scheduleResize();

    // Observe likely container(s) so layout changes from outside CSS reflow still snap cleanly.
    if ("ResizeObserver" in window) {
      const ro = new ResizeObserver(() => scheduleResize());

      // Observe all stacks (their box changes can matter)
      document.querySelectorAll(".image-stack").forEach(el => ro.observe(el));

      // Observe all #photo-container instances (your templates use this)
      document.querySelectorAll("#photo-container").forEach(el => ro.observe(el));

      // Also observe the document element for font-size/layout shifts
      ro.observe(document.documentElement);
    }
  });

  window.addEventListener("resize", () => scheduleResize());

  /* ============================================================= */
  /* Right-click prevention (kept; mostly legacy)                  */
  /* ============================================================= */

  document.addEventListener(
    "contextmenu",
    function (event) {
      // Old path: IMG elements
      if (event.target.tagName === "IMG") {
        event.preventDefault();
        return false;
      }
      // New path: background-layer stacks
      const stack = event.target.closest && event.target.closest(".image-stack");
      if (stack) {
        event.preventDefault();
        return false;
      }
    },
    false
  );

  document.addEventListener(
    "mousedown",
    function (event) {
      // Old path: right mouse on IMG
      if (event.button === 2 && event.target.tagName === "IMG") {
        console.log("Right-clicking on images is disabled");
        return false;
      }
      // New path: right mouse on stack
      if (event.button === 2 && event.target.closest && event.target.closest(".image-stack")) {
        console.log("Right-clicking on images is disabled");
        return false;
      }
    },
    false
  );

  /* ============================================================= */
  /* 1. LAZY LOADER – legacy (kept for back-compat)                */
  /* ============================================================= */

  class LazyLoader {
    constructor() {
      this.observer = new IntersectionObserver(this.handleIntersect.bind(this), {
        rootMargin: "200px",
      });
      this.tracked = new Set();
    }

    observe(img) {
      if (!img.dataset.src || img.classList.contains("loaded")) return;
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
      this.tracked.forEach((img) => this.observer.unobserve(img));
    }

    reconnect() {
      this.observer.disconnect();
      setTimeout(() => {
        this.tracked.forEach((img) => {
          if (!img.classList.contains("loaded")) {
            this.observer.observe(img);
          }
        });
      }, 0);
    }

    handleIntersect(entries) {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        this.loadImage(entry.target);
      });
    }

    loadImage(img) {
      const src = img.dataset.src;
      img.src = src;

      const poll = () => {
        if (img.complete && img.naturalWidth > 0) {
          img.classList.add("loaded");
          this.unobserve(img);
        } else {
          requestAnimationFrame(poll);
        }
      };
      poll();
    }
  }

  /* ============================================================= */
  /* 2. SCROLL SPEED – measures px/s, emits fast/slow events       */
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
      this.callbacks.forEach((c) => c.event === event && c.cb(data));
    }

    loop = () => {
      const now = performance.now();
      const y = window.scrollY;
      const dt = now - this.lastT || 1;
      const dy = Math.abs(y - this.lastY);
      const speed = dy / (dt / 1000);

      const wasFast = this.isFast;
      this.isFast = speed > this.threshold;

      if (!wasFast && this.isFast) this.emit("fast");
      if (wasFast && !this.isFast) this.emit("slow");

      this.lastY = y;
      this.lastT = now;
      requestAnimationFrame(this.loop);
    };
  }

  /* ============================================================= */
  /* 3. SCROLL CONTROLLER – pauses/resumes loader on fling         */
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
      this.speed.on("fast", () => this.pause());
      this.speed.on("slow", () => this.scheduleResume());
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
      this.loader.reconnect();
    }

    observeVisible() {
      const vh = window.innerHeight;
      const top = window.scrollY;
      const bot = top + vh;
      const buf = 300;

      document.querySelectorAll("img.lazy").forEach((img) => {
        if (img.classList.contains("loaded")) return;

        if (!this.loader.tracked.has(img)) {
          this.loader.tracked.add(img);
        }

        const rect = img.getBoundingClientRect();
        const imgTop = rect.top + window.scrollY;
        const imgBottom = imgTop + rect.height;

        if (imgBottom > top - buf && imgTop < bot + buf) {
          this.loader.observer.observe(img);
        }
      });
    }
  }

  /* ============================================================= */
  /* 4. BOOTSTRAP – wire everything together                       */
  /* ============================================================= */

  document.addEventListener("DOMContentLoaded", () => {
    const loader = new LazyLoader();
    const speed = new ScrollSpeed(3000);
    const controller = new ScrollController(loader, speed, 180);

    // Observe ALL lazy images (legacy path)
    const lazyImages = document.querySelectorAll("img.lazy");
    console.log(`Found ${lazyImages.length} lazy images on load`);
    lazyImages.forEach((img) => loader.observe(img));

    speed.start();
    controller.start();
    controller.observeVisible();

    window._debugLazy = { loader, speed, controller };
  });
})();
