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

// focus-read-suite/src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => FocusReadSuitePlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian8 = require("obsidian");

// focus-read-suite/src/core/logger.ts
var LeveledLogger = class {
  constructor() {
    this.debugEnabled = false;
    this.prefix = "[Focus Read Suite]";
  }
  setDebug(enabled) {
    this.debugEnabled = Boolean(enabled);
  }
  get isDebug() {
    return this.debugEnabled;
  }
  debug(...args) {
    if (this.debugEnabled) console.debug(this.prefix, ...args);
  }
  info(...args) {
    console.info(this.prefix, ...args);
  }
  warn(...args) {
    console.warn(this.prefix, ...args);
  }
  error(...args) {
    console.error(this.prefix, ...args);
  }
};
var logger = new LeveledLogger();

// focus-read-suite/src/core/settings-schema.ts
var SECTION_IDS = [
  "general",
  "timer",
  "focus",
  "ruler",
  "typography",
  "heatmap",
  "appearance",
  "advanced"
];
var FONT_OPTIONS = [
  { id: "system", label: "System default", stack: "", googleFamily: null },
  { id: "lexend", label: "Lexend (recommended for ADHD)", stack: "'Lexend', sans-serif", googleFamily: "Lexend" },
  { id: "atkinson", label: "Atkinson Hyperlegible", stack: "'Atkinson Hyperlegible', sans-serif", googleFamily: "Atkinson+Hyperlegible" },
  { id: "inter", label: "Inter", stack: "'Inter', sans-serif", googleFamily: "Inter" },
  { id: "source", label: "Source Sans 3", stack: "'Source Sans 3', sans-serif", googleFamily: "Source+Sans+3" },
  { id: "ibmplex", label: "IBM Plex Sans", stack: "'IBM Plex Sans', sans-serif", googleFamily: "IBM+Plex+Sans" },
  { id: "noto", label: "Noto Sans", stack: "'Noto Sans', sans-serif", googleFamily: "Noto+Sans" },
  { id: "custom", label: "Custom font stack", stack: "", googleFamily: null }
];
function fontOptionById(id) {
  return FONT_OPTIONS.find((f) => f.id === id);
}
var DEFAULT_SETTINGS = {
  general: {
    statsEnabled: true,
    showNotices: true
  },
  timer: {
    enabled: true,
    workMinutes: 25,
    breakMinutes: 5,
    autoHide: true,
    autoHideSeconds: 4,
    pauseOnBlur: true,
    positionX: null,
    positionY: null,
    focusDetectionEnabled: true,
    focusDetectionIdleSeconds: 30,
    nudgeEnabled: false,
    nudgeIdleSeconds: 60,
    nudgeIgnoreScroll: true,
    dopamineEnabled: false,
    dopamineDailyGoalMinutes: 60
  },
  focus: {
    enabled: false,
    showNotch: true,
    notchSize: 44,
    focusLine: false,
    smoothFollow: false,
    keyboardStepPercent: 5
  },
  ruler: {
    height: 28,
    color: "#ffd54f",
    opacity: 0.18,
    mode: "auto",
    positionRatio: null
  },
  typography: {
    enabled: true,
    fontFamily: "system",
    customFontFamily: "",
    loadGoogleFonts: false,
    fontSize: 17,
    lineHeight: 1.7,
    maxWidthChars: 66,
    paragraphSpacing: 1.4
  },
  heatmap: {
    enabled: true,
    idleSeconds: 30,
    bucketCount: 100,
    width: 16,
    offsetRight: 12,
    opacity: 0.85
  },
  appearance: {
    accentMode: "native",
    customAccent: "#7c4dff",
    widgetScale: 1
  },
  advanced: {
    debugMode: false,
    refreshIntervalMs: 1e3
  }
};
function clampNum(value, min, max, fallback, round = true) {
  if (typeof value !== "number" || !Number.isFinite(value)) return fallback;
  const clamped = Math.min(Math.max(value, min), max);
  return round ? Math.round(clamped) : clamped;
}
function clampRatio2(value, min, max, fallback) {
  return Math.round(clampNum(value, min, max, fallback, false) * 100) / 100;
}
function boolOr(value, fallback) {
  return typeof value === "boolean" ? value : fallback;
}
function strOr(value, fallback) {
  return typeof value === "string" ? value : fallback;
}
function sanitizeFontStack(raw) {
  if (typeof raw !== "string") return "";
  return raw.replace(/[{}<>\\@]+/g, "").split(";").map((part) => part.trim()).filter((part) => part.length > 0).join(", ");
}
function resolveFontStack(settings) {
  if (settings.fontFamily === "custom") {
    return sanitizeFontStack(settings.customFontFamily);
  }
  const option = fontOptionById(settings.fontFamily);
  return option ? option.stack : "";
}
function normalizeHexColor(value, fallback) {
  return /^#[0-9a-fA-F]{6}$/.test(String(value)) ? String(value) : fallback;
}
function normalizeSettings(raw, sections = "*") {
  const out = JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
  if (!raw || typeof raw !== "object") return out;
  const sectionList = sections === "*" ? SECTION_IDS : sections;
  for (const section of sectionList) {
    const incoming = raw[section];
    if (!incoming || typeof incoming !== "object") continue;
    if (section === "general") {
      const d = DEFAULT_SETTINGS.general;
      out.general = {
        statsEnabled: boolOr(incoming.statsEnabled, d.statsEnabled),
        showNotices: boolOr(incoming.showNotices, d.showNotices)
      };
    } else if (section === "timer") {
      const d = DEFAULT_SETTINGS.timer;
      const pos = (key) => {
        const v = incoming[key];
        return typeof v === "number" && Number.isFinite(v) ? v : null;
      };
      out.timer = {
        enabled: boolOr(incoming.enabled, d.enabled),
        workMinutes: clampNum(incoming.workMinutes, 1, 180, d.workMinutes),
        breakMinutes: clampNum(incoming.breakMinutes, 1, 60, d.breakMinutes),
        autoHide: boolOr(incoming.autoHide, d.autoHide),
        autoHideSeconds: clampNum(incoming.autoHideSeconds, 1, 120, d.autoHideSeconds),
        pauseOnBlur: boolOr(incoming.pauseOnBlur, d.pauseOnBlur),
        positionX: pos("positionX"),
        positionY: pos("positionY"),
        focusDetectionEnabled: boolOr(incoming.focusDetectionEnabled, d.focusDetectionEnabled),
        focusDetectionIdleSeconds: clampNum(incoming.focusDetectionIdleSeconds, 5, 600, d.focusDetectionIdleSeconds),
        nudgeEnabled: boolOr(incoming.nudgeEnabled, d.nudgeEnabled),
        nudgeIdleSeconds: clampNum(incoming.nudgeIdleSeconds, 5, 600, d.nudgeIdleSeconds),
        nudgeIgnoreScroll: boolOr(incoming.nudgeIgnoreScroll, d.nudgeIgnoreScroll),
        dopamineEnabled: boolOr(incoming.dopamineEnabled, d.dopamineEnabled),
        dopamineDailyGoalMinutes: clampNum(incoming.dopamineDailyGoalMinutes, 1, 720, d.dopamineDailyGoalMinutes)
      };
    } else if (section === "focus") {
      const d = DEFAULT_SETTINGS.focus;
      out.focus = {
        enabled: boolOr(incoming.enabled, d.enabled),
        showNotch: boolOr(incoming.showNotch, d.showNotch),
        notchSize: clampNum(incoming.notchSize, 36, 56, d.notchSize),
        focusLine: boolOr(incoming.focusLine, d.focusLine),
        smoothFollow: boolOr(incoming.smoothFollow, d.smoothFollow),
        keyboardStepPercent: clampNum(incoming.keyboardStepPercent, 2, 25, d.keyboardStepPercent)
      };
    } else if (section === "ruler") {
      const d = DEFAULT_SETTINGS.ruler;
      const mode = incoming.mode;
      const ratio = incoming.positionRatio;
      out.ruler = {
        height: clampNum(incoming.height, 10, 80, d.height),
        color: normalizeHexColor(incoming.color, d.color),
        opacity: clampRatio2(incoming.opacity, 0.05, 0.9, d.opacity),
        mode: mode === "auto" || mode === "follow" || mode === "manual" ? mode : d.mode,
        positionRatio: ratio === null || ratio === void 0 ? null : Number.isFinite(Number(ratio)) ? Math.min(Math.max(Number(ratio), 0), 1) : null
      };
    } else if (section === "typography") {
      const d = DEFAULT_SETTINGS.typography;
      const family = fontOptionById(strOr(incoming.fontFamily, d.fontFamily)) ? strOr(incoming.fontFamily, d.fontFamily) : d.fontFamily;
      out.typography = {
        enabled: boolOr(incoming.enabled, d.enabled),
        fontFamily: family,
        customFontFamily: sanitizeFontStack(incoming.customFontFamily),
        loadGoogleFonts: boolOr(incoming.loadGoogleFonts, d.loadGoogleFonts),
        fontSize: clampNum(incoming.fontSize, 13, 26, d.fontSize),
        lineHeight: clampRatio2(incoming.lineHeight, 1.2, 2.2, d.lineHeight),
        maxWidthChars: clampNum(incoming.maxWidthChars, 40, 120, d.maxWidthChars),
        paragraphSpacing: clampRatio2(incoming.paragraphSpacing, 1, 2.5, d.paragraphSpacing)
      };
    } else if (section === "heatmap") {
      const d = DEFAULT_SETTINGS.heatmap;
      out.heatmap = {
        enabled: boolOr(incoming.enabled, d.enabled),
        idleSeconds: clampNum(incoming.idleSeconds, 5, 600, d.idleSeconds),
        bucketCount: clampNum(incoming.bucketCount, 10, 400, d.bucketCount),
        width: clampNum(incoming.width, 8, 48, d.width),
        offsetRight: clampNum(incoming.offsetRight, 0, 80, d.offsetRight),
        opacity: clampRatio2(incoming.opacity, 0.1, 1, d.opacity)
      };
    } else if (section === "appearance") {
      const d = DEFAULT_SETTINGS.appearance;
      const accentMode = incoming.accentMode;
      out.appearance = {
        accentMode: accentMode === "native" || accentMode === "custom" ? accentMode : d.accentMode,
        customAccent: normalizeHexColor(incoming.customAccent, d.customAccent),
        widgetScale: clampRatio2(incoming.widgetScale, 0.8, 1.25, d.widgetScale)
      };
    } else if (section === "advanced") {
      const d = DEFAULT_SETTINGS.advanced;
      out.advanced = {
        debugMode: boolOr(incoming.debugMode, d.debugMode),
        refreshIntervalMs: clampNum(incoming.refreshIntervalMs, 250, 5e3, d.refreshIntervalMs)
      };
    }
  }
  return out;
}
function formatClock(ms) {
  const totalSec = Math.max(0, Math.ceil(ms / 1e3));
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

// focus-read-suite/src/core/settings-manager.ts
var SAVE_DEBOUNCE_MS = 300;
var SettingsManager = class {
  constructor(io) {
    this.listeners = /* @__PURE__ */ new Set();
    this.saveTimer = null;
    this.saving = false;
    /** Extra persisted payloads (stats, heatmap records, migration info). */
    this.extras = {};
    this.io = io;
    this.settingsValue = normalizeSettings(null);
  }
  get settings() {
    return this.settingsValue;
  }
  get raw() {
    return this.extras;
  }
  /* ------------------------------------------------------------------ */
  /* Load / persist                                                      */
  /* ------------------------------------------------------------------ */
  /**
   * Loads the persisted payload. `onLoad` lets the caller (main.ts) run
   * migration between reading and normalizing.
   */
  async load(onLoad) {
    var _a, _b;
    let raw = null;
    try {
      raw = await this.io.loadData();
    } catch (err) {
      logger.error("Failed to read data.json. Falling back to defaults.", err);
      raw = null;
    }
    if (onLoad) {
      try {
        raw = (_a = await onLoad(raw)) != null ? _a : null;
      } catch (err) {
        logger.error("Settings load hook failed. Continuing with raw data.", err);
      }
    }
    if (raw && typeof raw === "object") {
      const { settings: _settings, version: _version, ...extrasOnly } = raw;
      this.extras = extrasOnly;
      this.settingsValue = normalizeSettings((_b = raw.settings) != null ? _b : void 0);
    } else {
      this.extras = {};
      this.settingsValue = normalizeSettings(null);
    }
  }
  /** Builds the full payload that gets written to data.json. */
  buildPayload() {
    return {
      ...this.extras,
      version: 2,
      settings: this.settingsValue
    };
  }
  async persist(immediate = true) {
    if (immediate) {
      this.cancelPendingSave();
      await this.flush();
      return;
    }
    if (this.saveTimer !== null) return;
    this.saveTimer = window.setTimeout(() => {
      this.saveTimer = null;
      void this.flush();
    }, SAVE_DEBOUNCE_MS);
  }
  cancelPendingSave() {
    if (this.saveTimer !== null) {
      clearTimeout(this.saveTimer);
      this.saveTimer = null;
    }
  }
  async flush() {
    if (this.saving) return;
    this.saving = true;
    try {
      await this.io.saveData(this.buildPayload());
    } catch (err) {
      logger.error("Failed to save settings.", err);
    } finally {
      this.saving = false;
    }
  }
  /* ------------------------------------------------------------------ */
  /* Updates                                                             */
  /* ------------------------------------------------------------------ */
  /**
   * The one write path. Applies `mutate` to a working copy, normalizes the
   * affected sections, persists, and notifies subscribers.
   *
   * @param mutate  receives a mutable draft (a deep copy); return nothing.
   * @param sections the sections the caller believes it touched — used for
   *                 normalization and change notification.
   * @param immediate force an instant disk write (default) vs debounced.
   */
  async update(sections, mutate, immediate = true) {
    const sectionList = Array.isArray(sections) ? sections : [sections];
    const next = { ...this.settingsValue };
    for (const s of sectionList) {
      next[s] = JSON.parse(JSON.stringify(this.settingsValue[s]));
    }
    try {
      mutate(next);
    } catch (err) {
      logger.error("Settings update threw; rejecting the change.", err);
      return;
    }
    const normalized = normalizeSettings(
      next,
      sectionList
    );
    const merged = { ...this.settingsValue };
    for (const s of sectionList) {
      merged[s] = normalized[s];
    }
    const changed = [];
    for (const s of sectionList) {
      if (JSON.stringify(this.settingsValue[s]) !== JSON.stringify(merged[s])) {
        changed.push(s);
      }
    }
    this.settingsValue = merged;
    if (changed.length > 0) {
      await this.persist(immediate);
      this.emit(changed);
    }
  }
  /* ------------------------------------------------------------------ */
  /* Extras (stats, records, migration info)                             */
  /* ------------------------------------------------------------------ */
  /** Reads an extra persisted payload (e.g. "stats", "heatmapRecords"). */
  getExtra(key) {
    return this.extras[key];
  }
  /** Writes an extra payload and schedules persistence. */
  async setExtra(key, value, immediate = false) {
    this.extras[key] = value;
    await this.persist(immediate);
  }
  /* ------------------------------------------------------------------ */
  /* Reset                                                               */
  /* ------------------------------------------------------------------ */
  /** Resets the given sections to their defaults (settings only). */
  async resetSections(sections) {
    const next = { ...this.settingsValue };
    for (const s of sections) {
      next[s] = JSON.parse(JSON.stringify(DEFAULT_SETTINGS[s]));
    }
    this.settingsValue = next;
    await this.persist(true);
    this.emit(sections);
  }
  /**
   * Replaces the whole settings object with an externally-built one
   * (used by the migration re-run). Normalizes, persists and notifies.
   */
  async replaceAllSettings(next) {
    this.settingsValue = normalizeSettings(next);
    await this.persist(true);
    this.emit(SECTION_IDS);
  }
  /* ------------------------------------------------------------------ */
  /* Change events                                                       */
  /* ------------------------------------------------------------------ */
  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  emit(changed) {
    for (const listener of [...this.listeners]) {
      try {
        listener(changed);
      } catch (err) {
        logger.error("A settings change listener threw.", err);
      }
    }
  }
};

// focus-read-suite/src/core/migration.ts
var LEGACY_PLUGIN_PATHS = {
  timer: ".obsidian/plugins/focus-read-timer/data.json",
  typography: ".obsidian/plugins/focus-read-typography/data.json",
  heatmap: ".obsidian/plugins/heatmap/data.json"
};
function numOr(source, key, fallback) {
  const v = source == null ? void 0 : source[key];
  return typeof v === "number" && Number.isFinite(v) ? v : fallback;
}
function boolOr2(source, key, fallback) {
  const v = source == null ? void 0 : source[key];
  return typeof v === "boolean" ? v : fallback;
}
function mapLegacyData(timerRaw, typographyRaw, heatmapRaw, current) {
  var _a, _b, _c, _d, _e, _f, _g, _h;
  const sources = [];
  const notes = [];
  const t = (_a = timerRaw == null ? void 0 : timerRaw.settings) != null ? _a : timerRaw ? timerRaw : void 0;
  const timer = {};
  if (timerRaw && t) {
    sources.push("focus-read-timer");
    timer.enabled = boolOr2(t, "timerEnabled", true);
    timer.workMinutes = numOr(t, "timerWorkMinutes", 25);
    timer.breakMinutes = numOr(t, "timerBreakMinutes", 5);
    timer.autoHide = boolOr2(t, "timerAutoHide", true);
    timer.autoHideSeconds = numOr(t, "timerAutoHideSeconds", 4);
    timer.pauseOnBlur = boolOr2(t, "timerPauseOnBlur", true);
    timer.positionX = typeof t.timerPositionX === "number" ? t.timerPositionX : null;
    timer.positionY = typeof t.timerPositionY === "number" ? t.timerPositionY : null;
    timer.focusDetectionEnabled = boolOr2(t, "focusDetectionEnabled", true);
    timer.focusDetectionIdleSeconds = numOr(t, "focusDetectionIdleSeconds", 30);
    timer.nudgeEnabled = boolOr2(t, "nudgeEnabled", false);
    timer.nudgeIdleSeconds = numOr(t, "nudgeIdleSeconds", 60);
    timer.nudgeIgnoreScroll = boolOr2(t, "nudgeIgnoreScroll", true);
    timer.dopamineEnabled = boolOr2(t, "dopamineEnabled", false);
    timer.dopamineDailyGoalMinutes = numOr(t, "dopamineDailyGoalMinutes", 60);
  }
  const ty = typographyRaw != null ? typographyRaw : {};
  const typography = {};
  const focus = {};
  const ruler = {};
  if (typographyRaw) {
    sources.push("focus-read-typography");
    typography.enabled = typeof ty.typographyEnabled === "boolean" ? ty.typographyEnabled : true;
    typography.fontFamily = typeof ty.fontFamily === "string" ? ty.fontFamily : "system";
    typography.customFontFamily = typeof ty.customFontFamily === "string" ? ty.customFontFamily : "";
    typography.loadGoogleFonts = typeof ty.loadGoogleFonts === "boolean" ? ty.loadGoogleFonts : false;
    typography.fontSize = ty.fontSize;
    typography.lineHeight = ty.lineHeight;
    typography.maxWidthChars = ty.maxWidthChars;
    typography.paragraphSpacing = ty.paragraphSpacing;
    focus.enabled = typeof ty.readingRulerEnabled === "boolean" ? ty.readingRulerEnabled : false;
    ruler.height = ty.readingRulerHeight;
    ruler.color = typeof ty.readingRulerColor === "string" ? ty.readingRulerColor : void 0;
    ruler.opacity = ty.readingRulerOpacity;
    ruler.mode = ty.readingRulerMode;
    ruler.positionRatio = (_b = ty.readingRulerPositionRatio) != null ? _b : null;
  }
  const h = (_c = heatmapRaw == null ? void 0 : heatmapRaw.settings) != null ? _c : {};
  const heatmap = {};
  const advanced = {};
  if (heatmapRaw) {
    sources.push("heatmap-of-notes");
    heatmap.idleSeconds = h.idleSeconds;
    heatmap.bucketCount = h.bucketCount;
    heatmap.width = h.heatmapWidth;
    heatmap.offsetRight = h.heatmapOffsetRight;
    heatmap.opacity = h.heatmapOpacity;
    advanced.refreshIntervalMs = h.refreshIntervalMs;
    advanced.debugMode = h.debugMode;
  }
  const mergedSettings = {
    ...(_d = current == null ? void 0 : current.settings) != null ? _d : {}
  };
  const setSection = (name, patch) => {
    var _a2;
    if (Object.keys(patch).length === 0) return;
    mergedSettings[name] = { ...(_a2 = mergedSettings[name]) != null ? _a2 : {}, ...patch };
  };
  setSection("timer", timer);
  setSection("typography", typography);
  setSection("focus", focus);
  setSection("ruler", ruler);
  setSection("heatmap", heatmap);
  setSection("advanced", advanced);
  const stats = (_f = (_e = timerRaw == null ? void 0 : timerRaw.stats) != null ? _e : current == null ? void 0 : current.stats) != null ? _f : void 0;
  const heatmapRecords = (_h = (_g = heatmapRaw == null ? void 0 : heatmapRaw.records) != null ? _g : current == null ? void 0 : current.heatmapRecords) != null ? _h : void 0;
  if (sources.length > 0) {
    notes.push(
      `Migrated settings from: ${sources.join(", ")}. The legacy plugin files were left untouched \u2014 disable the old plugins after verifying.`
    );
  }
  return {
    settings: mergedSettings,
    stats,
    heatmapRecords,
    info: {
      state: sources.length > 0 ? "done" : "skipped",
      at: (/* @__PURE__ */ new Date()).toISOString(),
      sources,
      notes
    }
  };
}
var MigrationService = class {
  constructor(reader) {
    this.reader = reader;
  }
  /**
   * Returns the payload to persist. Runs the legacy mapping exactly once
   * (guarded by the `migration` marker); a re-run can be forced from
   * Settings → Advanced.
   */
  async migrate(current, force = false) {
    var _a, _b, _c, _d;
    const alreadyDone = ((_a = current == null ? void 0 : current.migration) == null ? void 0 : _a.state) === "done" || ((_b = current == null ? void 0 : current.migration) == null ? void 0 : _b.state) === "skipped";
    if (current && alreadyDone && !force) {
      logger.debug("Migration already completed \u2014 skipping.");
      return current;
    }
    const [timerRaw, typographyRaw, heatmapRaw] = await Promise.all([
      this.reader.readJson(LEGACY_PLUGIN_PATHS.timer),
      this.reader.readJson(LEGACY_PLUGIN_PATHS.typography),
      this.reader.readJson(LEGACY_PLUGIN_PATHS.heatmap)
    ]);
    const result = mapLegacyData(timerRaw, typographyRaw, heatmapRaw, current);
    if (((_c = result.info.sources) != null ? _c : []).length === 0) {
      logger.info("No legacy plugin data found \u2014 starting with defaults.");
      if (force) {
        return {
          ...current != null ? current : {},
          migration: { state: "skipped", at: (/* @__PURE__ */ new Date()).toISOString(), sources: [], notes: ["No legacy plugin data was found."] }
        };
      }
      return {
        ...current != null ? current : {},
        migration: { state: "skipped", at: (/* @__PURE__ */ new Date()).toISOString(), sources: [] }
      };
    }
    const sources = (_d = result.info.sources) != null ? _d : [];
    logger.info(`Migrating settings from: ${sources.join(", ")}`);
    return {
      version: 2,
      settings: result.settings,
      stats: result.stats,
      heatmapRecords: result.heatmapRecords,
      migration: result.info
    };
  }
};

// focus-read-suite/src/core/lifecycle.ts
var LifecycleHub = class {
  constructor(host) {
    /** Records for diagnostics/tests. */
    this.domEvents = [];
    this.intervals = [];
    this.unloadHooks = [];
    this.host = host;
  }
  /** Registers a DOM listener that is auto-removed on unload. */
  domEvent(el, type, cb, options) {
    if (!el) {
      logger.warn(`domEvent(${type}) called with a null element \u2014 ignored.`);
      return;
    }
    this.host.registerDomEvent(el, type, cb, options);
    this.domEvents.push({ el, type, cb });
  }
  /** Registers an Obsidian event ref (workspace/vault events). */
  event(ref) {
    this.host.registerEvent(ref);
  }
  /** Runs `fn` on an interval that is auto-cleared on unload. */
  every(ms, fn) {
    const id = window.setInterval(fn, ms);
    this.host.registerInterval(id);
    this.intervals.push(id);
    return id;
  }
  /** Registers an interval id created elsewhere (parity with legacy code). */
  interval(id) {
    this.host.registerInterval(id);
    this.intervals.push(id);
    return id;
  }
  /** Runs `fn` once after `ms` — cleared automatically on unload. */
  later(ms, fn) {
    const id = window.setTimeout(fn, ms);
    const clear = () => clearTimeout(id);
    this.host.register(clear);
    this.unloadHooks.push(clear);
    return id;
  }
  /** Registers a callback that runs when the plugin unloads. */
  onUnload(cb) {
    this.host.register(cb);
    this.unloadHooks.push(cb);
  }
  get stats() {
    return {
      domEvents: this.domEvents.length,
      intervals: this.intervals.length,
      eventRefs: -1,
      // refs are opaque; not tracked individually
      unloadHooks: this.unloadHooks.length
    };
  }
};

// focus-read-suite/src/modules/timer/TimerModule.ts
var import_obsidian = require("obsidian");

// focus-read-suite/src/modules/timer/FocusTimer.ts
var FocusTimer = class {
  constructor(host, nowMs = () => performance.now()) {
    this.intervalId = null;
    this.phase = "idle";
    this.running = false;
    this.remainingMs = 0;
    this.totalMs = 0;
    this.focusMs = 0;
    this.lastTickAt = 0;
    this.lastRenderedSecond = -1;
    this.host = host;
    this.nowMs = nowMs;
  }
  get snapshot() {
    return {
      phase: this.phase,
      running: this.running,
      remainingMs: this.remainingMs,
      totalMs: this.totalMs,
      focusMs: this.focusMs
    };
  }
  /* ------------------------------------------------------------------ */
  /* Control                                                             */
  /* ------------------------------------------------------------------ */
  startWork() {
    const s = this.host.getSettings();
    this.phase = "work";
    this.running = true;
    this.totalMs = Math.max(6e4 / 60, s.workMinutes * 6e4);
    this.remainingMs = this.totalMs;
    this.focusMs = 0;
    this.lastTickAt = this.nowMs();
    this.lastRenderedSecond = -1;
    this.ensureTicking();
    this.emit();
  }
  startBreak() {
    const s = this.host.getSettings();
    this.phase = "break";
    this.running = true;
    this.totalMs = s.breakMinutes * 6e4;
    this.remainingMs = this.totalMs;
    this.focusMs = 0;
    this.lastTickAt = this.nowMs();
    this.lastRenderedSecond = -1;
    this.ensureTicking();
    this.emit();
  }
  pause() {
    if (this.running) {
      this.running = false;
      this.emit();
    }
  }
  resume() {
    if (!this.running && this.phase !== "idle") {
      this.running = true;
      this.lastTickAt = this.nowMs();
      this.ensureTicking();
      this.emit();
    }
  }
  togglePauseResume() {
    if (this.running) this.pause();
    else this.resume();
  }
  stop() {
    this.phase = "idle";
    this.running = false;
    this.remainingMs = 0;
    this.totalMs = 0;
    this.focusMs = 0;
    this.lastRenderedSecond = -1;
    this.emit();
  }
  addTime(ms) {
    if (this.phase === "idle") return false;
    this.remainingMs += ms;
    this.totalMs += ms;
    this.emit();
    return true;
  }
  /* ------------------------------------------------------------------ */
  /* Ticking                                                             */
  /* ------------------------------------------------------------------ */
  tick() {
    if (this.phase === "idle" || !this.running) return;
    const now = this.nowMs();
    const elapsed = Math.max(0, now - this.lastTickAt);
    this.lastTickAt = now;
    this.remainingMs = Math.max(0, this.remainingMs - elapsed);
    if (this.phase === "work" && this.host.isUserFocused()) {
      this.focusMs += elapsed;
    }
    const shownSecond = Math.ceil(this.remainingMs / 1e3);
    if (shownSecond !== this.lastRenderedSecond) {
      this.lastRenderedSecond = shownSecond;
      this.emit();
    }
    if (this.remainingMs <= 0) {
      const finishedPhase = this.phase;
      const focusMs = this.focusMs;
      this.stop();
      if (finishedPhase === "work") this.host.onWorkComplete(focusMs);
      else this.host.onBreakComplete();
    }
  }
  ensureTicking() {
    if (this.intervalId !== null) return;
    this.intervalId = window.setInterval(() => this.tick(), 250);
  }
  /** Stops the internal interval (unload, or when fully idle). */
  shutdown() {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }
  emit() {
    this.host.onSnapshot(this.snapshot);
  }
};

// focus-read-suite/src/core/viewport.ts
function getViewportSize() {
  var _a, _b, _c, _d;
  const w = typeof window !== "undefined" ? (_b = (_a = window.visualViewport) == null ? void 0 : _a.width) != null ? _b : window.innerWidth : 1024;
  const h = typeof window !== "undefined" ? (_d = (_c = window.visualViewport) == null ? void 0 : _c.height) != null ? _d : window.innerHeight : 768;
  return { width: Math.max(0, w), height: Math.max(0, h) };
}
function clampToViewport(x, y, elWidth, elHeight) {
  const { width, height } = getViewportSize();
  const maxX = Math.max(0, width - elWidth);
  const maxY = Math.max(0, height - elHeight);
  return {
    x: Math.min(Math.max(0, x), maxX),
    y: Math.min(Math.max(0, y), maxY)
  };
}
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
function createRafScheduler() {
  let scheduled = false;
  let pending = null;
  return (fn) => {
    pending = fn;
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      const run = pending;
      pending = null;
      run == null ? void 0 : run();
    });
  };
}
function registerViewportChangeHandlers(register, handler) {
  register(window, "resize", handler);
  register(window, "orientationchange", handler);
  if (typeof window !== "undefined" && window.visualViewport) {
    register(window.visualViewport, "resize", handler);
  }
}

// focus-read-suite/src/modules/timer/TimerWidget.ts
var TIMER_ELEMENT_ID = "frs-timer";
var TimerWidget = class {
  constructor(host) {
    this.el = null;
    this.dragging = false;
    this.dragPointerId = null;
    this.dragOffsetX = 0;
    this.dragOffsetY = 0;
    this.collapsed = false;
    /** For double-tap detection on touch (dblclick is unreliable there). */
    this.lastHeaderTapAt = 0;
    this.lastHeaderTapX = 0;
    this.lastHeaderTapY = 0;
    this.autoHideTimer = null;
    this.host = host;
  }
  /* ------------------------------------------------------------------ */
  /* Lifecycle                                                           */
  /* ------------------------------------------------------------------ */
  mount() {
    if (document.getElementById(TIMER_ELEMENT_ID)) return;
    const el = document.createElement("div");
    el.id = TIMER_ELEMENT_ID;
    el.className = "frs-timer";
    el.style.display = "none";
    el.innerHTML = `
      <div class="frs-timer-header" title="Drag to move \u2014 double-click to collapse">
        <span class="frs-grip" aria-hidden="true">\u283F</span>
        <span class="frs-timer-title">Focus Reader</span>
        <span class="frs-timer-phase"><span class="frs-timer-phase-dot"></span><span class="frs-timer-phase-label">Ready</span></span>
      </div>
      <div class="frs-timer-body">
        <div class="frs-timer-clock">00:00</div>
        <div class="frs-timer-progress"><div class="frs-timer-progress-fill"></div></div>
        <div class="frs-timer-info">Click Start to begin</div>
        <div class="frs-timer-controls">
          <button class="frs-btn frs-btn-primary" data-action="start">Start</button>
          <button class="frs-btn" data-action="pause">Pause</button>
          <button class="frs-btn" data-action="addtime">+30s</button>
          <button class="frs-btn frs-btn-danger" data-action="stop">Stop</button>
        </div>
      </div>
    `;
    document.body.appendChild(el);
    this.el = el;
    this.bindControls(el);
    this.bindDrag(el);
    this.applyVisibility();
    this.applySavedPosition();
  }
  destroy() {
    var _a;
    this.cancelAutoHide();
    (_a = this.el) == null ? void 0 : _a.remove();
    this.el = null;
  }
  /* ------------------------------------------------------------------ */
  /* Visibility & position                                               */
  /* ------------------------------------------------------------------ */
  applyVisibility() {
    const el = this.el;
    if (!el) return;
    const visible = this.host.getSettings().enabled;
    el.style.display = visible ? "block" : "none";
    if (visible) this.applySavedPosition();
  }
  /**
   * Restores the saved position clamped into the current viewport — keeps
   * the timer reachable after switching from a big desktop screen to a phone.
   */
  applySavedPosition() {
    const el = this.el;
    if (!el) return;
    const { positionX, positionY } = this.host.getSettings();
    if (positionX === null || positionY === null) {
      el.style.left = "auto";
      el.style.top = "16px";
      el.style.right = "16px";
      return;
    }
    const rect = el.getBoundingClientRect();
    const { x, y } = clampToViewport(positionX, positionY, rect.width || 220, rect.height || 150);
    el.style.right = "auto";
    el.style.left = `${Math.round(x)}px`;
    el.style.top = `${Math.round(y)}px`;
  }
  /** Re-clamps after a resize/orientation change. */
  reflow() {
    if (!this.el || this.dragging) return;
    const { positionX, positionY } = this.host.getSettings();
    if (positionX === null || positionY === null) return;
    this.applySavedPosition();
  }
  resetPosition() {
    const el = this.el;
    if (!el) return;
    el.style.left = "auto";
    el.style.right = "16px";
    el.style.top = "16px";
  }
  /* ------------------------------------------------------------------ */
  /* Rendering                                                           */
  /* ------------------------------------------------------------------ */
  render(snap) {
    const el = this.el;
    if (!el) return;
    const s = this.host.getSettings();
    const clockEl = el.querySelector(".frs-timer-clock");
    const infoEl = el.querySelector(".frs-timer-info");
    const fillEl = el.querySelector(".frs-timer-progress-fill");
    const phaseLabelEl = el.querySelector(".frs-timer-phase-label");
    const cardEl = el.querySelector(".frs-timer-body");
    const startBtn = el.querySelector('[data-action="start"]');
    const pauseBtn = el.querySelector('[data-action="pause"]');
    const addBtn = el.querySelector('[data-action="addtime"]');
    const stopBtn = el.querySelector('[data-action="stop"]');
    const phaseKey = snap.phase === "idle" ? "ready" : snap.phase === "break" ? "break" : snap.running ? "reading" : "paused";
    el.setAttribute("data-phase", phaseKey);
    if (phaseLabelEl) {
      phaseLabelEl.textContent = phaseKey === "ready" ? "Ready" : phaseKey === "break" ? "Break" : phaseKey === "reading" ? "Reading" : "Paused";
    }
    if (snap.phase === "idle") {
      if (clockEl) clockEl.textContent = formatClock(s.workMinutes * 6e4);
      if (fillEl) fillEl.style.width = "0%";
      if (infoEl) infoEl.textContent = "Click Start to begin";
    } else {
      if (clockEl) clockEl.textContent = formatClock(snap.remainingMs);
      const pct = snap.totalMs > 0 ? (1 - snap.remainingMs / snap.totalMs) * 100 : 0;
      if (fillEl) fillEl.style.width = `${pct}%`;
      if (infoEl) {
        infoEl.textContent = snap.phase === "break" ? "Break \u2014 stretch, breathe" : snap.running ? `+${Math.round(snap.focusMs / 6e4)} min focused` : "Paused";
      }
    }
    if (cardEl) {
      cardEl.classList.toggle("frs-timer-collapsed-body", this.collapsed);
    }
    el.classList.toggle("frs-timer-collapsed", this.collapsed);
    if (startBtn) {
      const startDisabled = snap.phase === "work" && !snap.running;
      startBtn.disabled = startDisabled;
      startBtn.textContent = snap.phase === "break" ? "Skip Break" : "Start";
    }
    if (pauseBtn) {
      pauseBtn.disabled = snap.phase === "idle";
      pauseBtn.textContent = snap.running ? "Pause" : "Resume";
    }
    if (addBtn) addBtn.disabled = snap.phase === "idle";
    if (stopBtn) stopBtn.disabled = snap.phase === "idle";
  }
  /* ------------------------------------------------------------------ */
  /* Interaction                                                         */
  /* ------------------------------------------------------------------ */
  bindControls(el) {
    const controls = el.querySelector(".frs-timer-controls");
    if (!controls) return;
    this.host.registerDomEvent(controls, "pointerdown", (e) => e.stopPropagation());
    this.host.registerDomEvent(controls, "click", (e) => {
      var _a, _b;
      const btn = (_b = (_a = e.target) == null ? void 0 : _a.closest) == null ? void 0 : _b.call(_a, ".frs-btn");
      if (!btn) return;
      e.stopPropagation();
      this.host.onControl(btn.getAttribute("data-action"));
    });
  }
  bindDrag(el) {
    const header = el.querySelector(".frs-timer-header");
    if (!header) return;
    const register = (type, cb, options) => this.host.registerDomEvent(header, type, cb, options);
    register("pointerdown", (e) => {
      if (e.button !== void 0 && e.button !== 0) return;
      this.dragging = true;
      this.dragPointerId = e.pointerId;
      const rect = el.getBoundingClientRect();
      this.dragOffsetX = e.clientX - rect.left;
      this.dragOffsetY = e.clientY - rect.top;
      el.classList.add("frs-dragging");
      el.style.right = "auto";
      el.style.left = `${rect.left}px`;
      el.style.top = `${rect.top}px`;
      try {
        header.setPointerCapture(e.pointerId);
      } catch (e2) {
      }
      e.preventDefault();
      e.stopPropagation();
    });
    register("pointermove", (e) => {
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      const rect = el.getBoundingClientRect();
      const { x, y } = clampToViewport(
        e.clientX - this.dragOffsetX,
        e.clientY - this.dragOffsetY,
        rect.width || 220,
        rect.height || 150
      );
      el.style.left = `${Math.round(x)}px`;
      el.style.top = `${Math.round(y)}px`;
      e.preventDefault();
    });
    const endDrag = (e) => {
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      this.finishDrag(header, e.pointerId);
    };
    register("pointerup", endDrag);
    register("pointercancel", endDrag);
    register("lostpointercapture", (e) => {
      if (this.dragging && e.pointerId === this.dragPointerId) {
        this.finishDrag(header, e.pointerId);
      }
    });
    register("contextmenu", (e) => {
      if (this.dragging) e.preventDefault();
    });
    register("dblclick", () => this.toggleCollapsed());
    register("pointerup", (e) => {
      if (e.pointerType === "touch") this.maybeDoubleTap(e);
    });
  }
  finishDrag(header, pointerId) {
    var _a, _b;
    this.dragging = false;
    this.dragPointerId = null;
    (_a = this.el) == null ? void 0 : _a.classList.remove("frs-dragging");
    try {
      header.releasePointerCapture(pointerId);
    } catch (e) {
    }
    const rect = (_b = this.el) == null ? void 0 : _b.getBoundingClientRect();
    if (rect) {
      this.host.savePosition(Math.round(rect.left), Math.round(rect.top));
    }
  }
  /** Manual double-tap detection (dblclick does not fire reliably on touch). */
  maybeDoubleTap(e) {
    const now = Date.now();
    const isDoubleTap = now - this.lastHeaderTapAt < 320 && Math.abs(e.clientX - this.lastHeaderTapX) < 30 && Math.abs(e.clientY - this.lastHeaderTapY) < 30;
    this.lastHeaderTapAt = now;
    this.lastHeaderTapX = e.clientX;
    this.lastHeaderTapY = e.clientY;
    if (isDoubleTap) {
      this.lastHeaderTapAt = 0;
      this.toggleCollapsed();
    }
  }
  toggleCollapsed() {
    this.collapsed = !this.collapsed;
    if (this.el) {
      this.el.classList.toggle("frs-timer-collapsed", this.collapsed);
      const body = this.el.querySelector(".frs-timer-body");
      body == null ? void 0 : body.classList.toggle("frs-timer-collapsed-body", this.collapsed);
    }
  }
  get isCollapsed() {
    return this.collapsed;
  }
  /* ------------------------------------------------------------------ */
  /* Auto-hide                                                           */
  /* ------------------------------------------------------------------ */
  /** Un-dims the widget and restarts the auto-hide countdown. */
  poke() {
    if (!this.el) return;
    this.el.classList.remove("frs-dimmed");
    this.resetAutoHide();
  }
  resetAutoHide() {
    const s = this.host.getSettings();
    if (this.autoHideTimer !== null) {
      clearTimeout(this.autoHideTimer);
      this.autoHideTimer = null;
    }
    if (!s.autoHide) return;
    this.autoHideTimer = window.setTimeout(() => {
      if (this.el && !this.dragging) this.el.classList.add("frs-dimmed");
    }, s.autoHideSeconds * 1e3);
  }
  cancelAutoHide() {
    if (this.autoHideTimer !== null) {
      clearTimeout(this.autoHideTimer);
      this.autoHideTimer = null;
    }
  }
};

// focus-read-suite/src/modules/timer/stats.ts
var DEFAULT_STATS = {
  totalReadingMs: 0,
  todayMs: 0,
  todayDate: "",
  streak: 0,
  lastReadDate: "",
  longestStreak: 0,
  perDayMs: {},
  longestFocusMs: 0,
  sessionsToday: 0
};
function formatDate(date) {
  const d = date != null ? date : /* @__PURE__ */ new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
function dayDiff(a, b) {
  if (!a || !b) return 0;
  return Math.round(
    ((/* @__PURE__ */ new Date(b + "T00:00:00")).getTime() - (/* @__PURE__ */ new Date(a + "T00:00:00")).getTime()) / 864e5
  );
}
function normalizeStats(raw) {
  const merged = { ...DEFAULT_STATS, ...raw != null ? raw : {} };
  if (!merged.perDayMs || typeof merged.perDayMs !== "object") merged.perDayMs = {};
  for (const key of Object.keys(merged.perDayMs)) {
    const v = merged.perDayMs[key];
    if (typeof v !== "number" || !Number.isFinite(v) || v < 0) delete merged.perDayMs[key];
  }
  if (typeof merged.streak !== "number" || merged.streak < 0) merged.streak = 0;
  if (typeof merged.longestStreak !== "number" || merged.longestStreak < 0) merged.longestStreak = 0;
  if (typeof merged.longestFocusMs !== "number" || merged.longestFocusMs < 0) merged.longestFocusMs = 0;
  return merged;
}
var _ReadingStatsTracker = class _ReadingStatsTracker {
  constructor(host, nowMs = () => Date.now(), dateFn = () => formatDate()) {
    this.lastPersistAt = 0;
    this.host = host;
    this.nowMs = nowMs;
    this.dateFn = dateFn;
    this.lastAccrualAt = nowMs();
  }
  /** Restarts the accrual window (e.g. after focus loss). */
  resetWindow() {
    this.lastAccrualAt = this.nowMs();
  }
  /**
   * Rolls the daily counters over if the date changed. Updates streaks.
   * Must be called before reading/writing today's numbers.
   */
  rollOver() {
    const stats = this.host.getStats();
    const today = this.dateFn();
    if (stats.todayDate === today) return;
    if (stats.lastReadDate) {
      const diff = dayDiff(stats.lastReadDate, today);
      if (diff === 1) stats.streak = (stats.streak || 0) + 1;
      else if (diff > 1) stats.streak = 1;
    } else {
      stats.streak = 1;
    }
    stats.longestStreak = Math.max(stats.longestStreak || 0, stats.streak);
    stats.todayMs = 0;
    stats.sessionsToday = 0;
    stats.todayDate = today;
    this.host.persist();
  }
  /**
   * Accrues elapsed wall-clock time since the last successful accrual.
   * Returns the ms actually recorded (0 when nothing counted).
   */
  accrue(windowFocused, userActive) {
    const now = this.nowMs();
    let delta = now - this.lastAccrualAt;
    this.lastAccrualAt = now;
    if (!windowFocused || !userActive) return 0;
    if (delta > _ReadingStatsTracker.MAX_CHUNK_MS) delta = _ReadingStatsTracker.MAX_CHUNK_MS;
    if (delta < _ReadingStatsTracker.MIN_CHUNK_MS) return 0;
    this.rollOver();
    const stats = this.host.getStats();
    const today = this.dateFn();
    stats.totalReadingMs += delta;
    stats.todayMs += delta;
    stats.lastReadDate = today;
    stats.perDayMs[today] = (stats.perDayMs[today] || 0) + delta;
    if (now - this.lastPersistAt > _ReadingStatsTracker.SAVE_INTERVAL_MS) {
      this.lastPersistAt = now;
      this.host.persist();
    }
    return delta;
  }
  /** Records a completed focus session. */
  recordSession(focusMs) {
    const stats = this.host.getStats();
    stats.sessionsToday = (stats.sessionsToday || 0) + 1;
    if (focusMs > stats.longestFocusMs) stats.longestFocusMs = focusMs;
    this.host.persist();
  }
  /** Today's reading in whole minutes. */
  todayMinutes() {
    return Math.round(this.host.getStats().todayMs / 6e4);
  }
};
/** Cap on a single accrual chunk — avoids huge jumps after sleep/resume. */
_ReadingStatsTracker.MAX_CHUNK_MS = 3e5;
/** Minimum chunk worth recording. */
_ReadingStatsTracker.MIN_CHUNK_MS = 1e3;
/** Persist at most every 10 s. */
_ReadingStatsTracker.SAVE_INTERVAL_MS = 1e4;
var ReadingStatsTracker = _ReadingStatsTracker;

// focus-read-suite/src/modules/timer/NudgeController.ts
var NUDGE_ID = "frs-nudge";
var NudgeController = class {
  constructor(host, idleThresholdMs, nowMs = () => Date.now()) {
    this.visible = false;
    this.dismissedAt = null;
    this.host = host;
    this.idleThresholdMs = idleThresholdMs;
    this.nowMs = nowMs;
    this.lastInputActivityAt = nowMs();
  }
  /** Called on real user input (keyboard, taps — not passive scroll). */
  noteInputActivity(at) {
    this.lastInputActivityAt = at != null ? at : this.nowMs();
    this.dismissedAt = null;
    if (this.visible) this.hide();
  }
  /** Runs on the periodic check; shows the nudge when appropriate. */
  checkIdle(now) {
    if (this.visible) return;
    const at = now != null ? now : this.nowMs();
    const threshold = this.idleThresholdMs();
    const idleMs = at - this.lastInputActivityAt;
    if (idleMs < threshold) return;
    if (this.dismissedAt !== null) {
      const snoozeMs = Math.max(threshold * 2, 6e4);
      if (at - this.dismissedAt < snoozeMs) return;
      this.dismissedAt = null;
    }
    this.show();
  }
  get is_visible() {
    return this.visible;
  }
  show() {
    if (this.visible || document.getElementById(NUDGE_ID)) return;
    const nudge = document.createElement("div");
    nudge.id = NUDGE_ID;
    nudge.className = "frs-nudge";
    nudge.setAttribute("role", "alert");
    const remaining = this.host.getWorkRemainingMs();
    const body = remaining !== null && remaining > 0 ? `Continue? ${Math.ceil(remaining / 6e4)} min left in session.` : `You've been idle for ${Math.round(this.idleThresholdMs() / 1e3)}s. Get back to reading?`;
    nudge.innerHTML = `
      <div class="frs-nudge-title">You stopped reading.</div>
      <div class="frs-nudge-body">${body}</div>
      <div class="frs-nudge-actions">
        <button class="frs-btn frs-btn-primary frs-nudge-continue">Continue</button>
        <button class="frs-btn frs-nudge-dismiss">Dismiss</button>
      </div>`;
    document.body.appendChild(nudge);
    this.visible = true;
    const continueBtn = nudge.querySelector(".frs-nudge-continue");
    const dismissBtn = nudge.querySelector(".frs-nudge-dismiss");
    if (continueBtn) {
      this.host.registerDomEvent(continueBtn, "click", () => {
        this.host.onContinue();
        this.noteInputActivity();
      });
    }
    if (dismissBtn) {
      this.host.registerDomEvent(dismissBtn, "click", () => {
        this.dismissedAt = this.nowMs();
        this.hide();
      });
    }
  }
  hide() {
    var _a;
    (_a = document.getElementById(NUDGE_ID)) == null ? void 0 : _a.remove();
    this.visible = false;
  }
  destroy() {
    this.hide();
  }
};

// focus-read-suite/src/modules/timer/DopamineBar.ts
var GOAL_BAR_ID = "frs-goal-bar";
var GOAL_BAR_LABEL_ID = "frs-goal-bar-label";
var GoalBar = class {
  constructor() {
    this.bar = null;
    this.label = null;
    /** Guard: a destroyed bar must never resurrect via render(). */
    this.destroyed = false;
  }
  mount() {
    if (this.destroyed) return;
    if (document.getElementById(GOAL_BAR_ID)) return;
    const bar = document.createElement("div");
    bar.id = GOAL_BAR_ID;
    bar.className = "frs-goal-bar";
    bar.innerHTML = `<div class="frs-goal-bar-fill"></div>`;
    bar.style.display = "none";
    document.body.appendChild(bar);
    const label = document.createElement("div");
    label.id = GOAL_BAR_LABEL_ID;
    label.className = "frs-goal-bar-label";
    label.style.display = "none";
    document.body.appendChild(label);
    this.bar = bar;
    this.label = label;
  }
  destroy() {
    var _a, _b;
    this.destroyed = true;
    (_a = this.bar) == null ? void 0 : _a.remove();
    (_b = this.label) == null ? void 0 : _b.remove();
    this.bar = null;
    this.label = null;
  }
  applyVisibility(enabled) {
    if (this.destroyed) return;
    this.mountIfMissing();
    if (this.bar) this.bar.style.display = enabled ? "block" : "none";
    if (this.label) this.label.style.display = enabled ? "block" : "none";
    if (enabled) this.render(0, 1);
  }
  mountIfMissing() {
    if (!this.bar || !this.label || !document.getElementById(GOAL_BAR_ID)) {
      this.bar = null;
      this.label = null;
      this.mount();
    }
  }
  render(todayMinutes, goalMinutes) {
    if (this.destroyed) return;
    this.mountIfMissing();
    if (!this.bar || !this.label) return;
    const goal = Math.max(1, goalMinutes);
    const pct = Math.min(100, Math.round(todayMinutes / goal * 100));
    const fill = this.bar.querySelector(".frs-goal-bar-fill");
    if (fill) fill.style.width = `${pct}%`;
    this.label.textContent = `${todayMinutes} / ${goal} min (${pct}%)`;
  }
};

// focus-read-suite/src/modules/timer/TimerModule.ts
var STATS_KEY = "stats";
var TimerModule = class {
  constructor() {
    this.id = "timer";
    this.name = "Focus Read Timer";
    this.stats = { ...DEFAULT_STATS };
    /* Activity tracking */
    this.lastActivityAt = 0;
    this.lastInputActivityAt = 0;
    this.windowFocused = true;
  }
  /* ------------------------------------------------------------------ */
  /* Lifecycle                                                           */
  /* ------------------------------------------------------------------ */
  async load(ctx) {
    this.ctx = ctx;
    const { settings, lifecycle } = ctx;
    this.stats = normalizeStats(settings.getExtra(STATS_KEY));
    this.lastActivityAt = Date.now();
    this.lastInputActivityAt = Date.now();
    this.statsTracker = new ReadingStatsTracker({
      getStats: () => this.stats,
      persist: () => {
        void settings.setExtra(STATS_KEY, this.stats, false);
      }
    });
    this.statsTracker.rollOver();
    this.widget = new TimerWidget({
      getSettings: () => settings.settings.timer,
      onControl: (action) => this.handleControl(action),
      registerDomEvent: (el, type, cb, options) => lifecycle.domEvent(el, type, cb, options),
      savePosition: (x, y) => {
        void settings.update("timer", (draft) => {
          draft.timer.positionX = x;
          draft.timer.positionY = y;
        }, false);
      }
    });
    this.timer = new FocusTimer({
      getSettings: () => settings.settings.timer,
      isUserFocused: () => this.isUserFocused(),
      onSnapshot: (snap) => this.onTimerSnapshot(snap),
      onWorkComplete: (focusMs) => this.onWorkComplete(focusMs),
      onBreakComplete: () => {
        this.notify("Break over. Ready for another session?");
      }
    });
    this.nudge = new NudgeController(
      {
        registerDomEvent: (el, type, cb, options) => lifecycle.domEvent(el, type, cb, options),
        getWorkRemainingMs: () => this.timer.phase === "work" && this.timer.running ? this.timer.remainingMs : null,
        onContinue: () => this.widget.poke()
      },
      () => settings.settings.timer.nudgeIdleSeconds * 1e3
    );
    this.goalBar = new GoalBar();
    this.widget.mount();
    this.goalBar.mount();
    this.widget.render(this.timer.snapshot);
    this.goalBar.applyVisibility(settings.settings.timer.dopamineEnabled);
    if (settings.settings.timer.dopamineEnabled) {
      this.goalBar.render(this.statsTracker.todayMinutes(), settings.settings.timer.dopamineDailyGoalMinutes);
    }
    lifecycle.domEvent(window, "pointermove", () => this.onActivity(false), { passive: true });
    lifecycle.domEvent(window, "keydown", () => this.onActivity(true), { passive: true });
    lifecycle.domEvent(window, "scroll", () => this.onActivity(!settings.settings.timer.nudgeIgnoreScroll), { passive: true });
    lifecycle.domEvent(window, "pointerdown", () => this.onActivity(true), { passive: true });
    lifecycle.domEvent(window, "blur", () => {
      this.windowFocused = false;
      if (settings.settings.timer.pauseOnBlur && this.timer.running) {
        this.timer.pause();
        this.notify("Paused: window lost focus");
      }
    });
    lifecycle.domEvent(window, "focus", () => {
      this.windowFocused = true;
      this.onActivity(true);
    });
    lifecycle.domEvent(document, "visibilitychange", () => {
      if (document.hidden) {
        if (settings.settings.timer.pauseOnBlur && this.timer.running) {
          this.timer.pause();
          this.notify("Paused: tab hidden");
        }
      } else {
        this.windowFocused = true;
        this.onActivity(true);
      }
    });
    registerViewportChangeHandlers(
      (target, type, cb) => lifecycle.domEvent(target, type, cb),
      () => this.widget.reflow()
    );
    lifecycle.every(5e3, () => {
      if (this.ctx.settings.settings.timer.nudgeEnabled) this.nudge.checkIdle();
    });
    lifecycle.every(3e4, () => this.flushReadingTime());
    lifecycle.every(5e3, () => {
      if (this.ctx.settings.settings.timer.dopamineEnabled) {
        this.goalBar.render(
          this.statsTracker.todayMinutes(),
          this.ctx.settings.settings.timer.dopamineDailyGoalMinutes
        );
      }
    });
    this.registerCommands(ctx);
    logger.debug("Timer module loaded.");
  }
  async unload() {
    var _a, _b, _c, _d;
    (_a = this.timer) == null ? void 0 : _a.shutdown();
    this.flushReadingTime();
    (_b = this.widget) == null ? void 0 : _b.destroy();
    (_c = this.nudge) == null ? void 0 : _c.destroy();
    (_d = this.goalBar) == null ? void 0 : _d.destroy();
    await this.ctx.settings.setExtra(STATS_KEY, this.stats, true);
    logger.debug("Timer module unloaded.");
  }
  /* ------------------------------------------------------------------ */
  /* Settings                                                            */
  /* ------------------------------------------------------------------ */
  sections() {
    return ["timer", "general"];
  }
  onSettingsChanged(sections) {
    const s = this.ctx.settings.settings;
    if (sections.includes("timer")) {
      if (!s.timer.enabled) this.timer.stop();
      this.widget.applyVisibility();
      this.widget.render(this.timer.snapshot);
      this.goalBar.applyVisibility(s.timer.dopamineEnabled);
      if (s.timer.dopamineEnabled) {
        this.goalBar.render(this.statsTracker.todayMinutes(), s.timer.dopamineDailyGoalMinutes);
      }
    }
    if (sections.includes("general")) {
      this.flushReadingTime();
    }
  }
  /* ------------------------------------------------------------------ */
  /* Public API (commands)                                               */
  /* ------------------------------------------------------------------ */
  startWork() {
    const s = this.ctx.settings.settings.timer;
    if (!s.enabled) {
      new import_obsidian.Notice("Enable the Focus Read Timer module first (Settings \u2192 Focus Read Timer).");
      return;
    }
    this.timer.startWork();
    this.notify(`Focus session started: ${s.workMinutes} min`);
  }
  togglePause() {
    if (this.timer.phase === "idle") this.startWork();
    else this.timer.togglePauseResume();
  }
  stop() {
    this.timer.stop();
  }
  async resetPosition() {
    await this.ctx.settings.update("timer", (draft) => {
      draft.timer.positionX = null;
      draft.timer.positionY = null;
    });
    this.widget.resetPosition();
    this.notify("Timer moved back to the top-right corner.");
  }
  /* ------------------------------------------------------------------ */
  /* Internals                                                           */
  /* ------------------------------------------------------------------ */
  registerCommands(ctx) {
    ctx.addCommand({ id: "start-focus-session", name: "Start focus session", callback: () => this.startWork() });
    ctx.addCommand({
      id: "pause-resume-focus-session",
      name: "Pause/resume focus session",
      callback: () => this.togglePause()
    });
    ctx.addCommand({ id: "stop-focus-session", name: "Stop focus session", callback: () => this.stop() });
    ctx.addCommand({
      id: "reset-timer-position",
      name: "Reset timer position to top-right",
      callback: () => void this.resetPosition()
    });
  }
  notify(message) {
    var _a;
    if ((_a = this.ctx) == null ? void 0 : _a.settings.settings.general.showNotices) new import_obsidian.Notice(message);
  }
  isUserFocused() {
    const s = this.ctx.settings.settings.timer;
    if (!s.focusDetectionEnabled) return this.windowFocused;
    return this.windowFocused && Date.now() - this.lastActivityAt < s.focusDetectionIdleSeconds * 1e3;
  }
  /**
   * @param countsAsInput true for keyboard/touch (resets the nudge idle
   *                      timer); false for scroll/pointer-move.
   */
  onActivity(countsAsInput) {
    this.lastActivityAt = Date.now();
    const s = this.ctx.settings.settings.timer;
    if (countsAsInput || !s.nudgeIgnoreScroll) {
      this.lastInputActivityAt = Date.now();
      this.nudge.noteInputActivity(this.lastInputActivityAt);
    }
    this.widget.poke();
  }
  flushReadingTime() {
    if (!this.ctx.settings.settings.general.statsEnabled) {
      this.statsTracker.resetWindow();
      return;
    }
    const accrued = this.statsTracker.accrue(
      this.windowFocused && !document.hidden,
      !this.ctx.settings.settings.timer.focusDetectionEnabled || Date.now() - this.lastActivityAt < this.ctx.settings.settings.timer.focusDetectionIdleSeconds * 1e3
    );
    if (accrued > 0) {
      void this.ctx.settings.setExtra(STATS_KEY, this.stats, false);
    }
    if (this.ctx.settings.settings.timer.dopamineEnabled) {
      this.goalBar.render(
        this.statsTracker.todayMinutes(),
        this.ctx.settings.settings.timer.dopamineDailyGoalMinutes
      );
    }
  }
  handleControl(action) {
    switch (action) {
      case "start":
        this.startWork();
        break;
      case "pause":
        this.timer.togglePauseResume();
        break;
      case "addtime":
        if (this.timer.addTime(3e4)) this.notify("Added 30s");
        break;
      case "stop":
        if (this.timer.phase !== "idle") {
          this.timer.stop();
          this.notify("Timer stopped.");
        }
        break;
    }
  }
  onTimerSnapshot(snap) {
    this.widget.render(snap);
  }
  onWorkComplete(focusMs) {
    this.statsTracker.recordSession(focusMs);
    void this.ctx.settings.setExtra(STATS_KEY, this.stats, true);
    this.notify("Focus session complete! Take a break.");
    this.timer.startBreak();
  }
  /** Exposed for the settings dashboard. */
  get todayStats() {
    return this.stats;
  }
  get statsTrackerRef() {
    return this.statsTracker;
  }
};

// focus-read-suite/src/modules/focus/ReadingFocusModule.ts
var import_obsidian3 = require("obsidian");

// focus-read-suite/src/modules/focus/ReadingRuler.ts
var import_obsidian2 = require("obsidian");
var RULER_ID = "frs-ruler";
var RULER_BODY_CLASS = "frs-focus-on";
var DEFAULT_POSITION_RATIO = 0.4;
var ReadingRuler = class {
  constructor(host) {
    this.el = null;
    this.notch = null;
    this.badge = null;
    /** Current top of the band, in px. */
    this.topPx = 0;
    this.dragging = false;
    this.dragPointerId = null;
    this.dragStartPointerY = 0;
    this.dragStartTopPx = 0;
    this.dragMoved = false;
    /** Double-tap detection (dblclick is unreliable on touch). */
    this.lastNotchTapAt = 0;
    this.lastNotchTapX = 0;
    this.lastNotchTapY = 0;
    /** Follow mode state. */
    this.followTargetPx = null;
    this.followRafId = null;
    this.scheduleApply = createRafScheduler();
    this.host = host;
  }
  /* ------------------------------------------------------------------ */
  /* Lifecycle                                                           */
  /* ------------------------------------------------------------------ */
  mount() {
    if (this.el) return;
    const el = document.createElement("div");
    el.id = RULER_ID;
    el.className = "frs-ruler";
    el.setAttribute("aria-hidden", "false");
    const band = document.createElement("div");
    band.className = "frs-ruler-band";
    el.appendChild(band);
    const focusLine = document.createElement("div");
    focusLine.className = "frs-ruler-focus-line";
    el.appendChild(focusLine);
    const notch = document.createElement("div");
    notch.className = "frs-notch";
    notch.setAttribute("role", "slider");
    notch.setAttribute("aria-label", "Reading ruler position \u2014 drag to move, double-tap to center");
    notch.setAttribute("aria-orientation", "vertical");
    notch.tabIndex = 0;
    const icon = document.createElement("span");
    icon.className = "frs-notch-icon";
    icon.textContent = "\u283F";
    notch.appendChild(icon);
    el.appendChild(notch);
    this.notch = notch;
    const badge = document.createElement("div");
    badge.className = "frs-ruler-badge";
    badge.textContent = "40%";
    el.appendChild(badge);
    this.badge = badge;
    document.body.appendChild(el);
    this.el = el;
    this.bindPointerEvents();
    this.applyConfig();
    this.applyPosition();
    this.applyVisibility();
  }
  destroy() {
    var _a;
    this.stopFollowLoop();
    (_a = this.el) == null ? void 0 : _a.remove();
    this.el = null;
    this.notch = null;
    this.badge = null;
  }
  /* ------------------------------------------------------------------ */
  /* Configuration                                                       */
  /* ------------------------------------------------------------------ */
  /** Applies height/color/opacity/notch/focus-line config; re-clamps. */
  applyConfig() {
    if (!this.el) return;
    const { ruler, focus } = this.currentSettings();
    this.el.style.setProperty("--frs-ruler-height", `${ruler.height}px`);
    this.el.style.setProperty("--frs-ruler-color", ruler.color);
    this.el.style.setProperty("--frs-ruler-opacity", String(ruler.opacity));
    this.el.style.setProperty("--frs-notch-size", `${focus.notchSize}px`);
    this.el.classList.toggle("frs-ruler-with-focus-line", focus.focusLine);
    if (this.notch) {
      this.notch.style.display = focus.showNotch ? "" : "none";
    }
    this.applyPosition();
    this.updateAria();
  }
  applyVisibility() {
    const { focus } = this.currentSettings();
    document.body.classList.toggle(RULER_BODY_CLASS, focus.enabled);
    if (focus.enabled && !this.el) {
      this.mount();
      return;
    }
    if (focus.enabled) this.applyPosition();
    else this.stopFollowLoop();
  }
  /* ------------------------------------------------------------------ */
  /* Positioning                                                         */
  /* ------------------------------------------------------------------ */
  currentSettings() {
    return { focus: this.host.getFocusSettings(), ruler: this.host.getRulerSettings() };
  }
  /** Effective mode after resolving "auto" for this device. */
  get effectiveMode() {
    const { mode } = this.currentSettings().ruler;
    if (mode === "follow" || mode === "manual") return mode;
    return hasHoverPointer() && !import_obsidian2.Platform.isMobile ? "follow" : "manual";
  }
  /** Movable vertical range for the current viewport and ruler height. */
  movableRange() {
    const { height } = getViewportSize();
    const rulerHeight = this.currentSettings().ruler.height;
    return Math.max(0, height - rulerHeight);
  }
  /** Restores the persisted ratio (or default) and clamps it. */
  ratioToPx(ratio) {
    const range = this.movableRange();
    if (range <= 0) return 0;
    const r = ratio === null ? DEFAULT_POSITION_RATIO : Math.min(Math.max(ratio, 0), 1);
    return r * range;
  }
  pxToRatio(px) {
    const range = this.movableRange();
    if (range <= 0) return 0.5;
    return Math.min(Math.max(px / range, 0), 1);
  }
  /**
   * Re-applies the saved position, clamped to the current viewport.
   * Called on mount, resize, orientation change and config changes.
   */
  applyPosition() {
    if (!this.el || this.dragging) return;
    const { positionRatio } = this.currentSettings().ruler;
    this.topPx = this.ratioToPx(positionRatio);
    this.el.style.transform = `translate3d(0, ${Math.round(this.topPx)}px, 0)`;
    this.updateAria();
  }
  /** Moves the ruler to an absolute viewport Y, clamped. */
  moveToPx(px, options = {}) {
    const range = this.movableRange();
    this.topPx = Math.min(Math.max(px, 0), range);
    if (this.el) {
      this.el.style.transform = `translate3d(0, ${Math.round(this.topPx)}px, 0)`;
    }
    if (options.persist) {
      const ratio = this.pxToRatio(this.topPx);
      void this.host.saveRulerSettings((draft) => {
        draft.ruler.positionRatio = ratio;
      });
    }
    this.updateBadge();
    this.updateAria();
  }
  /** Public API for keyboard commands / notch double-tap. */
  center() {
    this.moveToPx(this.movableRange() / 2, { persist: true });
  }
  nudge(direction) {
    const stepPercent = this.currentSettings().focus.keyboardStepPercent;
    const range = this.movableRange();
    this.moveToPx(this.topPx + direction * range * (stepPercent / 100), { persist: true });
  }
  updateAria() {
    if (!this.notch) return;
    const range = this.movableRange();
    const pct = range > 0 ? Math.round(this.topPx / range * 100) : 0;
    this.notch.setAttribute("aria-valuenow", String(pct));
    this.notch.setAttribute("aria-valuetext", `${pct}% of the screen height`);
  }
  /** Shows the live position badge (dragging feedback). */
  updateBadge() {
    if (!this.badge) return;
    const range = this.movableRange();
    const pct = range > 0 ? Math.round(this.topPx / range * 100) : 0;
    this.badge.textContent = `${pct}%`;
    this.badge.classList.toggle("frs-visible", this.dragging);
  }
  /* ------------------------------------------------------------------ */
  /* Pointer handling                                                    */
  /* ------------------------------------------------------------------ */
  bindPointerEvents() {
    if (!this.el || !this.notch) return;
    const register = this.host.registerDomEvent;
    register(this.notch, "pointerdown", (e) => {
      var _a, _b;
      if (e.button !== 0) return;
      this.dragging = true;
      this.dragMoved = false;
      this.dragPointerId = e.pointerId;
      this.dragStartPointerY = e.clientY;
      this.dragStartTopPx = this.topPx;
      (_a = this.el) == null ? void 0 : _a.classList.add("frs-ruler-dragging");
      document.body.classList.add("frs-ruler-drag-global");
      try {
        (_b = this.notch) == null ? void 0 : _b.setPointerCapture(e.pointerId);
      } catch (e2) {
      }
      e.preventDefault();
      e.stopPropagation();
    });
    register(this.notch, "pointermove", (e) => {
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      const delta = e.clientY - this.dragStartPointerY;
      if (Math.abs(delta) > 2) this.dragMoved = true;
      this.moveToPx(this.dragStartTopPx + delta);
      e.preventDefault();
    });
    const endDrag = (e) => {
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      this.finishDrag(e.pointerId);
    };
    register(this.notch, "pointerup", endDrag);
    register(this.notch, "pointercancel", endDrag);
    register(this.notch, "lostpointercapture", (e) => {
      if (this.dragging && e.pointerId === this.dragPointerId) {
        this.finishDrag(e.pointerId);
      }
    });
    register(this.notch, "contextmenu", (e) => {
      if (this.dragging) e.preventDefault();
    });
    register(this.notch, "dblclick", () => this.center());
    register(this.notch, "pointerup", (e) => {
      if (e.pointerType === "touch") this.maybeDoubleTap(e);
    });
    register(this.notch, "keydown", (e) => {
      if (e.key === "ArrowUp" || e.key === "ArrowDown") {
        e.preventDefault();
        this.nudge(e.key === "ArrowUp" ? -1 : 1);
      } else if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.center();
      }
    });
    register(window, "pointermove", (e) => {
      const { focus, ruler } = this.currentSettings();
      if (!focus.enabled) return;
      if (this.effectiveMode !== "follow") return;
      if (this.dragging) return;
      if (e.pointerType === "touch") return;
      const targetY = e.clientY - ruler.height / 2;
      if (focus.smoothFollow) {
        this.followTargetPx = targetY;
        this.startFollowLoop();
      } else {
        this.scheduleApply(() => this.moveToPx(targetY));
      }
    });
    registerViewportChangeHandlers(
      (target, type, cb) => register(target, type, cb),
      () => this.applyPosition()
    );
  }
  finishDrag(pointerId) {
    var _a, _b;
    this.dragging = false;
    this.dragPointerId = null;
    (_a = this.el) == null ? void 0 : _a.classList.remove("frs-ruler-dragging");
    document.body.classList.remove("frs-ruler-drag-global");
    try {
      (_b = this.notch) == null ? void 0 : _b.releasePointerCapture(pointerId);
    } catch (e) {
    }
    this.moveToPx(this.topPx, { persist: true });
    this.updateBadge();
  }
  /** Manual double-tap detection on the notch. */
  maybeDoubleTap(e) {
    if (this.dragMoved) return;
    const now = Date.now();
    const isDoubleTap = now - this.lastNotchTapAt < 320 && Math.abs(e.clientX - this.lastNotchTapX) < 30 && Math.abs(e.clientY - this.lastNotchTapY) < 30;
    this.lastNotchTapAt = now;
    this.lastNotchTapX = e.clientX;
    this.lastNotchTapY = e.clientY;
    if (isDoubleTap) {
      this.lastNotchTapAt = 0;
      this.center();
    }
  }
  /* ------------------------------------------------------------------ */
  /* Smooth follow                                                       */
  /* ------------------------------------------------------------------ */
  /**
   * Interpolates toward the follow target each frame (factor 0.25 ≈ smooth
   * but responsive). The loop stops itself once it converges, so no rAF
   * churn while reading without moving the mouse.
   */
  startFollowLoop() {
    if (this.followRafId !== null) return;
    const step = () => {
      this.followRafId = null;
      if (this.followTargetPx === null || this.dragging) return;
      const diff = this.followTargetPx - this.topPx;
      if (Math.abs(diff) < 0.5) {
        this.moveToPx(this.followTargetPx);
        return;
      }
      this.moveToPx(this.topPx + diff * 0.25);
      this.followRafId = requestAnimationFrame(step);
    };
    this.followRafId = requestAnimationFrame(step);
  }
  stopFollowLoop() {
    if (this.followRafId !== null) {
      cancelAnimationFrame(this.followRafId);
      this.followRafId = null;
    }
    this.followTargetPx = null;
  }
};

// focus-read-suite/src/modules/focus/ReadingFocusModule.ts
var ReadingFocusModule = class {
  constructor() {
    this.id = "focus";
    this.name = "Notch & Reading Focus";
  }
  async load(ctx) {
    this.ctx = ctx;
    this.ruler = new ReadingRuler({
      getFocusSettings: () => ctx.settings.settings.focus,
      getRulerSettings: () => ctx.settings.settings.ruler,
      saveRulerSettings: (mutate) => ctx.settings.update(["focus", "ruler"], (draft) => mutate(draft), false),
      registerDomEvent: (el, type, cb, options) => ctx.lifecycle.domEvent(el, type, cb, options)
    });
    if (ctx.settings.settings.focus.enabled) {
      this.ruler.mount();
    }
    this.registerCommands(ctx);
    logger.debug("Reading Focus module loaded.");
  }
  async unload() {
    var _a;
    (_a = this.ruler) == null ? void 0 : _a.destroy();
    document.body.classList.remove(RULER_BODY_CLASS);
    logger.debug("Reading Focus module unloaded.");
  }
  sections() {
    return ["focus", "ruler"];
  }
  onSettingsChanged(sections) {
    if (!sections.includes("focus") && !sections.includes("ruler")) return;
    this.ruler.applyVisibility();
    this.ruler.applyConfig();
  }
  /* ------------------------------------------------------------------ */
  /* Commands                                                            */
  /* ------------------------------------------------------------------ */
  async toggle() {
    const enabled = !this.ctx.settings.settings.focus.enabled;
    await this.ctx.settings.update("focus", (draft) => {
      draft.focus.enabled = enabled;
    });
    this.ruler.applyVisibility();
    if (this.ctx.settings.settings.general.showNotices) {
      new import_obsidian3.Notice(`Reading focus: ${enabled ? "ON" : "OFF"}`);
    }
  }
  center() {
    this.ensureVisible();
    this.ruler.center();
  }
  nudgeUp() {
    this.ensureVisible();
    this.ruler.nudge(-1);
  }
  nudgeDown() {
    this.ensureVisible();
    this.ruler.nudge(1);
  }
  ensureVisible() {
    if (!this.ctx.settings.settings.focus.enabled) {
      void this.ctx.settings.update("focus", (draft) => {
        draft.focus.enabled = true;
      });
    }
    this.ruler.applyVisibility();
  }
  registerCommands(ctx) {
    ctx.addCommand({
      id: "toggle-reading-focus",
      name: "Toggle reading focus (ruler)",
      callback: () => void this.toggle()
    });
    ctx.addCommand({
      id: "center-reading-ruler",
      name: "Center reading ruler",
      callback: () => this.center()
    });
    ctx.addCommand({
      id: "move-reading-ruler-up",
      name: "Move reading ruler up",
      callback: () => this.nudgeUp()
    });
    ctx.addCommand({
      id: "move-reading-ruler-down",
      name: "Move reading ruler down",
      callback: () => this.nudgeDown()
    });
  }
};

// focus-read-suite/src/modules/typography/TypographyModule.ts
var import_obsidian4 = require("obsidian");

// focus-read-suite/src/modules/typography/TypographyController.ts
var TYPOGRAPHY_BODY_CLASS = "frs-typography-on";
var GOOGLE_FONTS_LINK_ID = "frs-google-fonts-link";
var ROOT_VARS = [
  "--frs-font-size",
  "--frs-line-height",
  "--frs-para-spacing",
  "--frs-max-width",
  "--frs-font-family"
];
var TypographyController = class {
  constructor(getSettings) {
    this.getSettings = getSettings;
  }
  /** Writes current typography settings into CSS variables + body class. */
  apply() {
    const s = this.getSettings();
    const rootStyle = document.documentElement.style;
    rootStyle.setProperty("--frs-font-size", `${s.fontSize}px`);
    rootStyle.setProperty("--frs-line-height", String(s.lineHeight));
    rootStyle.setProperty("--frs-para-spacing", String(s.paragraphSpacing));
    rootStyle.setProperty("--frs-max-width", `${s.maxWidthChars}ch`);
    rootStyle.setProperty("--frs-font-family", resolveFontStack(s) || "inherit");
    document.body.classList.toggle(TYPOGRAPHY_BODY_CLASS, s.enabled);
  }
  /** Manages the Google Fonts <link> (only the selected family). */
  applyGoogleFonts() {
    var _a;
    const s = this.getSettings();
    let link = document.getElementById(GOOGLE_FONTS_LINK_ID);
    const option = fontOptionById(s.fontFamily);
    const googleFamily = (_a = option == null ? void 0 : option.googleFamily) != null ? _a : null;
    if (!s.loadGoogleFonts || !googleFamily || !s.enabled) {
      link == null ? void 0 : link.remove();
      return;
    }
    const href = `https://fonts.googleapis.com/css2?family=${googleFamily}&display=swap`;
    if (!link) {
      link = document.createElement("link");
      link.id = GOOGLE_FONTS_LINK_ID;
      link.rel = "stylesheet";
      document.head.appendChild(link);
    }
    if (link.getAttribute("href") !== href) link.href = href;
  }
  /** Removes every trace this controller left on the DOM. */
  destroy() {
    var _a;
    (_a = document.getElementById(GOOGLE_FONTS_LINK_ID)) == null ? void 0 : _a.remove();
    document.body.classList.remove(TYPOGRAPHY_BODY_CLASS);
    const rootStyle = document.documentElement.style;
    for (const prop of ROOT_VARS) {
      rootStyle.removeProperty(prop);
    }
  }
};

// focus-read-suite/src/modules/typography/TypographyModule.ts
var TypographyModule = class {
  constructor() {
    this.id = "typography";
    this.name = "Typography";
  }
  async load(ctx) {
    this.ctx = ctx;
    this.controller = new TypographyController(() => ctx.settings.settings.typography);
    this.controller.apply();
    this.controller.applyGoogleFonts();
    this.registerCommands(ctx);
    logger.debug("Typography module loaded.");
  }
  async unload() {
    var _a;
    (_a = this.controller) == null ? void 0 : _a.destroy();
    document.body.classList.remove(TYPOGRAPHY_BODY_CLASS);
    logger.debug("Typography module unloaded.");
  }
  sections() {
    return ["typography"];
  }
  onSettingsChanged(sections) {
    if (!sections.includes("typography")) return;
    this.controller.apply();
    this.controller.applyGoogleFonts();
  }
  /* ------------------------------------------------------------------ */
  /* Commands                                                            */
  /* ------------------------------------------------------------------ */
  async toggle() {
    const enabled = !this.ctx.settings.settings.typography.enabled;
    await this.ctx.settings.update("typography", (draft) => {
      draft.typography.enabled = enabled;
    });
    if (this.ctx.settings.settings.general.showNotices) {
      new import_obsidian4.Notice(`Typography: ${enabled ? "ON" : "OFF"}`);
    }
  }
  registerCommands(ctx) {
    ctx.addCommand({
      id: "toggle-typography",
      name: "Toggle reading typography",
      callback: () => void this.toggle()
    });
  }
};

// focus-read-suite/src/modules/heatmap/HeatmapModule.ts
var import_obsidian5 = require("obsidian");

// focus-read-suite/src/modules/heatmap/storage.ts
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
var _HeatmapDatabase = class _HeatmapDatabase {
  constructor(host, getSettings) {
    this.records = {};
    this.lastSaveAt = 0;
    this.dirty = false;
    this.host = host;
    this.getSettings = getSettings;
  }
  async load() {
    try {
      const raw = await this.host.loadRecords();
      if (raw) {
        this.records = raw;
        for (const path of Object.keys(this.records)) {
          this.records[path] = this.normalizeRecord(this.records[path], this.getSettings().bucketCount);
        }
        logger.info(`Heatmap database loaded (${Object.keys(this.records).length} notes).`);
      } else {
        logger.info("No heatmap database found \u2014 starting fresh.");
      }
    } catch (err) {
      logger.error("Failed to load heatmap database.", err);
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
      await this.host.saveRecords(this.records);
      this.lastSaveAt = now;
      this.dirty = false;
    } catch (err) {
      logger.error("Failed to save heatmap database.", err);
    }
  }
  /** Read-only lookup — returns undefined when nothing was recorded yet. */
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
        buckets: Array(this.getSettings().bucketCount).fill(0),
        bucketVisits: Array(this.getSettings().bucketCount).fill(0)
      };
    } else {
      this.records[path] = this.normalizeRecord(this.records[path], this.getSettings().bucketCount);
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
      logger.info(`Cleared heatmap data for: ${path}`);
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

// focus-read-suite/src/modules/heatmap/activity.ts
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
    logger.debug("ActivityMonitor listeners registered.");
  }
  recordActivity() {
    this.lastActivityAt = Date.now();
  }
  isUserActive(now = Date.now()) {
    if (typeof document !== "undefined" && document.hidden) return false;
    return now - this.lastActivityAt < this.idleThresholdMs;
  }
};

// focus-read-suite/src/modules/heatmap/renderer.ts
var TOUCH_BODY_CLASS = "frs-touch-device";
var HEATMAP_TOOLTIP_ID = "frs-heatmap-tooltip";
var HeatmapRenderer = class {
  constructor(view, database, getSettings, registerDomElement) {
    this.registerDomElement = registerDomElement;
    this.container = null;
    this.canvas = null;
    this.ctx = null;
    this.tooltip = null;
    this.scrollerElement = null;
    this.resizeObserver = null;
    this.animationFrameId = null;
    /** Original inline position of contentEl (restored on destroy). */
    this.originalContentElPosition = null;
    this.view = view;
    this.database = database;
    this.getSettings = getSettings;
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
    logger.debug("Active scroller changed (e.g. mode toggle). Rebinding listeners.");
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
    this.container.className = "frs-heatmap-wrapper";
    const settings = this.getSettings();
    this.container.style.width = `${settings.width}px`;
    this.container.style.right = `${settings.offsetRight}px`;
    this.container.style.opacity = `${settings.opacity}`;
    this.canvas = document.createElement("canvas");
    this.canvas.className = "frs-heatmap-canvas";
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext("2d");
    contentEl.appendChild(this.container);
    logger.debug("Created heatmap container.");
    let tooltip = document.getElementById(HEATMAP_TOOLTIP_ID);
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.id = HEATMAP_TOOLTIP_ID;
      tooltip.className = "frs-heatmap-tooltip";
      document.body.appendChild(tooltip);
    }
    this.tooltip = tooltip;
  }
  /* ------------------------------------------------------------------ */
  /* Events                                                              */
  /* ------------------------------------------------------------------ */
  bindEvents() {
    if (!this.scrollerElement) return;
    this.registerDomElement(this.scrollerElement, "scroll", () => {
      this.hideTooltip();
      this.draw();
    }, { passive: true });
    this.resizeObserver = new ResizeObserver(() => this.resizeCanvas());
    this.resizeObserver.observe(this.scrollerElement);
    if (this.canvas) {
      this.registerDomElement(this.canvas, "pointermove", (e) => this.handlePointerMove(e));
      this.registerDomElement(this.canvas, "pointerleave", () => this.hideTooltip());
      this.registerDomElement(this.canvas, "pointerdown", (e) => e.preventDefault());
    }
  }
  unbindEvents() {
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
      this.container.style.width = `${settings.width}px`;
      this.container.style.right = `${settings.offsetRight}px`;
      this.container.style.opacity = `${settings.opacity}`;
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
    const path = this.view.file ? this.view.file.path : null;
    if (!path) return;
    const record = this.database.getRecord(path);
    const accent = this.accentColorFactory();
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
      ctx.strokeStyle = accent(0.55);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(0, yStart);
      ctx.lineTo(clientWidth, yStart);
      ctx.moveTo(0, yEnd);
      ctx.lineTo(clientWidth, yEnd);
      ctx.stroke();
    }
    if (!record) return;
    const buckets = record.buckets;
    const bucketCount = buckets.length;
    if (bucketCount === 0) return;
    const maxVal = Math.max(...buckets, 1);
    const itemHeight = clientHeight / bucketCount;
    for (let i = 0; i < bucketCount; i++) {
      const weight = buckets[i] / maxVal;
      if (weight <= 0) continue;
      const y = (i + 0.5) * itemHeight;
      const barH = Math.max(1, itemHeight * 0.55);
      ctx.fillStyle = accent(0.08 + weight * weight * 0.5);
      ctx.fillRect(1, y - barH / 2, (clientWidth - 2) * weight, barH);
    }
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
        <div class="frs-heatmap-tooltip-title">Section ~${Math.round(pct * 100)}%</div>
        <div class="frs-heatmap-tooltip-row"><span>No reading data yet</span></div>`;
      this.positionTooltip(e);
      return;
    }
    const bucketCount = record.buckets.length;
    const bucketIdx = Math.min(bucketCount - 1, Math.floor(pct * bucketCount));
    const ms = record.buckets[bucketIdx] || 0;
    const visits = record.bucketVisits[bucketIdx] || 0;
    const readBuckets = record.buckets.filter((v) => v > 0).length;
    const coverage = bucketCount > 0 ? Math.round(readBuckets / bucketCount * 100) : 0;
    const totalSeconds = Math.round(ms / 1e3);
    const minStr = Math.floor(totalSeconds / 60);
    const secStr = String(totalSeconds % 60).padStart(2, "0");
    this.tooltip.innerHTML = `
      <div class="frs-heatmap-tooltip-title">Section ~${Math.round(pct * 100)}%</div>
      <div class="frs-heatmap-tooltip-row">
        <span>Time spent</span>
        <span class="frs-heatmap-tooltip-value">${minStr}m ${secStr}s</span>
      </div>
      <div class="frs-heatmap-tooltip-row">
        <span>Visits</span>
        <span class="frs-heatmap-tooltip-value">${visits}</span>
      </div>
      <div class="frs-heatmap-tooltip-row">
        <span>Note coverage</span>
        <span class="frs-heatmap-tooltip-value">${coverage}%</span>
      </div>`;
    this.positionTooltip(e);
  }
  positionTooltip(e) {
    if (!this.tooltip) return;
    const tooltipWidth = this.tooltip.offsetWidth || 150;
    const xPos = e.clientX - tooltipWidth - 15;
    const yPos = Math.max(10, Math.min(window.innerHeight - 110, e.clientY - 30));
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
    logger.debug("Heatmap renderer destroyed.");
  }
};

// focus-read-suite/src/modules/heatmap/engine.ts
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
  /** Restarts the tracking loop after the interval setting changed. */
  restart() {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.start();
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

// focus-read-suite/src/modules/heatmap/HeatmapModule.ts
var RECORDS_KEY = "heatmapRecords";
var HeatmapModule = class {
  constructor() {
    this.id = "heatmap";
    this.name = "Heat Map of Notes";
    /** Last-seen bucket count — detects resample-needing changes. */
    this.lastBucketCount = 0;
  }
  async load(ctx) {
    this.ctx = ctx;
    const { settings, lifecycle } = ctx;
    const getSettings = () => settings.settings.heatmap;
    this.database = new HeatmapDatabase(
      {
        loadRecords: async () => settings.getExtra(RECORDS_KEY),
        saveRecords: async (records) => {
          await settings.setExtra(RECORDS_KEY, records, false);
        }
      },
      getSettings
    );
    await this.database.load();
    this.activityMonitor = new ActivityMonitor(
      (el, type, cb, options) => lifecycle.domEvent(el, type, cb, options),
      getSettings().idleSeconds
    );
    this.activityMonitor.start();
    this.engine = new HeatmapEngine(
      {
        registerInterval: (id) => lifecycle.interval(id),
        iterateMarkdownViews: (cb) => ctx.app.workspace.iterateAllLeaves((leaf) => {
          if (leaf.view instanceof import_obsidian5.MarkdownView) cb(leaf.view);
        }),
        registerDomElement: (el, type, cb, options) => lifecycle.domEvent(el, type, cb, options)
      },
      this.database,
      this.activityMonitor,
      () => ({ ...getSettings(), refreshIntervalMs: ctx.settings.settings.advanced.refreshIntervalMs })
    );
    if (!hasHoverPointer()) {
      document.body.classList.add(TOUCH_BODY_CLASS);
      lifecycle.onUnload(() => document.body.classList.remove(TOUCH_BODY_CLASS));
    }
    lifecycle.event(
      ctx.app.workspace.on("layout-change", () => {
        if (ctx.settings.settings.heatmap.enabled) this.engine.syncOpenViews();
      })
    );
    lifecycle.event(
      ctx.app.workspace.on("active-leaf-change", () => {
        if (ctx.settings.settings.heatmap.enabled) this.engine.syncOpenViews();
      })
    );
    lifecycle.event(
      ctx.app.vault.on("rename", (file, oldPath) => {
        this.database.handleRename(oldPath, file.path);
      })
    );
    if (ctx.settings.settings.heatmap.enabled) {
      this.startEngine();
    }
    this.lastBucketCount = ctx.settings.settings.heatmap.bucketCount;
    this.registerCommands(ctx);
    logger.debug("Heatmap module loaded.");
  }
  async unload() {
    var _a, _b, _c;
    (_a = this.engine) == null ? void 0 : _a.stop();
    await ((_b = this.database) == null ? void 0 : _b.save(true));
    (_c = document.getElementById(HEATMAP_TOOLTIP_ID)) == null ? void 0 : _c.remove();
    document.body.classList.remove(TOUCH_BODY_CLASS);
    logger.debug("Heatmap module unloaded.");
  }
  sections() {
    return ["heatmap", "advanced"];
  }
  onSettingsChanged(sections) {
    const s = this.ctx.settings.settings;
    if (sections.includes("heatmap")) {
      this.activityMonitor.setIdleThreshold(s.heatmap.idleSeconds);
      if (s.heatmap.bucketCount !== this.lastBucketCount) {
        this.lastBucketCount = s.heatmap.bucketCount;
        this.database.resizeAllRecords(s.heatmap.bucketCount);
        if (s.heatmap.enabled) this.engine.rebuildRenderers();
      }
      if (s.heatmap.enabled) {
        this.startEngine();
        this.engine.applySettingsToRenderers();
      } else {
        this.engine.stop();
      }
    }
    if (sections.includes("advanced")) {
      if (s.heatmap.enabled) this.engine.restart();
    }
  }
  /* ------------------------------------------------------------------ */
  /* Engine control                                                      */
  /* ------------------------------------------------------------------ */
  startEngine() {
    const layoutReady = this.ctx.app.workspace.layoutReady;
    const begin = () => {
      this.engine.start();
      this.engine.syncOpenViews();
    };
    if (layoutReady) begin();
    else this.ctx.app.workspace.onLayoutReady(() => begin());
  }
  /* ------------------------------------------------------------------ */
  /* Public API (commands + settings tools)                              */
  /* ------------------------------------------------------------------ */
  clearCurrentNote() {
    const activeView = this.ctx.app.workspace.getActiveViewOfType(import_obsidian5.MarkdownView);
    if (activeView && activeView.file) {
      this.database.clearRecord(activeView.file.path);
      if (this.ctx.settings.settings.heatmap.enabled) this.engine.rebuildRenderers();
      new import_obsidian5.Notice(`Cleared reading analytics for ${activeView.file.name}`);
    } else {
      new import_obsidian5.Notice("No active note found to clear.");
    }
  }
  pruneDeleted() {
    return this.database.pruneDeleted(
      (path) => this.ctx.app.vault.getAbstractFileByPath(path) !== null
    );
  }
  clearAll() {
    this.database.clearAll();
    if (this.ctx.settings.settings.heatmap.enabled) this.engine.rebuildRenderers();
  }
  rebuildRenderers() {
    if (this.ctx.settings.settings.heatmap.enabled) this.engine.rebuildRenderers();
  }
  get recordCount() {
    return Object.keys(this.database.records).length;
  }
  getRecord(path) {
    return this.database.getRecord(path);
  }
  get isTracking() {
    return this.activityMonitor.isUserActive();
  }
  registerCommands(ctx) {
    ctx.addCommand({
      id: "clear-note-heatmap",
      name: "Clear heatmap analytics for current note",
      callback: () => this.clearCurrentNote()
    });
  }
};

// focus-read-suite/src/ui/settings-tab.ts
var import_obsidian7 = require("obsidian");

// focus-read-suite/src/ui/components.ts
var import_obsidian6 = require("obsidian");
function formatSliderValue(value, decimals = 0, unit = "") {
  return `${value.toFixed(decimals)}${unit}`;
}
function labeledSlider(containerEl, opts) {
  var _a, _b;
  const setting = new import_obsidian6.Setting(containerEl).setName(opts.name);
  if (opts.desc) setting.setDesc(opts.desc);
  const badge = document.createElement("span");
  badge.className = "frs-setting-value";
  badge.textContent = formatSliderValue(opts.value, (_a = opts.decimals) != null ? _a : 0, (_b = opts.unit) != null ? _b : "");
  setting.nameEl.appendChild(badge);
  setting.addSlider(
    (slider) => slider.setLimits(opts.min, opts.max, opts.step).setValue(opts.value).setDynamicTooltip().onChange(async (v) => {
      var _a2, _b2;
      badge.textContent = formatSliderValue(v, (_a2 = opts.decimals) != null ? _a2 : 0, (_b2 = opts.unit) != null ? _b2 : "");
      await opts.onChange(v);
    })
  );
  return setting;
}
function sectionHeader(containerEl, title, subtitle, onReset) {
  const wrap = containerEl.createDiv({ cls: "frs-settings-section-head" });
  const titles = wrap.createDiv({ cls: "frs-settings-section-titles" });
  titles.createEl("h3", { text: title });
  if (subtitle) {
    titles.createEl("p", { text: subtitle, cls: "frs-settings-section-subtitle" });
  }
  if (onReset) {
    const resetBtn = wrap.createEl("button", {
      text: "Reset",
      cls: "frs-chip frs-chip-action"
    });
    resetBtn.setAttribute("aria-label", `Reset ${title} to defaults`);
    resetBtn.addEventListener("click", () => void onReset());
  }
  return wrap;
}
function statusPill(containerEl, label, active) {
  const pill = containerEl.createSpan({ cls: `frs-pill ${active ? "frs-pill-on" : "frs-pill-off"}` });
  pill.createSpan({ cls: "frs-pill-dot", text: "" });
  pill.createSpan({ text: label });
  return pill;
}
function callout(containerEl, text, variant = "info") {
  return containerEl.createDiv({ cls: `frs-callout frs-callout-${variant}`, text });
}

// focus-read-suite/src/ui/settings-tab.ts
var RULER_MODE_OPTIONS = {
  auto: "Auto \u2014 follow on desktop, drag on touch",
  follow: "Follow pointer (desktop)",
  manual: "Manual \u2014 drag the notch"
};
var ACCENT_MODE_OPTIONS = {
  native: "Native \u2014 use Obsidian's accent color",
  custom: "Custom accent color"
};
var ConfirmModal = class extends import_obsidian7.Modal {
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
    const buttonRow = this.contentEl.createDiv({ cls: "frs-modal-button-row" });
    new import_obsidian7.ButtonComponent(buttonRow).setButtonText(this.confirmLabel).setWarning().onClick(() => {
      this.close();
      void this.onConfirm();
    });
    new import_obsidian7.ButtonComponent(buttonRow).setButtonText("Cancel").onClick(() => this.close());
  }
  onClose() {
    this.contentEl.empty();
  }
};
var FocusSuiteSettingTab = class extends import_obsidian7.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.activeTab = "general";
    this.plugin = plugin;
  }
  get settings() {
    return this.plugin.settings;
  }
  display() {
    var _a;
    const { containerEl } = this;
    containerEl.empty();
    this.renderHeader(containerEl);
    const tabs = [
      { id: "general", label: "General", render: (el) => this.renderGeneral(el) },
      { id: "timer", label: "Timer", render: (el) => this.renderTimer(el) },
      { id: "focus", label: "Reading Focus", render: (el) => this.renderFocus(el) },
      { id: "typography", label: "Typography", render: (el) => this.renderTypography(el) },
      { id: "ruler", label: "Ruler", render: (el) => this.renderRuler(el) },
      { id: "heatmap", label: "Heatmap", render: (el) => this.renderHeatmap(el) },
      { id: "appearance", label: "Appearance", render: (el) => this.renderAppearance(el) },
      { id: "advanced", label: "Advanced", render: (el) => this.renderAdvanced(el) }
    ];
    const active = (_a = tabs.find((t) => t.id === this.activeTab)) != null ? _a : tabs[0];
    this.activeTab = active.id;
    const nav = containerEl.createDiv({ cls: "frs-settings-nav" });
    nav.setAttribute("role", "tablist");
    for (const tab of tabs) {
      const btn = nav.createEl("button", {
        cls: `frs-settings-tab ${tab.id === active.id ? "frs-settings-tab-active" : ""}`,
        text: tab.label
      });
      btn.setAttribute("role", "tab");
      btn.setAttribute("aria-selected", String(tab.id === active.id));
      btn.addEventListener("click", () => {
        this.activeTab = tab.id;
        this.display();
      });
    }
    const section = containerEl.createDiv({ cls: "frs-settings-section" });
    section.setAttribute("role", "tabpanel");
    active.render(section);
  }
  /* ------------------------------------------------------------------ */
  /* Header                                                              */
  /* ------------------------------------------------------------------ */
  renderHeader(el) {
    const head = el.createDiv({ cls: "frs-settings-head" });
    const title = head.createDiv({ cls: "frs-settings-head-titles" });
    title.createEl("h2", { text: "Focus Read Suite" });
    title.createEl("p", {
      text: "Timer, reading focus, typography and heatmap \u2014 one plugin.",
      cls: "frs-settings-head-sub"
    });
    const pills = head.createDiv({ cls: "frs-settings-head-pills" });
    const s = this.settings.settings;
    statusPill(pills, "Timer", s.timer.enabled);
    statusPill(pills, "Reading Focus", s.focus.enabled);
    statusPill(pills, "Typography", s.typography.enabled);
    statusPill(pills, "Heatmap", s.heatmap.enabled);
  }
  /* ------------------------------------------------------------------ */
  /* 1. General                                                          */
  /* ------------------------------------------------------------------ */
  renderGeneral(el) {
    sectionHeader(el, "General", "Plugin-wide behavior.");
    const s = this.settings.settings.general;
    new import_obsidian7.Setting(el).setName("Track reading-time statistics").setDesc("Accumulate today/total reading time, streaks and per-day history. Turn off for zero tracking.").addToggle(
      (toggle) => toggle.setValue(s.statsEnabled).onChange(async (v) => {
        await this.settings.update("general", (draft) => {
          draft.general.statsEnabled = v;
        });
      })
    );
    new import_obsidian7.Setting(el).setName("Show feedback notices").setDesc("Informational toasts (session started, ruler toggled\u2026). Errors are always shown.").addToggle(
      (toggle) => toggle.setValue(s.showNotices).onChange(async (v) => {
        await this.settings.update("general", (draft) => {
          draft.general.showNotices = v;
        });
      })
    );
    const modulesCard = el.createDiv({ cls: "frs-card" });
    modulesCard.createEl("h4", { text: "Modules" });
    modulesCard.createEl("p", { cls: "frs-card-note", text: "Enable or disable each feature set in its own settings tab:" });
    const rows = modulesCard.createDiv({ cls: "frs-module-rows" });
    const moduleRow = (name, desc, section, enabled) => {
      const row = rows.createDiv({ cls: "frs-module-row" });
      const titles = row.createDiv({ cls: "frs-module-row-titles" });
      titles.createEl("strong", { text: name });
      titles.createEl("span", { text: desc });
      const toggleSetting = new import_obsidian7.Setting(row).setClass("frs-module-row-toggle");
      toggleSetting.addToggle(
        (t) => t.setValue(enabled).onChange(async (v) => {
          await this.settings.update(section, (draft) => {
            draft[section].enabled = v;
          });
          this.display();
        })
      );
    };
    moduleRow("Focus Read Timer", "Floating timer, sessions, focus detection, goal bar", "timer", this.settings.settings.timer.enabled);
    moduleRow("Notch & Reading Focus", "The yellow ruler with its draggable notch", "focus", this.settings.settings.focus.enabled);
    moduleRow("Typography", "Reading font, size, line height and width", "typography", this.settings.settings.typography.enabled);
    moduleRow("Heat Map of Notes", "Per-note reading attention heatmap", "heatmap", this.settings.settings.heatmap.enabled);
  }
  /* ------------------------------------------------------------------ */
  /* 2. Focus Read Timer                                                 */
  /* ------------------------------------------------------------------ */
  renderTimer(el) {
    sectionHeader(el, "Focus Read Timer", "Floating timer, focus detection, idle nudge, daily goal.", async () => {
      await this.settings.resetSections(["timer"]);
      this.display();
    });
    const s = this.settings.settings.timer;
    const up = (mutate) => this.settings.update("timer", (draft) => mutate(draft.timer));
    new import_obsidian7.Setting(el).setName("Enable floating timer").setDesc("Show the floating timer box. Drag it by its header; double-click the header to collapse it.").addToggle((toggle) => toggle.setValue(s.enabled).onChange((v) => void up((d) => {
      d.enabled = v;
    })));
    labeledSlider(el, {
      name: "Work minutes",
      min: 5,
      max: 90,
      step: 1,
      value: s.workMinutes,
      unit: " min",
      onChange: (v) => up((d) => {
        d.workMinutes = v;
      })
    });
    labeledSlider(el, {
      name: "Break minutes",
      min: 1,
      max: 30,
      step: 1,
      value: s.breakMinutes,
      unit: " min",
      onChange: (v) => up((d) => {
        d.breakMinutes = v;
      })
    });
    new import_obsidian7.Setting(el).setName("Auto-hide timer").setDesc("Dim the timer box when idle.").addToggle((toggle) => toggle.setValue(s.autoHide).onChange((v) => void up((d) => {
      d.autoHide = v;
    })));
    labeledSlider(el, {
      name: "Auto-hide after",
      min: 1,
      max: 30,
      step: 1,
      value: s.autoHideSeconds,
      unit: " s",
      onChange: (v) => up((d) => {
        d.autoHideSeconds = v;
      })
    });
    new import_obsidian7.Setting(el).setName("Pause on window blur").setDesc("Pause when Obsidian loses focus or is hidden.").addToggle((toggle) => toggle.setValue(s.pauseOnBlur).onChange((v) => void up((d) => {
      d.pauseOnBlur = v;
    })));
    new import_obsidian7.Setting(el).setName("Reset timer position").setDesc("Snap the timer back to the top-right corner.").addButton(
      (button) => button.setButtonText("Reset position").onClick(async () => {
        await this.settings.update("timer", (draft) => {
          draft.timer.positionX = null;
          draft.timer.positionY = null;
        });
        this.plugin.modules.timer.resetPosition();
      })
    );
    el.createEl("h4", { text: "Focus detection", cls: "frs-subhead" });
    new import_obsidian7.Setting(el).setName("Enable focus detection").setDesc("Only accumulate focus time while you are actively reading (not just while the window is focused).").addToggle((toggle) => toggle.setValue(s.focusDetectionEnabled).onChange((v) => void up((d) => {
      d.focusDetectionEnabled = v;
    })));
    labeledSlider(el, {
      name: "Idle seconds",
      min: 10,
      max: 300,
      step: 5,
      value: s.focusDetectionIdleSeconds,
      unit: " s",
      onChange: (v) => up((d) => {
        d.focusDetectionIdleSeconds = v;
      })
    });
    el.createEl("h4", { text: "Idle nudge", cls: "frs-subhead" });
    new import_obsidian7.Setting(el).setName("Enable idle nudge").setDesc("A reminder card when you stop reading (works even without a running timer).").addToggle((toggle) => toggle.setValue(s.nudgeEnabled).onChange((v) => void up((d) => {
      d.nudgeEnabled = v;
    })));
    labeledSlider(el, {
      name: "Idle threshold",
      min: 10,
      max: 300,
      step: 5,
      value: s.nudgeIdleSeconds,
      unit: " s",
      onChange: (v) => up((d) => {
        d.nudgeIdleSeconds = v;
      })
    });
    new import_obsidian7.Setting(el).setName("Don't count scroll as activity").setDesc("Recommended ON \u2014 scrolling while reading shouldn't reset the idle timer.").addToggle((toggle) => toggle.setValue(s.nudgeIgnoreScroll).onChange((v) => void up((d) => {
      d.nudgeIgnoreScroll = v;
    })));
    el.createEl("h4", { text: "Daily goal bar", cls: "frs-subhead" });
    new import_obsidian7.Setting(el).setName("Enable daily goal bar").setDesc("Bottom bar showing today's reading vs your goal (works independently of the timer).").addToggle((toggle) => toggle.setValue(s.dopamineEnabled).onChange((v) => void up((d) => {
      d.dopamineEnabled = v;
    })));
    labeledSlider(el, {
      name: "Daily goal",
      min: 5,
      max: 240,
      step: 5,
      value: s.dopamineDailyGoalMinutes,
      unit: " min",
      onChange: (v) => up((d) => {
        d.dopamineDailyGoalMinutes = v;
      })
    });
    const stats = this.plugin.modules.timer.todayStats;
    const statsCard = el.createDiv({ cls: "frs-card" });
    statsCard.createEl("h4", { text: "Reading statistics" });
    const grid = statsCard.createDiv({ cls: "frs-stat-grid" });
    const stat = (label, value) => {
      const cell = grid.createDiv({ cls: "frs-stat-cell" });
      cell.createSpan({ text: label, cls: "frs-stat-label" });
      cell.createSpan({ text: value, cls: "frs-stat-value" });
    };
    const fmtMin = (ms) => {
      const totalMin = Math.floor(ms / 6e4);
      if (totalMin < 60) return `${totalMin} min`;
      return `${Math.floor(totalMin / 60)} h ${totalMin % 60} min`;
    };
    stat("Today", fmtMin(stats.todayMs));
    stat("All time", fmtMin(stats.totalReadingMs));
    stat("Streak", `${stats.streak} day${stats.streak === 1 ? "" : "s"}`);
    stat("Longest streak", `${stats.longestStreak} day${stats.longestStreak === 1 ? "" : "s"}`);
    stat("Sessions today", String(stats.sessionsToday));
    stat("Longest focus", fmtMin(stats.longestFocusMs));
  }
  /* ------------------------------------------------------------------ */
  /* 3. Notch & Reading Focus                                            */
  /* ------------------------------------------------------------------ */
  renderFocus(el) {
    sectionHeader(el, "Notch & Reading Focus", "How the reading-assistance system behaves and interacts.", async () => {
      await this.settings.resetSections(["focus"]);
      this.display();
    });
    const s = this.settings.settings.focus;
    const up = (mutate) => this.settings.update("focus", (draft) => mutate(draft.focus));
    new import_obsidian7.Setting(el).setName("Enable reading focus").setDesc("A horizontal highlight band (the yellow ruler) over your note, with a draggable notch on its right edge.").addToggle((toggle) => toggle.setValue(s.enabled).onChange((v) => void up((d) => {
      d.enabled = v;
    })));
    new import_obsidian7.Setting(el).setName("Show the notch").setDesc("The notch is the tab you drag to move the ruler (mouse, pen and touch). Hiding it leaves keyboard/command control.").addToggle((toggle) => toggle.setValue(s.showNotch).onChange((v) => void up((d) => {
      d.showNotch = v;
    })));
    labeledSlider(el, {
      name: "Notch size",
      min: 36,
      max: 56,
      step: 2,
      value: s.notchSize,
      unit: " px",
      desc: "Touch-target diameter. 44 px or more is comfortable on phones.",
      onChange: (v) => up((d) => {
        d.notchSize = v;
      })
    });
    new import_obsidian7.Setting(el).setName("Focus line").setDesc("Draw a crisp guide line at the band's center \u2014 helps the eyes track the current line.").addToggle((toggle) => toggle.setValue(s.focusLine).onChange((v) => void up((d) => {
      d.focusLine = v;
    })));
    new import_obsidian7.Setting(el).setName("Smooth pointer following").setDesc("In follow mode the band glides toward the pointer instead of jumping (desktop only).").addToggle((toggle) => toggle.setValue(s.smoothFollow).onChange((v) => void up((d) => {
      d.smoothFollow = v;
    })));
    labeledSlider(el, {
      name: "Keyboard move step",
      min: 2,
      max: 25,
      step: 1,
      value: s.keyboardStepPercent,
      unit: " %",
      desc: "Step size for the move-up/move-down commands and the notch's arrow keys.",
      onChange: (v) => up((d) => {
        d.keyboardStepPercent = v;
      })
    });
    callout(
      el,
      "Drag the notch to reposition the ruler. Double-tap (or double-click) the notch to center it. The notch also responds to Arrow keys when focused. On touch devices the band itself never reacts to taps \u2014 only the notch is interactive, so scrolling is never intercepted."
    );
  }
  /* ------------------------------------------------------------------ */
  /* 4. Typography                                                       */
  /* ------------------------------------------------------------------ */
  renderTypography(el) {
    sectionHeader(el, "Typography", "Reading font, size, line height, spacing and width.", async () => {
      await this.settings.resetSections(["typography"]);
      this.display();
    });
    const s = this.settings.settings.typography;
    const up = (mutate) => this.settings.update("typography", (draft) => mutate(draft.typography));
    new import_obsidian7.Setting(el).setName("Enable typography").setDesc("Apply the font and text metrics below to reading and editing views.").addToggle((toggle) => toggle.setValue(s.enabled).onChange((v) => void up((d) => {
      d.enabled = v;
    })));
    new import_obsidian7.Setting(el).setName("Reading font").setDesc("Applied on top of your theme when typography is enabled.").addDropdown((dropdown) => {
      for (const option of FONT_OPTIONS) dropdown.addOption(option.id, option.label);
      dropdown.setValue(s.fontFamily).onChange(async (v) => {
        await up((d) => {
          d.fontFamily = v;
        });
        this.display();
      });
    });
    if (s.fontFamily === "custom") {
      new import_obsidian7.Setting(el).setName("Custom font stack").setDesc("CSS font-family value, e.g. Georgia, 'Times New Roman', serif").addText(
        (text) => text.setValue(s.customFontFamily).onChange(async (v) => {
          await up((d) => {
            d.customFontFamily = v;
          });
        })
      );
    }
    new import_obsidian7.Setting(el).setName("Load Google Fonts").setDesc("Download the selected font from Google Fonts (requires internet). Only the selected family is loaded.").addToggle((toggle) => toggle.setValue(s.loadGoogleFonts).onChange((v) => void up((d) => {
      d.loadGoogleFonts = v;
    })));
    labeledSlider(el, { name: "Font size", min: 13, max: 26, step: 1, value: s.fontSize, unit: " px", onChange: (v) => up((d) => {
      d.fontSize = v;
    }) });
    labeledSlider(el, { name: "Line height", min: 1.2, max: 2.2, step: 0.05, decimals: 2, value: s.lineHeight, onChange: (v) => up((d) => {
      d.lineHeight = v;
    }) });
    labeledSlider(el, { name: "Paragraph spacing", min: 1, max: 2.5, step: 0.1, decimals: 1, value: s.paragraphSpacing, onChange: (v) => up((d) => {
      d.paragraphSpacing = v;
    }) });
    labeledSlider(el, { name: "Max line width", min: 40, max: 120, step: 1, value: s.maxWidthChars, unit: " ch", desc: "Measured in characters \u2014 keeps lines comfortably readable.", onChange: (v) => up((d) => {
      d.maxWidthChars = v;
    }) });
  }
  /* ------------------------------------------------------------------ */
  /* 5. Yellow Ruler                                                     */
  /* ------------------------------------------------------------------ */
  renderRuler(el) {
    sectionHeader(el, "Yellow Ruler", "The highlight band itself \u2014 size, color, opacity, positioning.", async () => {
      await this.settings.resetSections(["ruler"]);
      this.display();
    });
    const s = this.settings.settings.ruler;
    const up = (mutate) => this.settings.update("ruler", (draft) => mutate(draft.ruler));
    callout(el, `The ruler is part of the Reading Focus feature \u2014 enable it in the "Reading Focus" tab (currently ${this.settings.settings.focus.enabled ? "ON" : "OFF"}).`);
    labeledSlider(el, { name: "Ruler height", min: 10, max: 80, step: 1, value: s.height, unit: " px", onChange: (v) => up((d) => {
      d.height = v;
    }) });
    new import_obsidian7.Setting(el).setName("Ruler color").setDesc("The classic highlighter yellow works in light and dark themes.").addColorPicker((picker) => picker.setValue(s.color).onChange((v) => void up((d) => {
      d.color = v;
    })));
    labeledSlider(el, { name: "Ruler opacity", min: 0.05, max: 0.9, step: 0.01, decimals: 2, value: s.opacity, onChange: (v) => up((d) => {
      d.opacity = v;
    }) });
    new import_obsidian7.Setting(el).setName("Interaction mode").setDesc("Follow: the band tracks your mouse. Manual: the band stays where you drag the notch \u2014 recommended on touch. Auto picks per device.").addDropdown((dropdown) => {
      for (const [mode, label] of Object.entries(RULER_MODE_OPTIONS)) dropdown.addOption(mode, label);
      dropdown.setValue(s.mode).onChange(async (v) => {
        await up((d) => {
          d.mode = v;
        });
      });
    });
    new import_obsidian7.Setting(el).setName("Reset ruler position").setDesc("Put the ruler back at its default height (slightly above the middle).").addButton(
      (button) => button.setButtonText("Reset position").onClick(async () => {
        await up((d) => {
          d.positionRatio = null;
        });
      })
    );
    callout(el, "The position is remembered as a fraction of the screen height, so it stays sensible after rotating the device or switching monitors.");
  }
  /* ------------------------------------------------------------------ */
  /* 6. Heat Map of Notes                                                */
  /* ------------------------------------------------------------------ */
  renderHeatmap(el) {
    var _a;
    sectionHeader(el, "Heat Map of Notes", "Reading-attention tracking and the vertical heatmap strip.", async () => {
      await this.settings.resetSections(["heatmap"]);
      this.display();
    });
    const s = this.settings.settings.heatmap;
    const up = (mutate) => this.settings.update("heatmap", (draft) => mutate(draft.heatmap));
    new import_obsidian7.Setting(el).setName("Enable heatmap").setDesc("Track which parts of your notes you actually read, and show the vertical attention strip beside each note.").addToggle((toggle) => toggle.setValue(s.enabled).onChange((v) => void up((d) => {
      d.enabled = v;
    })));
    labeledSlider(el, {
      name: "Activity idle threshold",
      min: 10,
      max: 300,
      step: 5,
      value: s.idleSeconds,
      unit: " s",
      desc: "Tracking pauses after this period of inactivity.",
      onChange: (v) => up((d) => {
        d.idleSeconds = v;
      })
    });
    labeledSlider(el, {
      name: "Resolution",
      min: 20,
      max: 200,
      step: 10,
      value: s.bucketCount,
      unit: " bands",
      desc: "Density of the vertical bands. Existing data is resampled, never lost.",
      onChange: (v) => up((d) => {
        d.bucketCount = v;
      })
    });
    labeledSlider(el, { name: "Strip width", min: 8, max: 48, step: 2, value: s.width, unit: " px", onChange: (v) => up((d) => {
      d.width = v;
    }) });
    labeledSlider(el, { name: "Edge offset", min: 0, max: 50, step: 2, value: s.offsetRight, unit: " px", desc: "Spacing from the right pane border.", onChange: (v) => up((d) => {
      d.offsetRight = v;
    }) });
    labeledSlider(el, { name: "Strip opacity", min: 0.1, max: 1, step: 0.05, decimals: 2, value: s.opacity, onChange: (v) => up((d) => {
      d.opacity = v;
    }) });
    callout(el, "Desktop: hover the strip to see time spent, visits and coverage per section. Touch: the strip never intercepts scroll gestures.");
    const toolsCard = el.createDiv({ cls: "frs-card" });
    toolsCard.createEl("h4", { text: "Analytics dashboard" });
    const activeView = this.app.workspace.getActiveViewOfType(import_obsidian7.MarkdownView);
    const activeFile = (_a = activeView == null ? void 0 : activeView.file) != null ? _a : null;
    if (activeFile) {
      const rec = this.plugin.modules.heatmap.getRecord(activeFile.path);
      const grid = toolsCard.createDiv({ cls: "frs-stat-grid" });
      const stat = (label, value) => {
        const cell = grid.createDiv({ cls: "frs-stat-cell" });
        cell.createSpan({ text: label, cls: "frs-stat-label" });
        cell.createSpan({ text: value, cls: "frs-stat-value" });
      };
      if (rec) {
        const totalSec = Math.round(rec.totalTimeMs / 1e3);
        stat("Active note", activeFile.name);
        stat("Time spent", `${Math.floor(totalSec / 60)}m ${String(totalSec % 60).padStart(2, "0")}s`);
        stat("Visits", String(rec.visits || 0));
        stat("Last accessed", rec.lastAccessed ? new Date(rec.lastAccessed).toLocaleDateString() : "Unknown");
      } else {
        stat("Active note", activeFile.name);
        stat("Time spent", "No data yet");
      }
      stat("Indexed notes", `${this.plugin.modules.heatmap.recordCount}`);
    } else {
      toolsCard.createEl("p", {
        cls: "frs-card-note",
        text: "Open a note in the editor to see its reading analytics."
      });
    }
    toolsCard.createEl("h4", { text: "Maintenance", cls: "frs-subhead" });
    new import_obsidian7.Setting(toolsCard).setName("Reset current note analytics").setDesc("Permanently discard collected reading metrics for the active note.").addButton(
      (button) => button.setButtonText("Reset note").setWarning().onClick(() => {
        this.plugin.modules.heatmap.clearCurrentNote();
        this.display();
      })
    );
    new import_obsidian7.Setting(toolsCard).setName("Reset all analytics").setDesc("Delete all historical engagement records across the entire vault.").addButton(
      (button) => button.setButtonText("Reset database").setWarning().onClick(() => {
        new ConfirmModal(
          this.app,
          "Reset all reading analytics?",
          "This permanently deletes all reading engagement history for every note. This action cannot be undone.",
          "Delete everything",
          async () => {
            this.plugin.modules.heatmap.clearAll();
            new import_obsidian7.Notice("All vault reading metrics have been cleared.");
            this.display();
          }
        ).open();
      })
    );
    new import_obsidian7.Setting(toolsCard).setName("Prune records for deleted notes").setDesc("Remove analytics entries whose notes no longer exist in the vault.").addButton(
      (button) => button.setButtonText("Prune deleted").onClick(() => {
        const removed = this.plugin.modules.heatmap.pruneDeleted();
        new import_obsidian7.Notice(removed.length > 0 ? `Pruned ${removed.length} record(s).` : "Nothing to prune.");
        this.display();
      })
    );
    const diag = toolsCard.createDiv({ cls: "frs-diag-row" });
    statusPill(diag, this.plugin.modules.heatmap.isTracking ? "Tracking active" : "Idle \u2014 paused", this.plugin.modules.heatmap.isTracking);
  }
  /* ------------------------------------------------------------------ */
  /* 7. Appearance                                                       */
  /* ------------------------------------------------------------------ */
  renderAppearance(el) {
    sectionHeader(el, "Appearance", "One visual identity for every module.", async () => {
      await this.settings.resetSections(["appearance"]);
      this.display();
    });
    const s = this.settings.settings.appearance;
    const up = (mutate) => this.settings.update("appearance", (draft) => mutate(draft.appearance));
    new import_obsidian7.Setting(el).setName("Accent source").setDesc("Native follows your Obsidian theme accent; custom lets you pick the suite's own accent (notch, progress bars, heatmap).").addDropdown((dropdown) => {
      for (const [mode, label] of Object.entries(ACCENT_MODE_OPTIONS)) dropdown.addOption(mode, label);
      dropdown.setValue(s.accentMode).onChange(async (v) => {
        await up((d) => {
          d.accentMode = v;
        });
        this.display();
      });
    });
    if (s.accentMode === "custom") {
      new import_obsidian7.Setting(el).setName("Custom accent color").addColorPicker((picker) => picker.setValue(s.customAccent).onChange((v) => void up((d) => {
        d.customAccent = v;
      })));
    }
    labeledSlider(el, {
      name: "Widget scale",
      min: 0.8,
      max: 1.25,
      step: 0.05,
      decimals: 2,
      value: s.widgetScale,
      desc: "Size of the floating timer and the goal bar \u2014 handy on small phones.",
      onChange: (v) => up((d) => {
        d.widgetScale = v;
      })
    });
    callout(el, "All modules read Obsidian theme variables (backgrounds, borders, text) so they match your theme automatically; only the accent is customizable.");
  }
  /* ------------------------------------------------------------------ */
  /* 8. Advanced                                                         */
  /* ------------------------------------------------------------------ */
  renderAdvanced(el) {
    var _a, _b, _c;
    sectionHeader(el, "Advanced", "Diagnostics, migration and data management.");
    const adv = this.settings.settings.advanced;
    const up = (mutate) => this.settings.update("advanced", (draft) => mutate(draft.advanced));
    new import_obsidian7.Setting(el).setName("Debug mode").setDesc("Verbose tracing in the developer console.").addToggle((toggle) => toggle.setValue(adv.debugMode).onChange((v) => void up((d) => {
      d.debugMode = v;
    })));
    labeledSlider(el, {
      name: "Analytics update interval",
      min: 250,
      max: 5e3,
      step: 250,
      value: adv.refreshIntervalMs,
      unit: " ms",
      desc: "How often the heatmap re-measures the viewport. Lower = more responsive, higher = less work.",
      onChange: (v) => up((d) => {
        d.refreshIntervalMs = v;
      })
    });
    const migration = this.settings.raw.migration;
    const migCard = el.createDiv({ cls: "frs-card" });
    migCard.createEl("h4", { text: "Legacy plugin migration" });
    const state = (_a = migration == null ? void 0 : migration.state) != null ? _a : "pending";
    migCard.createEl("p", {
      cls: "frs-card-note",
      text: state === "done" ? `Settings and data were migrated from: ${((_b = migration == null ? void 0 : migration.sources) != null ? _b : []).join(", ")}.` : state === "skipped" ? "No legacy plugin data was found (fresh install, or the old plugins never had data)." : "Migration has not run yet \u2014 it runs on the next plugin load."
    });
    for (const note of (_c = migration == null ? void 0 : migration.notes) != null ? _c : []) {
      migCard.createEl("p", { cls: "frs-card-note", text: note });
    }
    new import_obsidian7.Setting(migCard).setName("Re-run migration").setDesc(`Reads ${Object.values(LEGACY_PLUGIN_PATHS).map((p) => p.replace(".obsidian/plugins/", "")).join(", ")} and merges any settings found. Existing suite settings win for keys you've changed here.`).addButton(
      (button) => button.setButtonText("Re-run").onClick(async () => {
        await this.plugin.rerunMigration();
        new import_obsidian7.Notice("Migration re-checked. Existing customized settings were preserved.");
        this.display();
      })
    );
    const legacyCard = el.createDiv({ cls: "frs-card" });
    legacyCard.createEl("h4", { text: "Legacy plugins" });
    const detected = this.plugin.detectLegacyPlugins();
    if (detected.length > 0) {
      legacyCard.createEl("p", {
        cls: "frs-card-note",
        text: `These legacy plugins are currently enabled: ${detected.join(", ")}. Running them together with the suite duplicates UI (two floating timers, two rulers). Disable them now?`
      });
      new import_obsidian7.Setting(legacyCard).setName("Disable legacy plugins").addButton(
        (button) => button.setButtonText("Disable them").setWarning().onClick(async () => {
          const ok = await this.plugin.disableLegacyPlugins();
          new import_obsidian7.Notice(ok ? "Legacy plugins disabled." : "Could not disable them automatically \u2014 disable them in Settings \u2192 Community plugins.");
          this.display();
        })
      );
    } else {
      legacyCard.createEl("p", {
        cls: "frs-card-note",
        text: "No legacy Focus Read / Heatmap plugins are enabled. The old plugin folders and their data files were left untouched \u2014 you can remove them from .obsidian/plugins whenever you like."
      });
    }
    const dangerCard = el.createDiv({ cls: "frs-card frs-card-danger" });
    dangerCard.createEl("h4", { text: "Reset" });
    new import_obsidian7.Setting(dangerCard).setName("Reset all settings").setDesc("Every section back to its defaults. Reading statistics and heatmap records are kept.").addButton(
      (button) => button.setButtonText("Reset settings").setWarning().onClick(() => {
        new ConfirmModal(
          this.app,
          "Reset all settings?",
          "Every setting returns to its default value. Your statistics and heatmap records are not touched.",
          "Reset settings",
          async () => {
            await this.settings.resetSections([
              "general",
              "timer",
              "focus",
              "ruler",
              "typography",
              "heatmap",
              "appearance",
              "advanced"
            ]);
            new import_obsidian7.Notice("All settings were reset to defaults.");
            this.display();
          }
        ).open();
      })
    );
  }
};

// focus-read-suite/src/main.ts
var LEGACY_PLUGIN_IDS = ["focus-read-timer", "focus-read-typography", "heatmap-of-notes"];
var FocusReadSuitePlugin = class extends import_obsidian8.Plugin {
  constructor(app, manifest) {
    super(app, manifest);
    this.unsubscribeSettings = null;
    this.modules = {
      timer: new TimerModule(),
      focus: new ReadingFocusModule(),
      typography: new TypographyModule(),
      heatmap: new HeatmapModule()
    };
  }
  /* ------------------------------------------------------------------ */
  /* Lifecycle                                                           */
  /* ------------------------------------------------------------------ */
  async onload() {
    logger.info("Loading Focus Read Suite\u2026");
    this.settings = new SettingsManager({
      loadData: () => this.loadData(),
      saveData: (data) => this.saveData(data)
    });
    this.migration = new MigrationService({
      readJson: (path) => this.readLegacyJson(path)
    });
    await this.settings.load(async (raw) => {
      var _a, _b, _c, _d;
      const wasSettled = ((_a = raw == null ? void 0 : raw.migration) == null ? void 0 : _a.state) === "done" || ((_b = raw == null ? void 0 : raw.migration) == null ? void 0 : _b.state) === "skipped";
      const migrated = await this.migration.migrate(raw);
      if (!wasSettled && ((_c = migrated.migration) == null ? void 0 : _c.state) === "done") {
        const sources = (_d = migrated.migration.sources) != null ? _d : [];
        new import_obsidian8.Notice(
          `Focus Read Suite: migrated your settings from ${sources.length} plugin${sources.length === 1 ? "" : "s"} (${sources.join(", ")}).`
        );
      }
      return migrated;
    });
    logger.setDebug(this.settings.settings.advanced.debugMode);
    this.lifecycle = new LifecycleHub({
      registerDomEvent: (el, type, cb, options) => this.registerDomEvent(el, type, cb, options),
      registerInterval: (id) => this.registerInterval(id),
      registerEvent: (ref) => this.registerEvent(ref),
      register: (cb) => this.register(cb)
    });
    this.applyAppearance();
    this.lifecycle.onUnload(() => this.clearAppearance());
    const ctx = {
      app: this.app,
      settings: this.settings,
      lifecycle: this.lifecycle,
      isMobile: this.app.isMobile === true,
      addCommand: (command) => this.addCommand(command)
    };
    for (const module2 of this.moduleList()) {
      try {
        await module2.load(ctx);
      } catch (err) {
        logger.error(`Module "${module2.name}" failed to load.`, err);
        new import_obsidian8.Notice(`Focus Read Suite: the ${module2.name} module failed to load (see console).`);
      }
    }
    this.unsubscribeSettings = this.settings.subscribe((changed) => {
      this.dispatchSettingsChange(changed);
    });
    this.addCommand({
      id: "open-settings",
      name: "Open Focus Read Suite settings",
      callback: () => this.openSettings()
    });
    this.addCommand({
      id: "disable-legacy-plugins",
      name: "Disable the legacy Focus Read / Heatmap plugins",
      callback: () => void this.disableLegacyPlugins()
    });
    this.addSettingTab(new FocusSuiteSettingTab(this.app, this));
    logger.info("Focus Read Suite loaded.");
  }
  async onunload() {
    var _a;
    logger.info("Unloading Focus Read Suite\u2026");
    (_a = this.unsubscribeSettings) == null ? void 0 : _a.call(this);
    this.unsubscribeSettings = null;
    const list = this.moduleList();
    for (const module2 of [...list].reverse()) {
      try {
        await module2.unload();
      } catch (err) {
        logger.error(`Module "${module2.name}" failed to unload cleanly.`, err);
      }
    }
    this.clearAppearance();
    await this.settings.persist(true);
    logger.info("Focus Read Suite unloaded.");
  }
  moduleList() {
    return [this.modules.timer, this.modules.focus, this.modules.typography, this.modules.heatmap];
  }
  /* ------------------------------------------------------------------ */
  /* Settings dispatch                                                   */
  /* ------------------------------------------------------------------ */
  dispatchSettingsChange(changed) {
    for (const module2 of this.moduleList()) {
      if (changed.some((section) => module2.sections().includes(section))) {
        try {
          module2.onSettingsChanged(changed);
        } catch (err) {
          logger.error(`Module "${module2.name}" failed to apply settings change.`, err);
        }
      }
    }
    if (changed.includes("appearance")) this.applyAppearance();
    if (changed.includes("advanced")) {
      logger.setDebug(this.settings.settings.advanced.debugMode);
    }
  }
  /* ------------------------------------------------------------------ */
  /* Appearance                                                          */
  /* ------------------------------------------------------------------ */
  /** Writes the shared accent + widget scale into CSS variables. */
  applyAppearance() {
    const { appearance } = this.settings.settings;
    const rootStyle = document.documentElement.style;
    if (appearance.accentMode === "custom") {
      rootStyle.setProperty("--frs-accent", appearance.customAccent);
    } else {
      rootStyle.removeProperty("--frs-accent");
    }
    rootStyle.setProperty("--frs-widget-scale", String(appearance.widgetScale));
  }
  clearAppearance() {
    const rootStyle = document.documentElement.style;
    rootStyle.removeProperty("--frs-accent");
    rootStyle.removeProperty("--frs-widget-scale");
  }
  /* ------------------------------------------------------------------ */
  /* Legacy plugin interop                                               */
  /* ------------------------------------------------------------------ */
  /** Reads a legacy plugin's data.json (vault-relative), or null. */
  async readLegacyJson(path) {
    var _a;
    try {
      const adapter = (_a = this.app.vault) == null ? void 0 : _a.adapter;
      if (!(adapter == null ? void 0 : adapter.exists) || !(adapter == null ? void 0 : adapter.read)) return null;
      const normalized = (0, import_obsidian8.normalizePath)(path);
      if (!await adapter.exists(normalized)) return null;
      const text = await adapter.read(normalized);
      return JSON.parse(text);
    } catch (err) {
      logger.warn(`Could not read legacy data at ${path}.`, err);
      return null;
    }
  }
  /** Legacy plugins that are currently enabled (empty when none). */
  detectLegacyPlugins() {
    try {
      const plugins = this.app.plugins;
      const enabled = plugins == null ? void 0 : plugins.enabledPlugins;
      if (enabled instanceof Set) {
        return LEGACY_PLUGIN_IDS.filter((id) => enabled.has(id));
      }
    } catch (e) {
    }
    return [];
  }
  /** Disables the legacy plugins through Obsidian's plugin manager. */
  async disableLegacyPlugins() {
    const detected = this.detectLegacyPlugins();
    if (detected.length === 0) {
      new import_obsidian8.Notice("No legacy plugins are enabled.");
      return true;
    }
    try {
      const plugins = this.app.plugins;
      if (typeof (plugins == null ? void 0 : plugins.disablePlugin) === "function") {
        for (const id of detected) {
          await plugins.disablePlugin(id);
        }
        new import_obsidian8.Notice(`Disabled: ${detected.join(", ")}`);
        return true;
      }
      const commands = this.app.commands;
      if (typeof (commands == null ? void 0 : commands.executeCommandById) === "function") {
        for (const id of detected) {
          commands.executeCommandById(`app:disable-plugin:${id}`);
        }
        new import_obsidian8.Notice(`Disabled: ${detected.join(", ")}`);
        return true;
      }
    } catch (err) {
      logger.warn("Automatic disable failed.", err);
    }
    return false;
  }
  /* ------------------------------------------------------------------ */
  /* Migration re-run (Advanced settings)                                */
  /* ------------------------------------------------------------------ */
  /**
   * Re-runs the legacy mapping and merges it UNDER the current settings
   * (keys the user has changed in the suite win; only missing keys are
   * filled from legacy data). Stats/records are never overwritten.
   */
  async rerunMigration() {
    var _a;
    const raw = this.settings.raw;
    const reset = { ...raw, migration: { state: "pending" } };
    const migrated = await this.migration.migrate(reset, true);
    const mergedSettings = { ...(_a = migrated.settings) != null ? _a : {} };
    for (const key of Object.keys(this.settings.settings)) {
      mergedSettings[key] = this.settings.settings[key];
    }
    const info = migrated.migration;
    await this.settings.setExtra("migration", info, true);
    await this.settings.replaceAllSettings(mergedSettings);
    return info;
  }
  /* ------------------------------------------------------------------ */
  /* Misc                                                                */
  /* ------------------------------------------------------------------ */
  openSettings() {
    var _a, _b;
    try {
      const setting = this.app.setting;
      (_a = setting == null ? void 0 : setting.open) == null ? void 0 : _a.call(setting);
      (_b = setting == null ? void 0 : setting.openTabById) == null ? void 0 : _b.call(setting, this.manifest.id);
    } catch (e) {
      new import_obsidian8.Notice("Open Settings \u2192 Community plugins \u2192 Focus Read Suite.");
    }
  }
};
