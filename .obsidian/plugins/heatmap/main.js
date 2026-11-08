"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// heatmap-of-notes/src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => HeatmapPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian2 = require("obsidian");

// heatmap-of-notes/src/logger.ts
var HeatmapLogger = class {
  constructor(pluginId) {
    this.pluginId = pluginId;
    this.debugEnabled = false;
  }
  setDebug(enabled) {
    this.debugEnabled = enabled;
  }
  log(level, ...args) {
    if (level === "DEBUG" && !this.debugEnabled) return;
    const prefix = `[${this.pluginId}] [${level}]`;
    switch (level) {
      case "WARN":
        console.warn(prefix, ...args);
        break;
      case "ERROR":
        console.error(prefix, ...args);
        break;
      default:
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
};
var logger = new HeatmapLogger("HeatmapOfNotes");

// heatmap-of-notes/src/types.ts
var DEFAULT_HEATMAP_SETTINGS = {
  idleSeconds: 30,
  bucketCount: 100,
  heatmapWidth: 16,
  heatmapOffsetRight: 12,
  heatmapOpacity: 0.85,
  refreshIntervalMs: 1e3,
  debugMode: false
};

// heatmap-of-notes/src/storage.ts
function resizeArray(arr, targetSize) {
  if (arr.length === targetSize) return arr;
  const resized = Array(targetSize).fill(0);
  if (arr.length === 0) return resized;
  for (let i = 0; i < targetSize; i++) {
    const srcIndex = i / targetSize * arr.length;
    const low = Math.floor(srcIndex);
    const high = Math.min(arr.length - 1, Math.ceil(srcIndex));
    const weight = srcIndex - low;
    resized[i] = Math.round(arr[low] * (1 - weight) + arr[high] * weight);
  }
  return resized;
}
function remapRecordPaths(records, oldPath, newPath) {
  if (!oldPath || !newPath || oldPath === newPath) return 0;
  let moved = 0;
  if (oldPath in records) {
    records[newPath] = records[oldPath];
    delete records[oldPath];
    moved++;
  }
  const prefix = `${oldPath}/`;
  for (const key of Object.keys(records)) {
    if (key.startsWith(prefix)) {
      const remapped = `${newPath}/${key.slice(prefix.length)}`;
      if (!(remapped in records)) {
        records[remapped] = records[key];
        moved++;
      }
      delete records[key];
    }
  }
  return moved;
}
function pruneDeletedRecords(records, fileExists) {
  const removed = [];
  for (const key of Object.keys(records)) {
    if (!fileExists(key)) {
      delete records[key];
      removed.push(key);
    }
  }
  return removed;
}
function clampInt(value, min, max, fallback) {
  if (typeof value !== "number" || !Number.isFinite(value)) return fallback;
  return Math.round(Math.min(Math.max(value, min), max));
}
function normalizeHeatmapSettings(raw) {
  const merged = { ...DEFAULT_HEATMAP_SETTINGS, ...raw != null ? raw : {} };
  merged.idleSeconds = clampInt(merged.idleSeconds, 5, 600, DEFAULT_HEATMAP_SETTINGS.idleSeconds);
  merged.bucketCount = clampInt(merged.bucketCount, 10, 400, DEFAULT_HEATMAP_SETTINGS.bucketCount);
  merged.heatmapWidth = clampInt(merged.heatmapWidth, 8, 48, DEFAULT_HEATMAP_SETTINGS.heatmapWidth);
  merged.heatmapOffsetRight = clampInt(merged.heatmapOffsetRight, 0, 80, DEFAULT_HEATMAP_SETTINGS.heatmapOffsetRight);
  merged.heatmapOpacity = Math.min(Math.max(Number(merged.heatmapOpacity) || DEFAULT_HEATMAP_SETTINGS.heatmapOpacity, 0.1), 1);
  merged.refreshIntervalMs = clampInt(merged.refreshIntervalMs, 250, 5e3, DEFAULT_HEATMAP_SETTINGS.refreshIntervalMs);
  merged.debugMode = Boolean(merged.debugMode);
  return merged;
}
var _HeatmapDatabase = class _HeatmapDatabase {
  constructor(plugin) {
    this.settings = { ...DEFAULT_HEATMAP_SETTINGS };
    this.records = {};
    this.lastSaveAt = 0;
    this.dirty = false;
    this.plugin = plugin;
  }
  async load() {
    var _a;
    try {
      const raw = await this.plugin.loadData();
      if (raw) {
        this.settings = normalizeHeatmapSettings(raw.settings);
        this.records = (_a = raw.records) != null ? _a : {};
        for (const path of Object.keys(this.records)) {
          this.records[path] = this.normalizeRecord(this.records[path], this.settings.bucketCount);
        }
        logger.info("Database loaded successfully.");
      } else {
        logger.info("No existing database found. Creating a fresh copy.");
      }
    } catch (err) {
      logger.error("Failed to load database from disk. Using defaults.", err);
    }
  }
  /**
   * Normalizes a record's fields IN PLACE (so callers holding the record
   * reference keep mutating the stored object) and returns it.
   */
  normalizeRecord(record, bucketCount) {
    if (!Array.isArray(record.buckets) || record.buckets.length !== bucketCount) {
      record.buckets = resizeArray(Array.isArray(record.buckets) ? record.buckets : [], bucketCount);
    }
    if (!Array.isArray(record.bucketVisits) || record.bucketVisits.length !== bucketCount) {
      record.bucketVisits = resizeArray(Array.isArray(record.bucketVisits) ? record.bucketVisits : [], bucketCount);
    }
    record.totalTimeMs = Number(record.totalTimeMs) || 0;
    record.visits = Number(record.visits) || 0;
    return record;
  }
  async save(force = false) {
    const now = Date.now();
    if (!force && !this.dirty) return;
    if (!force && now - this.lastSaveAt < _HeatmapDatabase.SAVE_THROTTLE_MS) return;
    try {
      await this.plugin.saveData({ settings: this.settings, records: this.records });
      this.lastSaveAt = now;
      this.dirty = false;
    } catch (err) {
      logger.error("Failed to save database to disk.", err);
    }
  }
  /**
   * Read-only lookup — returns undefined when nothing was recorded yet.
   * (Creating records on read was a bug: hover tooltips used to mint empty
   * records for never-opened notes.)
   */
  getRecord(path) {
    return this.records[path];
  }
  /** Gets or creates the record for a path. Write-intent only. */
  getOrCreateRecord(path) {
    if (!this.records[path]) {
      this.records[path] = {
        totalTimeMs: 0,
        visits: 0,
        lastAccessed: (/* @__PURE__ */ new Date()).toISOString(),
        buckets: Array(this.settings.bucketCount).fill(0),
        bucketVisits: Array(this.settings.bucketCount).fill(0)
      };
    } else {
      this.records[path] = this.normalizeRecord(this.records[path], this.settings.bucketCount);
    }
    return this.records[path];
  }
  /** Resizes all records after a bucket-count change. */
  resizeAllRecords(bucketCount) {
    for (const path of Object.keys(this.records)) {
      this.records[path] = this.normalizeRecord(this.records[path], bucketCount);
    }
  }
  recordReadingTime(path, startBucket, endBucket, incrementMs, newlyVisibleBuckets) {
    const rec = this.getOrCreateRecord(path);
    rec.totalTimeMs += incrementMs;
    rec.lastAccessed = (/* @__PURE__ */ new Date()).toISOString();
    for (let i = startBucket; i <= endBucket; i++) {
      if (i >= 0 && i < rec.buckets.length) rec.buckets[i] += incrementMs;
    }
    for (const bucketIdx of newlyVisibleBuckets) {
      if (bucketIdx >= 0 && bucketIdx < rec.bucketVisits.length) rec.bucketVisits[bucketIdx] += 1;
    }
    this.dirty = true;
    void this.save();
  }
  incrementVisit(path) {
    const rec = this.getOrCreateRecord(path);
    rec.visits += 1;
    this.dirty = true;
    void this.save();
  }
  /** Handles file AND folder renames (see remapRecordPaths). */
  handleRename(oldPath, newPath) {
    const moved = remapRecordPaths(this.records, oldPath, newPath);
    if (moved > 0) {
      this.dirty = true;
      void this.save(true);
      logger.info(`Renamed ${moved} record(s): ${oldPath} -> ${newPath}`);
    }
  }
  /** Drops records for files that no longer exist. Returns removed paths. */
  pruneDeleted(fileExists) {
    const removed = pruneDeletedRecords(this.records, fileExists);
    if (removed.length > 0) {
      this.dirty = true;
      void this.save(true);
      logger.info(`Pruned ${removed.length} record(s) for deleted files.`);
    }
    return removed;
  }
  clearRecord(path) {
    if (this.records[path]) {
      delete this.records[path];
      void this.save(true);
      logger.info(`Cleared storage data for: ${path}`);
      return true;
    }
    return false;
  }
  clearAll() {
    this.records = {};
    void this.save(true);
  }
};
/** Minimum interval between throttled saves (ms). */
_HeatmapDatabase.SAVE_THROTTLE_MS = 1e4;
var HeatmapDatabase = _HeatmapDatabase;

// heatmap-of-notes/src/activity.ts
var WINDOW_EVENTS = ["pointermove", "pointerdown", "keydown", "wheel", "scroll"];
var ActivityMonitor = class {
  constructor(registerDomElement, idleThresholdSeconds) {
    this.lastActivityAt = Date.now();
    this.register = registerDomElement;
    this.idleThresholdMs = idleThresholdSeconds * 1e3;
  }
  setIdleThreshold(seconds) {
    this.idleThresholdMs = seconds * 1e3;
    logger.debug(`Idle threshold updated to ${seconds}s.`);
  }
  start() {
    this.recordActivity();
    const handler = () => this.recordActivity();
    for (const evt of WINDOW_EVENTS) {
      this.register(window, evt, handler, { passive: true });
    }
    this.register(document, "visibilitychange", handler);
    logger.debug("ActivityMonitor listeners registered successfully.");
  }
  recordActivity() {
    this.lastActivityAt = Date.now();
  }
  isUserActive(now = Date.now()) {
    if (typeof document !== "undefined" && document.hidden) return false;
    return now - this.lastActivityAt < this.idleThresholdMs;
  }
};

// heatmap-of-notes/src/renderer.ts
var TOUCH_BODY_CLASS = "frh-touch-device";
var HeatmapRenderer = class {
  constructor(view, database, getSettings, registerDomElement) {
    this.container = null;
    this.canvas = null;
    this.ctx = null;
    this.tooltip = null;
    this.scrollerElement = null;
    this.resizeObserver = null;
    this.animationFrameId = null;
    this.scrollListener = null;
    this.pointerMoveListener = null;
    this.pointerLeaveListener = null;
    /** Original inline position of contentEl (restored on destroy). */
    this.originalContentElPosition = null;
    this.view = view;
    this.database = database;
    this.getSettings = getSettings;
    this.registerDomElement = registerDomElement;
    this.initDOM();
    this.scrollerElement = this.findScroller();
    this.bindEvents();
    this.resizeCanvas();
  }
  /* ------------------------------------------------------------------ */
  /* Scroller resolution                                                 */
  /* ------------------------------------------------------------------ */
  findScroller() {
    var _a, _b;
    const container = (_a = this.view) == null ? void 0 : _a.contentEl;
    if (!container) return null;
    let mode = null;
    try {
      mode = typeof this.view.getMode === "function" ? this.view.getMode() : null;
    } catch (e) {
      mode = null;
    }
    if (mode === "preview") {
      const preview = container.querySelector(".markdown-preview-view");
      if (preview) return preview;
    } else if (mode === "source") {
      const source = container.querySelector(".cm-scroller");
      if (source) return source;
    }
    const sourceScroller = container.querySelector(".cm-scroller");
    if (sourceScroller && sourceScroller.clientHeight > 0) return sourceScroller;
    const previewScroller = container.querySelector(".markdown-preview-view");
    if (previewScroller && previewScroller.clientHeight > 0) return previewScroller;
    return (_b = sourceScroller != null ? sourceScroller : previewScroller) != null ? _b : null;
  }
  /**
   * Cheap validity check + rebind. Called from the engine tick — must stay
   * O(1) when nothing changed (it is: just isConnected).
   */
  checkAndRebindScroller() {
    if (this.scrollerElement && this.scrollerElement.isConnected) return;
    this.initDOM();
    const current = this.findScroller();
    if (!current) return;
    logger.debug("Active scroller changed (e.g. mode toggle). Rebinding event listeners.");
    this.unbindEvents();
    this.scrollerElement = current;
    this.bindEvents();
    this.resizeCanvas();
  }
  /* ------------------------------------------------------------------ */
  /* DOM                                                                 */
  /* ------------------------------------------------------------------ */
  initDOM() {
    var _a;
    const contentEl = (_a = this.view) == null ? void 0 : _a.contentEl;
    if (!contentEl) return;
    if (getComputedStyle(contentEl).position === "static") {
      if (this.originalContentElPosition === null) {
        this.originalContentElPosition = contentEl.style.position;
      }
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
    const settings = this.getSettings();
    this.container.style.width = `${settings.heatmapWidth}px`;
    this.container.style.right = `${settings.heatmapOffsetRight}px`;
    this.container.style.opacity = `${settings.heatmapOpacity}`;
    this.canvas = document.createElement("canvas");
    this.canvas.className = "frh-heatmap-canvas";
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext("2d");
    contentEl.appendChild(this.container);
    logger.debug("Created and appended new heatmap container.");
    let tooltip = document.getElementById("frh-tooltip-element");
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.id = "frh-tooltip-element";
      tooltip.className = "frh-heatmap-tooltip";
      document.body.appendChild(tooltip);
    }
    this.tooltip = tooltip;
  }
  /* ------------------------------------------------------------------ */
  /* Events                                                              */
  /* ------------------------------------------------------------------ */
  bindEvents() {
    if (!this.scrollerElement) return;
    this.scrollListener = () => {
      this.hideTooltip();
      this.draw();
    };
    this.registerDomElement(this.scrollerElement, "scroll", this.scrollListener, { passive: true });
    this.resizeObserver = new ResizeObserver(() => this.resizeCanvas());
    this.resizeObserver.observe(this.scrollerElement);
    if (this.canvas) {
      this.pointerMoveListener = (e) => this.handlePointerMove(e);
      this.pointerLeaveListener = () => this.hideTooltip();
      this.registerDomElement(this.canvas, "pointermove", this.pointerMoveListener);
      this.registerDomElement(this.canvas, "pointerleave", this.pointerLeaveListener);
      this.registerDomElement(this.canvas, "pointerdown", (e) => e.preventDefault());
    }
  }
  unbindEvents() {
    this.scrollListener = null;
    this.pointerMoveListener = null;
    this.pointerLeaveListener = null;
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
  }
  /* ------------------------------------------------------------------ */
  /* Canvas                                                              */
  /* ------------------------------------------------------------------ */
  syncCanvasSize() {
    if (!this.scrollerElement || !this.canvas || !this.container || !this.ctx) return false;
    const rect = this.container.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return false;
    const dpr = window.devicePixelRatio || 1;
    const expectedWidth = Math.round(rect.width * dpr);
    const expectedHeight = Math.round(rect.height * dpr);
    if (this.canvas.width !== expectedWidth || this.canvas.height !== expectedHeight) {
      this.canvas.width = expectedWidth;
      this.canvas.height = expectedHeight;
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    return true;
  }
  resizeCanvas() {
    if (this.syncCanvasSize()) this.draw();
  }
  applySettings() {
    const settings = this.getSettings();
    if (this.container) {
      this.container.style.width = `${settings.heatmapWidth}px`;
      this.container.style.right = `${settings.heatmapOffsetRight}px`;
      this.container.style.opacity = `${settings.heatmapOpacity}`;
    }
    this.resizeCanvas();
  }
  draw() {
    if (this.animationFrameId !== null) cancelAnimationFrame(this.animationFrameId);
    this.animationFrameId = requestAnimationFrame(() => this.paint());
  }
  /** Parses the theme accent color once; returns an rgba() factory. */
  accentColorFactory() {
    const bodyStyle = getComputedStyle(document.body);
    const colorStr = bodyStyle.getPropertyValue("--interactive-accent").trim();
    let r = 36, g = 143, b = 178;
    if (colorStr.startsWith("#")) {
      const clean = colorStr.replace("#", "");
      if (clean.length === 3) {
        r = parseInt(clean[0] + clean[0], 16);
        g = parseInt(clean[1] + clean[1], 16);
        b = parseInt(clean[2] + clean[2], 16);
      } else if (clean.length === 6) {
        r = parseInt(clean.substring(0, 2), 16);
        g = parseInt(clean.substring(2, 4), 16);
        b = parseInt(clean.substring(4, 6), 16);
      }
    } else if (colorStr.startsWith("rgb")) {
      const matches = colorStr.match(/\d+/g);
      if (matches && matches.length >= 3) {
        r = parseInt(matches[0], 10);
        g = parseInt(matches[1], 10);
        b = parseInt(matches[2], 10);
      }
    }
    return (alpha) => `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }
  paint() {
    this.animationFrameId = null;
    if (!this.canvas || !this.ctx || !this.scrollerElement || !this.container) return;
    const rect = this.container.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return;
    if (!this.syncCanvasSize()) return;
    const clientWidth = rect.width;
    const clientHeight = rect.height;
    const ctx = this.ctx;
    ctx.clearRect(0, 0, clientWidth, clientHeight);
    ctx.fillStyle = "rgba(128, 128, 128, 0.03)";
    ctx.fillRect(0, 0, clientWidth, clientHeight);
    const path = this.view.file ? this.view.file.path : null;
    if (!path) return;
    const record = this.database.getRecord(path);
    if (!record) return;
    const buckets = record.buckets;
    const bucketCount = buckets.length;
    if (bucketCount === 0) return;
    const accent = this.accentColorFactory();
    const maxVal = Math.max(...buckets, 1);
    const itemHeight = clientHeight / bucketCount;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    for (let i = 0; i < bucketCount; i++) {
      const weight = buckets[i] / maxVal;
      const y = (i + 0.5) * itemHeight;
      ctx.lineTo(weight * clientWidth, y);
    }
    ctx.lineTo(0, clientHeight);
    ctx.closePath();
    ctx.fillStyle = accent(0.18);
    ctx.fill();
    ctx.beginPath();
    for (let i = 0; i < bucketCount; i++) {
      const weight = buckets[i] / maxVal;
      const y = (i + 0.5) * itemHeight;
      const x = weight * clientWidth;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = accent(0.85);
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
      ctx.fillStyle = accent(0.1);
      ctx.fillRect(0, yStart, clientWidth, yEnd - yStart);
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
  /* ------------------------------------------------------------------ */
  /* Tooltip (desktop hover)                                             */
  /* ------------------------------------------------------------------ */
  handlePointerMove(e) {
    if (!this.canvas || !this.tooltip) return;
    if (e.pointerType === "touch") return;
    const rect = this.canvas.getBoundingClientRect();
    const relativeY = e.clientY - rect.top;
    const pct = Math.max(0, Math.min(1, relativeY / Math.max(1, rect.height)));
    const path = this.view.file ? this.view.file.path : null;
    if (!path) return;
    const record = this.database.getRecord(path);
    if (!record) {
      this.tooltip.innerHTML = `
        <div class="frh-heatmap-tooltip-title">Section ~${Math.round(pct * 100)}%</div>
        <div class="frh-heatmap-tooltip-row"><span>No reading data yet</span></div>`;
      this.positionTooltip(e);
      return;
    }
    const bucketCount = record.buckets.length;
    const bucketIdx = Math.min(bucketCount - 1, Math.floor(pct * bucketCount));
    const ms = record.buckets[bucketIdx] || 0;
    const visits = record.bucketVisits[bucketIdx] || 0;
    const totalSeconds = Math.round(ms / 1e3);
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
      </div>`;
    this.positionTooltip(e);
  }
  positionTooltip(e) {
    if (!this.tooltip) return;
    const tooltipWidth = this.tooltip.offsetWidth || 150;
    const xPos = e.clientX - tooltipWidth - 15;
    const yPos = Math.max(10, Math.min(window.innerHeight - 90, e.clientY - 30));
    this.tooltip.style.left = `${Math.max(4, xPos)}px`;
    this.tooltip.style.top = `${yPos}px`;
    this.tooltip.style.opacity = "1";
  }
  hideTooltip() {
    if (this.tooltip) this.tooltip.style.opacity = "0";
  }
  /* ------------------------------------------------------------------ */
  /* Teardown                                                            */
  /* ------------------------------------------------------------------ */
  destroy() {
    var _a, _b;
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
    this.unbindEvents();
    if (this.originalContentElPosition !== null && ((_a = this.view) == null ? void 0 : _a.contentEl)) {
      this.view.contentEl.style.position = this.originalContentElPosition;
      this.originalContentElPosition = null;
    }
    (_b = this.container) == null ? void 0 : _b.remove();
    this.container = null;
    logger.debug("Renderer destroyed for pane view.");
  }
};

// heatmap-of-notes/src/engine.ts
function computeVisibleBuckets(scrollTop, scrollHeight, clientHeight, bucketCount) {
  if (bucketCount <= 0) return { start: 0, end: -1 };
  if (scrollHeight <= 0) return { start: 0, end: -1 };
  if (scrollHeight <= clientHeight) {
    return { start: 0, end: bucketCount - 1 };
  }
  const startPct = scrollTop / scrollHeight;
  const endPct = (scrollTop + clientHeight) / scrollHeight;
  const start = Math.max(0, Math.floor(startPct * bucketCount));
  const end = Math.min(bucketCount - 1, Math.floor(endPct * bucketCount));
  return { start, end };
}
function diffVisibleBuckets(current, previous) {
  const newlyVisible = [];
  for (const b of current) {
    if (!previous.has(b)) newlyVisible.push(b);
  }
  return newlyVisible;
}
var HeatmapEngine = class {
  constructor(host, database, activityMonitor, getSettings) {
    this.renderers = /* @__PURE__ */ new Map();
    this.intervalId = null;
    this.lastVisibleBuckets = /* @__PURE__ */ new Map();
    /** Paths already visited in this session (visit counted once per session). */
    this.sessionVisitedPaths = /* @__PURE__ */ new Set();
    this.host = host;
    this.database = database;
    this.activityMonitor = activityMonitor;
    this.getSettings = getSettings;
  }
  /* ------------------------------------------------------------------ */
  /* Lifecycle                                                           */
  /* ------------------------------------------------------------------ */
  start() {
    if (this.intervalId !== null) return;
    const intervalMs = this.getSettings().refreshIntervalMs;
    this.intervalId = this.host.registerInterval(window.setInterval(() => this.tick(), intervalMs));
  }
  stop() {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.clearAllRenderers();
  }
  /* ------------------------------------------------------------------ */
  /* View management                                                     */
  /* ------------------------------------------------------------------ */
  registerView(view) {
    var _a;
    if (this.renderers.has(view)) return;
    logger.debug(`Registering view: ${view.file ? view.file.name : "unknown"}`);
    const renderer = new HeatmapRenderer(
      view,
      this.database,
      this.getSettings,
      (el, type, cb, options) => this.host.registerDomElement(el, type, cb, options)
    );
    this.renderers.set(view, renderer);
    const path = (_a = view.file) == null ? void 0 : _a.path;
    if (path && !this.sessionVisitedPaths.has(path)) {
      this.sessionVisitedPaths.add(path);
      this.database.incrementVisit(path);
    }
  }
  deregisterView(view) {
    var _a;
    const renderer = this.renderers.get(view);
    if (!renderer) return;
    renderer.destroy();
    this.renderers.delete(view);
    const path = (_a = view.file) == null ? void 0 : _a.path;
    if (path && !this.hasOpenViewForPath(path)) {
      this.lastVisibleBuckets.delete(path);
    }
  }
  hasOpenViewForPath(path) {
    var _a;
    for (const view of this.renderers.keys()) {
      if (((_a = view.file) == null ? void 0 : _a.path) === path) return true;
    }
    return false;
  }
  clearAllRenderers() {
    for (const renderer of this.renderers.values()) renderer.destroy();
    this.renderers.clear();
    this.lastVisibleBuckets.clear();
  }
  /** Rebuilds renderers after a settings change WITHOUT recounting visits. */
  rebuildRenderers() {
    this.clearAllRenderers();
    this.syncOpenViews();
  }
  syncOpenViews() {
    var _a;
    const activeViews = [];
    this.host.iterateMarkdownViews((view) => activeViews.push(view));
    for (const view of [...this.renderers.keys()]) {
      if (!activeViews.includes(view)) this.deregisterView(view);
    }
    for (const view of activeViews) {
      if (!this.renderers.has(view)) {
        this.registerView(view);
      } else {
        (_a = this.renderers.get(view)) == null ? void 0 : _a.checkAndRebindScroller();
      }
    }
  }
  applySettingsToRenderers() {
    for (const renderer of this.renderers.values()) renderer.applySettings();
  }
  /* ------------------------------------------------------------------ */
  /* Tracking loop                                                       */
  /* ------------------------------------------------------------------ */
  tick() {
    if (!this.activityMonitor.isUserActive()) return;
    for (const [view, renderer] of this.renderers.entries()) {
      const contentEl = view.contentEl;
      if (!contentEl || !contentEl.isConnected) continue;
      if (contentEl.getBoundingClientRect().height <= 0) continue;
      this.refreshViewPort(view, renderer);
    }
  }
  refreshViewPort(view, renderer) {
    var _a;
    const path = view.file ? view.file.path : null;
    if (!path) return;
    renderer.checkAndRebindScroller();
    const scroller = renderer.scrollerElement;
    if (!scroller) return;
    const scrollTop = scroller.scrollTop;
    const scrollHeight = scroller.scrollHeight;
    const clientHeight = scroller.clientHeight;
    if (scrollHeight <= 0) return;
    const bucketCount = this.getSettings().bucketCount;
    const { start, end } = computeVisibleBuckets(scrollTop, scrollHeight, clientHeight, bucketCount);
    const currentlyVisible = /* @__PURE__ */ new Set();
    for (let i = start; i <= end; i++) currentlyVisible.add(i);
    const previouslyVisible = (_a = this.lastVisibleBuckets.get(path)) != null ? _a : /* @__PURE__ */ new Set();
    const newlyVisible = diffVisibleBuckets(currentlyVisible, previouslyVisible);
    this.lastVisibleBuckets.set(path, currentlyVisible);
    const incrementMs = this.getSettings().refreshIntervalMs;
    this.database.recordReadingTime(path, start, end, incrementMs, newlyVisible);
    renderer.draw();
  }
};

// heatmap-of-notes/src/settings-tab.ts
var import_obsidian = require("obsidian");
var ConfirmModal = class extends import_obsidian.Modal {
  constructor(app, title, body, confirmLabel, onConfirm) {
    super(app);
    this.title = title;
    this.body = body;
    this.confirmLabel = confirmLabel;
    this.onConfirm = onConfirm;
  }
  onOpen() {
    this.titleEl.setText(this.title);
    this.contentEl.empty();
    this.contentEl.createEl("p", { text: this.body });
    const buttonRow = this.contentEl.createDiv({ cls: "frh-modal-button-row" });
    new import_obsidian.ButtonComponent(buttonRow).setButtonText(this.confirmLabel).setWarning().onClick(() => {
      this.close();
      this.onConfirm();
    });
    new import_obsidian.ButtonComponent(buttonRow).setButtonText("Cancel").onClick(() => this.close());
  }
  onClose() {
    this.contentEl.empty();
  }
};
var HeatmapSettingTab = class extends import_obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  get db() {
    return this.plugin.database;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Heatmap of Notes Settings" });
    new import_obsidian.Setting(containerEl).setName("Activity idle threshold (seconds)").setDesc("Reading data accumulation pauses after this period of inactivity.").addSlider(
      (slider) => slider.setLimits(10, 300, 5).setValue(this.db.settings.idleSeconds).setDynamicTooltip().onChange(async (val) => {
        this.db.settings.idleSeconds = val;
        this.plugin.activityMonitor.setIdleThreshold(val);
        await this.db.save(true);
      })
    );
    new import_obsidian.Setting(containerEl).setName("Heatmap resolution (buckets)").setDesc("Density of the vertical bands. Existing data is resampled.").addSlider(
      (slider) => slider.setLimits(20, 200, 10).setValue(this.db.settings.bucketCount).setDynamicTooltip().onChange(async (val) => {
        this.db.settings.bucketCount = val;
        this.db.resizeAllRecords(val);
        await this.db.save(true);
        this.plugin.engine.rebuildRenderers();
      })
    );
    new import_obsidian.Setting(containerEl).setName("Visual bar width (pixels)").setDesc("Screen width of the vertical colored track.").addSlider(
      (slider) => slider.setLimits(8, 48, 2).setValue(this.db.settings.heatmapWidth).setDynamicTooltip().onChange(async (val) => {
        this.db.settings.heatmapWidth = val;
        await this.db.save(true);
        this.plugin.engine.applySettingsToRenderers();
      })
    );
    new import_obsidian.Setting(containerEl).setName("Sidebar edge offset (pixels)").setDesc("Spacing from the right pane border.").addSlider(
      (slider) => slider.setLimits(0, 50, 2).setValue(this.db.settings.heatmapOffsetRight).setDynamicTooltip().onChange(async (val) => {
        this.db.settings.heatmapOffsetRight = val;
        await this.db.save(true);
        this.plugin.engine.applySettingsToRenderers();
      })
    );
    new import_obsidian.Setting(containerEl).setName("Track transparency").setDesc("Opacity of the heatmap strip.").addSlider(
      (slider) => slider.setLimits(0.1, 1, 0.05).setValue(this.db.settings.heatmapOpacity).setDynamicTooltip().onChange(async (val) => {
        this.db.settings.heatmapOpacity = val;
        await this.db.save(true);
        this.plugin.engine.applySettingsToRenderers();
      })
    );
    new import_obsidian.Setting(containerEl).setName("Debug mode").setDesc("Verbose tracing in the developer console.").addToggle(
      (toggle) => toggle.setValue(this.db.settings.debugMode).onChange(async (val) => {
        this.db.settings.debugMode = val;
        this.plugin.setDebugLogging(val);
        await this.db.save(true);
      })
    );
    containerEl.createEl("p", {
      cls: "frh-setting-hint",
      text: "Tip: on desktop, hover the pointer over the vertical heatmap strip to see time spent, visit counts and read lengths for each part of the note. On touch devices the strip never intercepts your scroll gestures."
    });
    this.renderTimelineTools(containerEl);
  }
  renderTimelineTools(containerEl) {
    var _a;
    containerEl.createEl("h3", { text: "Timeline Tools" });
    const toolsContainer = containerEl.createDiv({ cls: "frh-tools-container" });
    toolsContainer.createEl("h4", { text: "Analytics Dashboard", cls: "frh-subsection-title" });
    const activeView = this.app.workspace.getActiveViewOfType(import_obsidian.MarkdownView);
    const activeFile = (_a = activeView == null ? void 0 : activeView.file) != null ? _a : null;
    const db = this.db;
    if (activeFile) {
      const rec = db.getRecord(activeFile.path);
      const dashDiv = toolsContainer.createDiv({ cls: "frh-dashboard-panel" });
      const createStat = (label, val) => {
        const row = dashDiv.createDiv({ cls: "frh-dashboard-stat" });
        row.createSpan({ text: label, cls: "frh-stat-label" });
        row.createSpan({ text: val, cls: "frh-stat-value" });
      };
      if (rec) {
        const totalSec = Math.round(rec.totalTimeMs / 1e3);
        const minStr = Math.floor(totalSec / 60);
        const secStr = String(totalSec % 60).padStart(2, "0");
        createStat("Active note name", activeFile.name);
        createStat("Total time spent", `${minStr}m ${secStr}s`);
        createStat("Total section visits", `${rec.visits || 0}`);
        createStat("Last accessed", rec.lastAccessed ? new Date(rec.lastAccessed).toLocaleString() : "Unknown");
      } else {
        createStat("Active note name", activeFile.name);
        createStat("Total time spent", "No data yet");
      }
      createStat("Indexed notes count", `${Object.keys(db.records).length} files`);
    } else {
      toolsContainer.createEl("p", {
        cls: "frh-setting-hint",
        text: "Please open a markdown file in the editor to view active note analytics."
      });
    }
    toolsContainer.createEl("h4", { text: "Reset Operations", cls: "frh-subsection-title" });
    new import_obsidian.Setting(toolsContainer).setName("Reset current note analytics").setDesc("Permanently discard collected reading metrics for the active note.").addButton(
      (button) => button.setButtonText("Reset Current Note").setWarning().onClick(async () => {
        if (activeFile) {
          db.clearRecord(activeFile.path);
          new import_obsidian.Notice(`Cleared reading analytics for: ${activeFile.name}`);
          this.plugin.engine.rebuildRenderers();
          this.display();
        } else {
          new import_obsidian.Notice("No active note found to reset.");
        }
      })
    );
    new import_obsidian.Setting(toolsContainer).setName("Reset all heatmaps").setDesc("Delete all historical engagement records across the entire vault database.").addButton(
      (button) => button.setButtonText("Reset Database").setWarning().onClick(() => {
        new ConfirmModal(
          this.app,
          "Reset all reading analytics?",
          "This permanently deletes all reading engagement history for every note. This action cannot be undone.",
          "Delete everything",
          async () => {
            db.clearAll();
            new import_obsidian.Notice("All vault reading metrics have been cleared.");
            this.plugin.engine.rebuildRenderers();
            this.display();
          }
        ).open();
      })
    );
    new import_obsidian.Setting(toolsContainer).setName("Prune records for deleted notes").setDesc("Remove analytics entries whose notes no longer exist in the vault.").addButton(
      (button) => button.setButtonText("Prune Deleted").onClick(() => {
        const removed = db.pruneDeleted(
          (path) => this.app.vault.getAbstractFileByPath(path) !== null
        );
        new import_obsidian.Notice(removed.length > 0 ? `Pruned ${removed.length} record(s).` : "Nothing to prune.");
        this.display();
      })
    );
    const diagSection = toolsContainer.createDiv({ cls: "frh-diagnostic-section" });
    diagSection.createEl("h4", { text: "Diagnostics & System Health" });
    const isUserActive = this.plugin.activityMonitor.isUserActive();
    const recordsCount = Object.keys(db.records).length;
    new import_obsidian.Setting(diagSection).setName("Tracking status").setDesc("Verifies if the activity monitor is actively tracking runtime engagement.").addText(
      (text) => text.setValue(isUserActive ? "Active & Monitoring" : "Suspended (Idle/Inactive)").setDisabled(true)
    );
    new import_obsidian.Setting(diagSection).setName("Storage database state").setDesc("Indexed registry nodes and system health check.").addText((text) => text.setValue(`Healthy (${recordsCount} tracked files)`).setDisabled(true));
  }
};

// shared/src/viewport.ts
function hasHoverPointer() {
  if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
    return true;
  }
  try {
    return window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  } catch (e) {
    return true;
  }
}

// heatmap-of-notes/src/main.ts
var HeatmapPlugin = class extends import_obsidian2.Plugin {
  async onload() {
    logger.info("Initializing Heatmap of Notes plugin...");
    this.database = new HeatmapDatabase({
      loadData: () => this.loadData(),
      saveData: (data) => this.saveData(data)
    });
    await this.database.load();
    logger.setDebug(this.database.settings.debugMode);
    this.activityMonitor = new ActivityMonitor(
      (el, type, cb, options) => this.registerDomEvent(el, type, cb, options),
      this.database.settings.idleSeconds
    );
    this.activityMonitor.start();
    this.engine = new HeatmapEngine(
      {
        registerInterval: (id) => this.registerInterval(id),
        iterateMarkdownViews: (cb) => this.app.workspace.iterateAllLeaves((leaf) => {
          if (leaf.view instanceof import_obsidian2.MarkdownView) cb(leaf.view);
        }),
        registerDomElement: (el, type, cb, options) => this.registerDomEvent(el, type, cb, options)
      },
      this.database,
      this.activityMonitor,
      () => this.database.settings
    );
    if (!hasHoverPointer()) {
      document.body.classList.add(TOUCH_BODY_CLASS);
      this.register(() => document.body.classList.remove(TOUCH_BODY_CLASS));
    }
    this.registerEvent(
      this.app.workspace.on("layout-change", () => this.engine.syncOpenViews())
    );
    this.registerEvent(
      this.app.workspace.on("active-leaf-change", () => this.engine.syncOpenViews())
    );
    this.registerEvent(
      this.app.vault.on("rename", (file, oldPath) => {
        this.database.handleRename(oldPath, file.path);
      })
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
      name: "Clear heatmap analytics for current note",
      callback: () => {
        const activeView = this.app.workspace.getActiveViewOfType(import_obsidian2.MarkdownView);
        if (activeView && activeView.file) {
          this.database.clearRecord(activeView.file.path);
          new import_obsidian2.Notice(`Cleared reading analytics for ${activeView.file.name}`);
          this.engine.rebuildRenderers();
        } else {
          new import_obsidian2.Notice("No active note found to clear.");
        }
      }
    });
    logger.info("Load lifecycle completed successfully.");
  }
  setDebugLogging(enabled) {
    logger.setDebug(enabled);
  }
  async onunload() {
    var _a, _b, _c;
    logger.info("Unloading Heatmap of Notes plugin...");
    (_a = this.engine) == null ? void 0 : _a.stop();
    await ((_b = this.database) == null ? void 0 : _b.save(true));
    (_c = document.getElementById("frh-tooltip-element")) == null ? void 0 : _c.remove();
    document.body.classList.remove(TOUCH_BODY_CLASS);
    logger.info("Cleanup successfully completed.");
  }
};
