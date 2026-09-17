const {
  Plugin,
  PluginSettingTab,
  Setting,
  MarkdownView,
  Notice,
} = require("obsidian");

/* =========================================================================
   1. UTILS & LOGGER MODULE
   ========================================================================= */

class HeatmapLogger {
  constructor(pluginId) {
    this.pluginId = pluginId;
    this.debugEnabled = false;
  }

  setDebug(enabled) {
    this.debugEnabled = enabled;
  }

  log(level, ...args) {
    const timestamp = new Date().toISOString();
    const prefix = `[${timestamp}] [${this.pluginId}] [${level}]`;
    if (level === "DEBUG") {
      if (this.debugEnabled) {
        console.log(prefix, ...args);
      }
    } else if (level === "WARN") {
      console.warn(prefix, ...args);
    } else if (level === "ERROR") {
      console.error(prefix, ...args);
    } else {
      console.log(prefix, ...args);
    }
  }

  debug(...args) {
    this.log("DEBUG", ...args);
  }
  info(...args) {
    this.log("INFO", ...args);
  }
  warn(...args) {
    this.log("WARN", ...args);
  }
  error(...args) {
    this.log("ERROR", ...args);
  }
}

const logger = new HeatmapLogger("HeatmapOfNotes");

/* =========================================================================
   2. ACTIVITY MONITOR MODULE
   ========================================================================= */

class ActivityMonitor {
  constructor(idleThresholdSeconds) {
    this.idleThresholdMs = idleThresholdSeconds * 1000;
    this.lastActivityTime = Date.now();
    this.boundHandlers = [];
  }

  setIdleThreshold(seconds) {
    this.idleThresholdMs = seconds * 1000;
    logger.debug(`Idle threshold updated to ${seconds}s.`);
  }

  recordActivity() {
    this.lastActivityTime = Date.now();
  }

  start() {
    this.recordActivity();

    const handleEvent = () => {
      this.recordActivity();
    };

    const events = [
      "mousemove",
      "keydown",
      "wheel",
      "touchstart",
      "click",
      "scroll",
    ];
    events.forEach((evt) => {
      window.addEventListener(evt, handleEvent, { passive: true });
      this.boundHandlers.push({
        element: window,
        event: evt,
        handler: handleEvent,
      });
    });

    document.addEventListener("visibilitychange", handleEvent);
    this.boundHandlers.push({
      element: document,
      event: "visibilitychange",
      handler: handleEvent,
    });

    logger.debug("ActivityMonitor listeners registered successfully.");
  }

  isUserActive() {
    if (document.hidden) return false;
    return Date.now() - this.lastActivityTime < this.idleThresholdMs;
  }

  destroy() {
    this.boundHandlers.forEach(({ element, event, handler }) => {
      element.removeEventListener(event, handler);
    });
    this.boundHandlers = [];
    logger.debug("ActivityMonitor destroyed.");
  }
}

/* =========================================================================
   3. PERSISTENT STORAGE MODULE (DATABASE)
   ========================================================================= */

const DEFAULT_SETTINGS = {
  idleSeconds: 30,
  bucketCount: 100,
  heatmapWidth: 16,
  heatmapOffsetRight: 12,
  heatmapOpacity: 0.85,
  refreshIntervalMs: 1000,
  debugMode: false,
};

class HeatmapDatabase {
  constructor(plugin) {
    this.plugin = plugin;
    this.settings = Object.assign({}, DEFAULT_SETTINGS);
    this.records = {};
    this.lastSaveTime = Date.now();
  }

  async load() {
    try {
      const rawData = await this.plugin.loadData();
      if (rawData) {
        this.settings = Object.assign(
          {},
          DEFAULT_SETTINGS,
          rawData.settings || {},
        );
        this.records = rawData.records || {};
        logger.setDebug(this.settings.debugMode);
        logger.info("Database loaded successfully.");
      } else {
        logger.info("No existing database found. Creating a fresh copy.");
      }
    } catch (err) {
      logger.error("Failed to load database from disk. Using defaults.", err);
    }
  }

  async save(force = false) {
    const now = Date.now();
    if (!force && now - this.lastSaveTime < 10000) {
      return;
    }

    try {
      await this.plugin.saveData({
        settings: this.settings,
        records: this.records,
      });
      this.lastSaveTime = Date.now();
      logger.debug("Database persisted to disk.");
    } catch (err) {
      logger.error("Failed to save database to disk.", err);
    }
  }

  getOrCreateRecord(path) {
    const defaultBuckets = Array(this.settings.bucketCount).fill(0);
    const defaultVisits = Array(this.settings.bucketCount).fill(0);

    if (!this.records[path]) {
      this.records[path] = {
        totalTimeMs: 0,
        visits: 0,
        lastAccessed: new Date().toISOString(),
        buckets: defaultBuckets,
        bucketVisits: defaultVisits,
      };
      logger.debug(`Created fresh record for path: ${path}`);
    } else {
      const record = this.records[path];
      if (
        !record.buckets ||
        record.buckets.length !== this.settings.bucketCount
      ) {
        this.records[path].buckets = this.resizeArray(
          record.buckets || [],
          this.settings.bucketCount,
        );
      }
      if (
        !record.bucketVisits ||
        record.bucketVisits.length !== this.settings.bucketCount
      ) {
        this.records[path].bucketVisits = this.resizeArray(
          record.bucketVisits || [],
          this.settings.bucketCount,
        );
      }
    }
    return this.records[path];
  }

  resizeArray(arr, targetSize) {
    if (arr.length === targetSize) return arr;
    const resized = Array(targetSize).fill(0);
    if (arr.length === 0) return resized;

    for (let i = 0; i < targetSize; i++) {
      const srcIndex = (i / targetSize) * arr.length;
      const low = Math.floor(srcIndex);
      const high = Math.min(arr.length - 1, Math.ceil(srcIndex));
      const weight = srcIndex - low;
      resized[i] = Math.round(arr[low] * (1 - weight) + arr[high] * weight);
    }
    return resized;
  }

  recordReadingTime(
    path,
    startBucket,
    endBucket,
    incrementMs,
    newlyVisibleBuckets,
  ) {
    const rec = this.getOrCreateRecord(path);
    rec.totalTimeMs += incrementMs;
    rec.lastAccessed = new Date().toISOString();

    for (let i = startBucket; i <= endBucket; i++) {
      if (i >= 0 && i < rec.buckets.length) {
        rec.buckets[i] += incrementMs;
      }
    }

    newlyVisibleBuckets.forEach((bucketIdx) => {
      if (bucketIdx >= 0 && bucketIdx < rec.bucketVisits.length) {
        rec.bucketVisits[bucketIdx] += 1;
      }
    });

    this.save();
  }

  incrementOverallVisit(path) {
    const rec = this.getOrCreateRecord(path);
    rec.visits += 1;
    this.save();
  }

  handleRename(oldPath, newPath) {
    if (this.records[oldPath]) {
      this.records[newPath] = this.records[oldPath];
      delete this.records[oldPath];
      this.save(true);
      logger.info(`Renamed record: ${oldPath} -> ${newPath}`);
    }
  }

  clearRecord(path) {
    if (this.records[path]) {
      delete this.records[path];
      this.save(true);
      logger.info(`Cleared storage data for: ${path}`);
    }
  }
}

/* =========================================================================
   4. RENDERER MODULE (DYNAMIC ATTENTION PROFILE GRAPH OVERLAY)
   ========================================================================= */

class HeatmapRenderer {
  constructor(view, database) {
    this.view = view;
    this.database = database;

    this.container = null;
    this.canvas = null;
    this.ctx = null;
    this.tooltip = null;

    this.scrollerElement = null;
    this.resizeObserver = null;
    this.animationFrameId = null;

    this.scrollListener = null;
    this.mouseMoveListener = null;
    this.mouseLeaveListener = null;

    this.initDOM();
    this.scrollerElement = this.getScroller();
    this.bindEvents();
    this.resizeCanvas();
  }

  getScroller() {
    if (!this.view) return null;
    const container = this.view.contentEl;
    if (!container) return null;

    const mode =
      typeof this.view.getMode === "function" ? this.view.getMode() : null;

    if (mode === "preview") {
      const preview = container.querySelector(".markdown-preview-view");
      if (preview) return preview;
    } else if (mode === "source") {
      const source = container.querySelector(".cm-scroller");
      if (source) return source;
    }

    const sourceScroller = container.querySelector(".cm-scroller");
    const previewScroller = container.querySelector(".markdown-preview-view");

    if (sourceScroller && sourceScroller.clientHeight > 0) {
      return sourceScroller;
    }
    if (previewScroller && previewScroller.clientHeight > 0) {
      return previewScroller;
    }

    return sourceScroller || previewScroller || null;
  }

  checkAndRebindScroller() {
    this.initDOM();

    const currentScroller = this.getScroller();
    if (!currentScroller) return;

    if (this.scrollerElement !== currentScroller) {
      logger.debug(
        "Active scroller changed (e.g. mode toggle). Rebinding event listeners.",
      );
      this.unbindEvents();
      this.scrollerElement = currentScroller;
      this.bindEvents();
      this.resizeCanvas();
    }
  }

  initDOM() {
    const contentEl = this.view.contentEl;
    if (!contentEl) return;

    if (getComputedStyle(contentEl).position === "static") {
      contentEl.style.position = "relative";
    }

    if (this.container) {
      if (this.container.parentElement !== contentEl) {
        contentEl.appendChild(this.container);
        logger.debug("Re-appended detached heatmap container.");
      } else if (contentEl.lastChild !== this.container) {
        contentEl.appendChild(this.container);
      }
      return;
    }

    this.container = document.createElement("div");
    this.container.className = "frh-heatmap-wrapper";

    const settings = this.database.settings;
    this.container.style.width = `${settings.heatmapWidth}px`;
    this.container.style.right = `${settings.heatmapOffsetRight}px`;
    this.container.style.opacity = `${settings.heatmapOpacity}`;

    this.canvas = document.createElement("canvas");
    this.canvas.className = "frh-heatmap-canvas";
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext("2d");

    contentEl.appendChild(this.container);
    logger.debug("Created and appended new heatmap container.");

    let existingTooltip = document.getElementById("frh-tooltip-element");
    if (!existingTooltip) {
      this.tooltip = document.createElement("div");
      this.tooltip.id = "frh-tooltip-element";
      this.tooltip.className = "frh-heatmap-tooltip";
      document.body.appendChild(this.tooltip);
    } else {
      this.tooltip = existingTooltip;
    }
  }

  bindEvents() {
    if (!this.scrollerElement) return;

    this.scrollListener = () => {
      this.database.plugin.activityMonitor.recordActivity();
      this.draw();
    };
    this.scrollerElement.addEventListener("scroll", this.scrollListener, {
      passive: true,
    });

    this.resizeObserver = new ResizeObserver(() => {
      this.resizeCanvas();
    });
    this.resizeObserver.observe(this.scrollerElement);

    this.mouseMoveListener = (e) => this.handleMouseMove(e);
    this.mouseLeaveListener = () => this.handleMouseLeave();

    if (this.canvas) {
      this.canvas.addEventListener("mousemove", this.mouseMoveListener);
      this.canvas.addEventListener("mouseleave", this.mouseLeaveListener);
    }
  }

  unbindEvents() {
    if (this.scrollerElement) {
      if (this.scrollListener) {
        this.scrollerElement.removeEventListener("scroll", this.scrollListener);
      }
      if (this.resizeObserver) {
        this.resizeObserver.disconnect();
        this.resizeObserver = null;
      }
    }
    if (this.canvas) {
      if (this.mouseMoveListener) {
        this.canvas.removeEventListener("mousemove", this.mouseMoveListener);
      }
      if (this.mouseLeaveListener) {
        this.canvas.removeEventListener("mouseleave", this.mouseLeaveListener);
      }
    }
  }

  resizeCanvas() {
    if (!this.scrollerElement || !this.canvas || !this.container) return;
    const rect = this.container.getBoundingClientRect();

    if (rect.width <= 0 || rect.height <= 0) return;

    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    this.draw();
  }

  draw() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }

    this.animationFrameId = requestAnimationFrame(() => {
      this.paint();
    });
  }

  getAccentColor(alpha = 1) {
    const bodyStyle = getComputedStyle(document.body);
    let colorStr = bodyStyle.getPropertyValue("--interactive-accent").trim();
    if (!colorStr) {
      return `rgba(36, 143, 178, ${alpha})`;
    }

    if (colorStr.startsWith("#")) {
      const clean = colorStr.replace("#", "");
      let r = 36,
        g = 143,
        b = 178;
      if (clean.length === 3) {
        r = parseInt(clean[0] + clean[0], 16);
        g = parseInt(clean[1] + clean[1], 16);
        b = parseInt(clean[2] + clean[2], 16);
      } else if (clean.length === 6) {
        r = parseInt(clean.substring(0, 2), 16);
        g = parseInt(clean.substring(2, 4), 16);
        b = parseInt(clean.substring(4, 6), 16);
      }
      return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    if (colorStr.startsWith("rgb")) {
      const matches = colorStr.match(/\d+/g);
      if (matches && matches.length >= 3) {
        return `rgba(${matches[0]}, ${matches[1]}, ${matches[2]}, ${alpha})`;
      }
    }

    return `rgba(36, 143, 178, ${alpha})`;
  }

  paint() {
    this.checkAndRebindScroller();
    if (!this.canvas || !this.ctx || !this.scrollerElement) return;

    const rect = this.container.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return;

    const dpr = window.devicePixelRatio || 1;
    const expectedWidth = Math.round(rect.width * dpr);
    const expectedHeight = Math.round(rect.height * dpr);

    if (
      this.canvas.width !== expectedWidth ||
      this.canvas.height !== expectedHeight
    ) {
      this.canvas.width = expectedWidth;
      this.canvas.height = expectedHeight;
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      logger.debug(
        `Canvas bounds normalized: ${expectedWidth}px x ${expectedHeight}px`,
      );
    }

    const clientWidth = rect.width;
    const clientHeight = rect.height;

    const ctx = this.ctx;
    ctx.clearRect(0, 0, clientWidth, clientHeight);

    ctx.fillStyle = "rgba(128, 128, 128, 0.03)";
    ctx.fillRect(0, 0, clientWidth, clientHeight);

    const path = this.view.file ? this.view.file.path : null;
    if (!path) return;

    const record = this.database.getOrCreateRecord(path);
    const buckets = record.buckets;
    const bucketCount = buckets.length;

    const maxVal = Math.max(...buckets, 1);
    const itemHeight = clientHeight / bucketCount;

    ctx.beginPath();
    ctx.moveTo(0, 0);
    for (let i = 0; i < bucketCount; i++) {
      const val = buckets[i];
      const weight = val / maxVal;
      const y = (i + 0.5) * itemHeight;
      const x = weight * clientWidth;
      ctx.lineTo(x, y);
    }
    ctx.lineTo(0, clientHeight);
    ctx.closePath();

    ctx.fillStyle = this.getAccentColor(0.18);
    ctx.fill();

    ctx.beginPath();
    for (let i = 0; i < bucketCount; i++) {
      const val = buckets[i];
      const weight = val / maxVal;
      const y = (i + 0.5) * itemHeight;
      const x = weight * clientWidth;
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.strokeStyle = this.getAccentColor(0.85);
    ctx.lineWidth = 2;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.stroke();

    const scrollTop = this.scrollerElement.scrollTop;
    const scrollHeight = this.scrollerElement.scrollHeight;
    const scrollerHeight = this.scrollerElement.clientHeight;

    if (scrollHeight > 0) {
      const startPct = scrollTop / scrollHeight;
      const endPct = (scrollTop + scrollerHeight) / scrollHeight;

      const yStart = startPct * clientHeight;
      const yEnd = Math.min(clientHeight, endPct * clientHeight);

      ctx.fillStyle = this.getAccentColor(0.1);
      ctx.fillRect(0, yStart, clientWidth, yEnd - yStart);

      // White borders for the upper and lower bands to stand out and improve visual contrast
      ctx.strokeStyle = "rgba(255, 255, 255, 0.95)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(0, yStart);
      ctx.lineTo(clientWidth, yStart);
      ctx.moveTo(0, yEnd);
      ctx.lineTo(clientWidth, yEnd);
      ctx.stroke();
    }
  }

  handleMouseMove(e) {
    this.checkAndRebindScroller();
    if (!this.canvas || !this.tooltip) return;
    const rect = this.canvas.getBoundingClientRect();
    const relativeY = e.clientY - rect.top;
    const pct = Math.max(0, Math.min(1, relativeY / rect.height));

    const path = this.view.file ? this.view.file.path : null;
    if (!path) return;

    const record = this.database.getOrCreateRecord(path);
    const bucketCount = record.buckets.length;
    const bucketIdx = Math.floor(pct * bucketCount);

    const ms = record.buckets[bucketIdx] || 0;
    const visits = record.bucketVisits[bucketIdx] || 0;

    const totalSeconds = Math.round(ms / 1000);
    const minStr = Math.floor(totalSeconds / 60);
    const secStr = String(totalSeconds % 60).padStart(2, "0");

    this.tooltip.innerHTML = `
      <div class="frh-heatmap-tooltip-title">Section ~${Math.round(pct * 100)}%</div>
      <div class="frh-heatmap-tooltip-row">
        <span>Time Spent:</span>
        <span class="frh-heatmap-tooltip-value">${minStr}m ${secStr}s</span>
      </div>
      <div class="frh-heatmap-tooltip-row">
        <span>Visits:</span>
        <span class="frh-heatmap-tooltip-value">${visits}</span>
      </div>
    `;

    const tooltipWidth = 140;
    const xPos = e.clientX - tooltipWidth - 15;
    const yPos = Math.max(
      10,
      Math.min(window.innerHeight - 80, e.clientY - 30),
    );

    this.tooltip.style.left = `${xPos}px`;
    this.tooltip.style.top = `${yPos}px`;
    this.tooltip.style.opacity = "1";
  }

  handleMouseLeave() {
    if (this.tooltip) {
      this.tooltip.style.opacity = "0";
    }
  }

  destroy() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    this.unbindEvents();
    if (this.container) {
      this.container.remove();
    }
    logger.debug(`Renderer destroyed for pane view.`);
  }
}

/* =========================================================================
   5. ENGINE MODULE (RUNTIME LOOP & ORCHESTRATOR)
   ========================================================================= */

class HeatmapEngine {
  constructor(plugin, database, activityMonitor) {
    this.plugin = plugin;
    this.database = database;
    this.activityMonitor = activityMonitor;
    this.renderers = new Map();
    this.intervalId = null;
    this.lastVisibleBucketsMap = new Map();
  }

  start() {
    const intervalMs = this.database.settings.refreshIntervalMs;
    this.intervalId = window.setInterval(() => this.tick(), intervalMs);
    logger.debug(`Engine sequence started with cycle rate: ${intervalMs}ms.`);
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.clearAllRenderers();
    logger.debug("Engine sequence terminated.");
  }

  registerView(view) {
    if (this.renderers.has(view)) return;

    logger.debug(`Registering view: ${view.file ? view.file.name : "unknown"}`);

    const renderer = new HeatmapRenderer(view, this.database);

    this.renderers.set(view, renderer);

    if (view.file) {
      this.database.incrementOverallVisit(view.file.path);
    }
  }

  deregisterView(view) {
    const renderer = this.renderers.get(view);
    if (renderer) {
      renderer.destroy();
      this.renderers.delete(view);
      logger.debug(`Deregistered view.`);
    }
  }

  clearAllRenderers() {
    this.renderers.forEach((renderer) => renderer.destroy());
    this.renderers.clear();
    this.lastVisibleBucketsMap.clear();
  }

  syncOpenViews() {
    const activeViews = [];
    this.plugin.app.workspace.iterateAllLeaves((leaf) => {
      if (leaf.view instanceof MarkdownView) {
        activeViews.push(leaf.view);
      }
    });

    for (const [view, renderer] of this.renderers.entries()) {
      if (!activeViews.includes(view)) {
        this.deregisterView(view);
      }
    }

    activeViews.forEach((view) => {
      if (!this.renderers.has(view)) {
        this.registerView(view);
      } else {
        const renderer = this.renderers.get(view);
        if (renderer) {
          renderer.checkAndRebindScroller();
        }
      }
    });
  }

  tick() {
    if (!this.activityMonitor.isUserActive()) {
      return;
    }

    this.renderers.forEach((renderer, view) => {
      if (
        !view.contentEl ||
        view.contentEl.getBoundingClientRect().height <= 0
      ) {
        return;
      }
      this.refreshCurrentActiveViewPort(view);
    });
  }

  refreshCurrentActiveViewPort(view) {
    const path = view.file ? view.file.path : null;
    if (!path) return;

    const renderer = this.renderers.get(view);
    if (!renderer) return;

    renderer.checkAndRebindScroller();

    const scroller = renderer.scrollerElement;
    if (!scroller) return;

    const scrollTop = scroller.scrollTop;
    const scrollHeight = scroller.scrollHeight;
    const clientHeight = scroller.clientHeight;

    if (scrollHeight <= 0) return;

    const bucketCount = this.database.settings.bucketCount;
    let startBucket = 0;
    let endBucket = bucketCount - 1;

    if (scrollHeight > clientHeight) {
      const startPct = scrollTop / scrollHeight;
      const endPct = (scrollTop + clientHeight) / scrollHeight;

      startBucket = Math.floor(startPct * bucketCount);
      endBucket = Math.min(bucketCount - 1, Math.floor(endPct * bucketCount));
    }

    const currentlyVisible = new Set();
    const newlyVisible = [];

    if (!this.lastVisibleBucketsMap.has(path)) {
      this.lastVisibleBucketsMap.set(path, new Set());
    }
    const previouslyVisible = this.lastVisibleBucketsMap.get(path);

    for (let i = startBucket; i <= endBucket; i++) {
      currentlyVisible.add(i);
      if (!previouslyVisible.has(i)) {
        newlyVisible.push(i);
      }
    }

    this.lastVisibleBucketsMap.set(path, currentlyVisible);

    const incrementMs = this.database.settings.refreshIntervalMs;
    this.database.recordReadingTime(
      path,
      startBucket,
      endBucket,
      incrementMs,
      newlyVisible,
    );

    renderer.draw();
  }
}

/* =========================================================================
   6. SETTINGS TAB INTERFACE (WITH TIMELINE TOOLS PANEL)
   ========================================================================= */

class HeatmapSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl("h2", { text: "Heatmap of Notes Settings" });

    new Setting(containerEl)
      .setName("Activity Idle Threshold (seconds)")
      .setDesc(
        "The reading viewport halts data accumulation after this period of user inactivity.",
      )
      .addSlider((slider) =>
        slider
          .setLimits(10, 300, 5)
          .setValue(this.plugin.database.settings.idleSeconds)
          .setDynamicTooltip()
          .onChange(async (val) => {
            this.plugin.database.settings.idleSeconds = val;
            this.plugin.activityMonitor.setIdleThreshold(val);
            await this.plugin.database.save(true);
          }),
      );

    new Setting(containerEl)
      .setName("Heatmap Resolution (buckets)")
      .setDesc("The density of segmented vertical bands.")
      .addSlider((slider) =>
        slider
          .setLimits(20, 200, 10)
          .setValue(this.plugin.database.settings.bucketCount)
          .setDynamicTooltip()
          .onChange(async (val) => {
            this.plugin.database.settings.bucketCount = val;
            await this.plugin.database.save(true);
            this.plugin.engine.clearAllRenderers();
            this.plugin.engine.syncOpenViews();
          }),
      );

    new Setting(containerEl)
      .setName("Visual Bar Width (pixels)")
      .setDesc("The screen width of the vertical colored track.")
      .addSlider((slider) =>
        slider
          .setLimits(8, 48, 2)
          .setValue(this.plugin.database.settings.heatmapWidth)
          .setDynamicTooltip()
          .onChange(async (val) => {
            this.plugin.database.settings.heatmapWidth = val;
            await this.plugin.database.save(true);
            this.refreshUIPositioning();
          }),
      );

    new Setting(containerEl)
      .setName("Sidebar Edge Offset (pixels)")
      .setDesc(
        "Position spacing from the right pane borders to fit clean native layouts.",
      )
      .addSlider((slider) =>
        slider
          .setLimits(0, 50, 2)
          .setValue(this.plugin.database.settings.heatmapOffsetRight)
          .setDynamicTooltip()
          .onChange(async (val) => {
            this.plugin.database.settings.heatmapOffsetRight = val;
            await this.plugin.database.save(true);
            this.refreshUIPositioning();
          }),
      );

    new Setting(containerEl)
      .setName("Track Transparency")
      .setDesc("Alpha transparent blend values.")
      .addSlider((slider) =>
        slider
          .setLimits(0.1, 1.0, 0.05)
          .setValue(this.plugin.database.settings.heatmapOpacity)
          .setDynamicTooltip()
          .onChange(async (val) => {
            this.plugin.database.settings.heatmapOpacity = val;
            await this.plugin.database.save(true);
            this.refreshUIPositioning();
          }),
      );

    new Setting(containerEl)
      .setName("Debug Mode")
      .setDesc("Toggle verbose tracing inside consoles.")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.database.settings.debugMode)
          .onChange(async (val) => {
            this.plugin.database.settings.debugMode = val;
            logger.setDebug(val);
            await this.plugin.database.save(true);
          }),
      );

    containerEl.createEl("p", {
      cls: "frh-setting-hint",
      text: "Tip: Hover your pointer directly over the vertical heatmap strip to review total engagement, historical visit counts, and dynamic read lengths for each portion of your notes.",
    });

    /* =========================================================================
       TIMELINE TOOLS PANEL
       ========================================================================= */
    containerEl.createEl("h3", { text: "Timeline Tools" });
    const toolsContainer = containerEl.createDiv({
      cls: "frh-tools-container",
    });

    // 1. DASHBOARD SUBSECTION
    toolsContainer.createEl("h4", {
      text: "Analytics Dashboard",
      cls: "frh-subsection-title",
    });
    const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
    const activeFile = activeView ? activeView.file : null;
    const db = this.plugin.database;

    if (activeFile) {
      const rec = db.getOrCreateRecord(activeFile.path);
      const totalSec = Math.round(rec.totalTimeMs / 1000);
      const minStr = Math.floor(totalSec / 60);
      const secStr = String(totalSec % 60).padStart(2, "0");

      const dashDiv = toolsContainer.createDiv({ cls: "frh-dashboard-panel" });

      const createStat = (label, val) => {
        const row = dashDiv.createDiv({ cls: "frh-dashboard-stat" });
        row.createSpan({ text: label, cls: "frh-stat-label" });
        row.createSpan({ text: val, cls: "frh-stat-value" });
      };

      createStat("Active Note Name", activeFile.name);
      createStat("Total Time Spent", `${minStr}m ${secStr}s`);
      createStat("Total Section Visits", `${rec.visits || 0}`);
      createStat(
        "Last Accessed",
        rec.lastAccessed
          ? new Date(rec.lastAccessed).toLocaleString()
          : "Unknown",
      );
      createStat(
        "Indexed Notes Count",
        `${Object.keys(db.records).length} files`,
      );
    } else {
      toolsContainer.createEl("p", {
        cls: "frh-setting-hint",
        text: "Please open a markdown file in the editor to view active note analytics.",
      });
    }

    // 2. RESET SUBSECTION
    toolsContainer.createEl("h4", {
      text: "Reset Operations",
      cls: "frh-subsection-title",
    });

    new Setting(toolsContainer)
      .setName("Reset Current Note Analytics")
      .setDesc(
        "Permanently discard collected reading metrics for the active note.",
      )
      .addButton((button) =>
        button
          .setButtonText("Reset Current Note")
          .setWarning()
          .onClick(async () => {
            if (activeFile) {
              db.clearRecord(activeFile.path);
              new Notice(`Cleared reading analytics for: ${activeFile.name}`);
              this.plugin.engine.clearAllRenderers();
              this.plugin.engine.syncOpenViews();
              this.display();
            } else {
              new Notice("No active note found to reset.");
            }
          }),
      );

    new Setting(toolsContainer)
      .setName("Reset All Heatmaps")
      .setDesc(
        "Delete all historical engagement records across the entire vault database.",
      )
      .addButton((button) =>
        button
          .setButtonText("Reset Database")
          .setWarning()
          .onClick(async () => {
            if (
              confirm(
                "Are you sure you want to permanently delete all reading engagement history? This action cannot be undone.",
              )
            ) {
              db.records = {};
              await db.save(true);
              new Notice("All vault reading metrics have been cleared.");
              this.plugin.engine.clearAllRenderers();
              this.plugin.engine.syncOpenViews();
              this.display();
            }
          }),
      );

    // 3. ERROR & DIAGNOSTICS SUBSECTION
    const diagSection = toolsContainer.createDiv({
      cls: "frh-diagnostic-section",
    });
    diagSection.createEl("h4", { text: "Diagnostics & System Health" });

    const isUserActive = this.plugin.activityMonitor.isUserActive();
    const recordsCount = Object.keys(db.records).length;

    new Setting(diagSection)
      .setName("Tracking Status")
      .setDesc(
        "Verifies if the activity monitor is actively tracking runtime engagement.",
      )
      .addText((text) =>
        text
          .setValue(
            isUserActive ? "Active & Monitoring" : "Suspended (Idle/Inactive)",
          )
          .setDisabled(true),
      );

    new Setting(diagSection)
      .setName("Storage Database State")
      .setDesc("Indexed registry nodes and system health check.")
      .addText((text) =>
        text
          .setValue(`Healthy (${recordsCount} tracked files)`)
          .setDisabled(true),
      );
  }

  refreshUIPositioning() {
    const settings = this.plugin.database.settings;
    this.plugin.engine.renderers.forEach((renderer) => {
      if (renderer.container) {
        renderer.container.style.width = `${settings.heatmapWidth}px`;
        renderer.container.style.right = `${settings.heatmapOffsetRight}px`;
        renderer.container.style.opacity = `${settings.heatmapOpacity}`;
        renderer.resizeCanvas();
      }
    });
  }
}

/* =========================================================================
   7. MAIN PLUG-IN BOOTSTRAPPER (LIFECYCLE ENTRY POINT)
   ========================================================================= */

class HeatmapPlugin extends Plugin {
  async onload() {
    logger.info("Initializing Heatmap of Notes plugin...");

    this.database = new HeatmapDatabase(this);
    await this.database.load();

    this.activityMonitor = new ActivityMonitor(
      this.database.settings.idleSeconds,
    );
    this.activityMonitor.start();

    this.engine = new HeatmapEngine(this, this.database, this.activityMonitor);

    this.registerEvent(
      this.app.workspace.on("layout-change", () => {
        this.engine.syncOpenViews();
      }),
    );

    this.registerEvent(
      this.app.workspace.on("active-leaf-change", () => {
        this.engine.syncOpenViews();
      }),
    );

    this.registerEvent(
      this.app.vault.on("rename", (file, oldPath) => {
        this.database.handleRename(oldPath, file.path);
      }),
    );

    if (this.app.workspace.layoutReady) {
      this.engine.start();
      this.engine.syncOpenViews();
    } else {
      this.app.workspace.onLayoutReady(() => {
        this.engine.start();
        this.engine.syncOpenViews();
      });
    }

    this.addSettingTab(new HeatmapSettingTab(this.app, this));

    this.addCommand({
      id: "clear-heatmap-data",
      name: "Clear Heatmap Analytics for Current Note",
      callback: () => {
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (activeView && activeView.file) {
          this.database.clearRecord(activeView.file.path);
          new Notice(`Cleared reading analytics for ${activeView.file.name}`);
          this.engine.clearAllRenderers();
          this.engine.syncOpenViews();
        } else {
          new Notice("No active note found to clear.");
        }
      },
    });

    logger.info("Load lifecycle completed successfully.");
  }

  async onunload() {
    logger.info("Unloading Heatmap of Notes plugin...");

    if (this.engine) {
      this.engine.stop();
    }
    if (this.activityMonitor) {
      this.activityMonitor.destroy();
    }
    if (this.database) {
      await this.database.save(true);
    }

    const tooltip = document.getElementById("frh-tooltip-element");
    if (tooltip) {
      tooltip.remove();
    }

    logger.info("Cleanup successfully completed.");
  }
}

module.exports = HeatmapPlugin;
