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

// focus-read-typography/src/main.ts
var main_exports = {};
__export(main_exports, {
  DEFAULT_SETTINGS: () => DEFAULT_SETTINGS,
  FONT_OPTIONS: () => FONT_OPTIONS,
  default: () => TypographyRulerPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian3 = require("obsidian");

// focus-read-typography/src/settings.ts
var DEFAULT_SETTINGS = {
  typographyEnabled: true,
  fontFamily: "system",
  customFontFamily: "",
  loadGoogleFonts: false,
  fontSize: 17,
  lineHeight: 1.7,
  maxWidthChars: 66,
  paragraphSpacing: 1.4,
  readingRulerEnabled: false,
  readingRulerHeight: 28,
  readingRulerColor: "#ffd54f",
  readingRulerOpacity: 0.18,
  readingRulerMode: "auto",
  readingRulerPositionRatio: null
};
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
function clamp(value, min, max, fallback) {
  if (typeof value !== "number" || !Number.isFinite(value)) return fallback;
  return Math.min(Math.max(value, min), max);
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
function normalizeSettings(raw) {
  const merged = { ...DEFAULT_SETTINGS, ...raw != null ? raw : {} };
  merged.fontSize = Math.round(clamp(merged.fontSize, 13, 26, DEFAULT_SETTINGS.fontSize));
  merged.lineHeight = Math.round(clamp(merged.lineHeight, 1.2, 2.2, DEFAULT_SETTINGS.lineHeight) * 100) / 100;
  merged.paragraphSpacing = Math.round(clamp(merged.paragraphSpacing, 1, 2.5, DEFAULT_SETTINGS.paragraphSpacing) * 100) / 100;
  merged.maxWidthChars = Math.round(clamp(merged.maxWidthChars, 40, 120, DEFAULT_SETTINGS.maxWidthChars));
  merged.readingRulerHeight = Math.round(clamp(merged.readingRulerHeight, 10, 80, DEFAULT_SETTINGS.readingRulerHeight));
  merged.readingRulerOpacity = Math.round(clamp(merged.readingRulerOpacity, 0.05, 0.9, DEFAULT_SETTINGS.readingRulerOpacity) * 100) / 100;
  merged.readingRulerColor = /^#[0-9a-fA-F]{3,8}$/.test(String(merged.readingRulerColor)) ? merged.readingRulerColor : DEFAULT_SETTINGS.readingRulerColor;
  if (merged.readingRulerMode !== "auto" && merged.readingRulerMode !== "follow" && merged.readingRulerMode !== "manual") {
    merged.readingRulerMode = "auto";
  }
  if (merged.readingRulerPositionRatio !== null) {
    const ratio = Number(merged.readingRulerPositionRatio);
    merged.readingRulerPositionRatio = Number.isFinite(ratio) ? Math.min(Math.max(ratio, 0), 1) : null;
  }
  merged.customFontFamily = sanitizeFontStack(merged.customFontFamily);
  return merged;
}

// focus-read-typography/src/typography.ts
var TYPOGRAPHY_BODY_CLASS = "frt-typography-on";
var GOOGLE_FONTS_LINK_ID = "frt-google-fonts-link";
var ROOT_VARS = [
  "--frt-font-size",
  "--frt-line-height",
  "--frt-para-spacing",
  "--frt-max-width",
  "--frt-font-family"
];
var TypographyController = class {
  constructor(getSettings) {
    this.getSettings = getSettings;
  }
  /** Writes current typography settings into CSS variables + body class. */
  apply() {
    const s = this.getSettings();
    const rootStyle = document.documentElement.style;
    rootStyle.setProperty("--frt-font-size", `${s.fontSize}px`);
    rootStyle.setProperty("--frt-line-height", String(s.lineHeight));
    rootStyle.setProperty("--frt-para-spacing", String(s.paragraphSpacing));
    rootStyle.setProperty("--frt-max-width", `${s.maxWidthChars}ch`);
    rootStyle.setProperty("--frt-font-family", resolveFontStack(s) || "inherit");
    document.body.classList.toggle(TYPOGRAPHY_BODY_CLASS, s.typographyEnabled);
  }
  /**
   * Manages the Google Fonts `<link>`.
   * Only the *selected* family is loaded — the old version injected a
   * stylesheet URL containing all six families at once, wasting bandwidth
   * (especially on mobile connections).
   */
  applyGoogleFonts() {
    var _a;
    const s = this.getSettings();
    let link = document.getElementById(GOOGLE_FONTS_LINK_ID);
    const option = fontOptionById(s.fontFamily);
    const googleFamily = (_a = option == null ? void 0 : option.googleFamily) != null ? _a : null;
    if (!s.loadGoogleFonts || !googleFamily) {
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

// focus-read-typography/src/ruler.ts
var import_obsidian = require("obsidian");

// shared/src/viewport.ts
function getViewportSize() {
  var _a, _b, _c, _d;
  const w = typeof window !== "undefined" ? (_b = (_a = window.visualViewport) == null ? void 0 : _a.width) != null ? _b : window.innerWidth : 1024;
  const h = typeof window !== "undefined" ? (_d = (_c = window.visualViewport) == null ? void 0 : _c.height) != null ? _d : window.innerHeight : 768;
  return { width: Math.max(0, w), height: Math.max(0, h) };
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

// focus-read-typography/src/ruler.ts
var RULER_ID = "frt-reading-ruler";
var RULER_BODY_CLASS = "frt-ruler-on";
var DEFAULT_POSITION_RATIO = 0.4;
var KEYBOARD_STEP_RATIO = 0.05;
var ReadingRuler = class {
  constructor(host) {
    this.el = null;
    this.handle = null;
    /** Current top position of the ruler band, in px. */
    this.topPx = 0;
    /** True while a pointer drag on the handle is active. */
    this.dragging = false;
    this.dragPointerId = null;
    this.dragStartPointerY = 0;
    this.dragStartTopPx = 0;
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
    el.className = "frt-reading-ruler";
    el.setAttribute("aria-hidden", "true");
    const band = document.createElement("div");
    band.className = "frt-ruler-band";
    el.appendChild(band);
    const handle = document.createElement("div");
    handle.className = "frt-ruler-handle";
    handle.setAttribute("role", "button");
    handle.setAttribute(
      "aria-label",
      "Reading ruler handle \u2014 drag to move the ruler, double-tap to center it"
    );
    const icon = document.createElement("span");
    icon.className = "frt-ruler-handle-icon";
    icon.textContent = "\u283F";
    handle.appendChild(icon);
    el.appendChild(handle);
    document.body.appendChild(el);
    this.el = el;
    this.handle = handle;
    this.bindPointerEvents();
    this.applyConfig();
    this.applyPosition();
    this.applyVisibility();
  }
  destroy() {
    var _a;
    (_a = this.el) == null ? void 0 : _a.remove();
    this.el = null;
    this.handle = null;
  }
  /* ------------------------------------------------------------------ */
  /* Configuration                                                       */
  /* ------------------------------------------------------------------ */
  /** Applies height/color/opacity and re-clamps the position. */
  applyConfig() {
    if (!this.el) return;
    const s = this.host.settings;
    this.el.style.setProperty("--frt-ruler-height", `${s.readingRulerHeight}px`);
    this.el.style.setProperty("--frt-ruler-color", s.readingRulerColor);
    this.el.style.setProperty("--frt-ruler-opacity", String(s.readingRulerOpacity));
    this.applyPosition();
  }
  applyVisibility() {
    const enabled = this.host.settings.readingRulerEnabled;
    document.body.classList.toggle(RULER_BODY_CLASS, enabled);
    if (enabled && !this.el) {
      this.mount();
      return;
    }
    if (enabled) this.applyPosition();
  }
  /* ------------------------------------------------------------------ */
  /* Positioning                                                         */
  /* ------------------------------------------------------------------ */
  /** Effective mode after resolving "auto" for this device. */
  get effectiveMode() {
    const mode = this.host.settings.readingRulerMode;
    if (mode === "follow" || mode === "manual") return mode;
    return hasHoverPointer() && !import_obsidian.Platform.isMobile ? "follow" : "manual";
  }
  /** Movable vertical range for the current viewport and ruler height. */
  movableRange() {
    const { height } = getViewportSize();
    const rulerHeight = this.host.settings.readingRulerHeight;
    return Math.max(0, height - rulerHeight);
  }
  /** Restores the persisted ratio (or the default) and clamps it. */
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
    this.topPx = this.ratioToPx(this.host.settings.readingRulerPositionRatio);
    this.el.style.transform = `translate3d(0, ${Math.round(this.topPx)}px, 0)`;
  }
  /** Moves the ruler to an absolute viewport Y, clamped. */
  moveToPx(px, options = {}) {
    const range = this.movableRange();
    this.topPx = Math.min(Math.max(px, 0), range);
    if (this.el) {
      this.el.style.transform = `translate3d(0, ${Math.round(this.topPx)}px, 0)`;
    }
    if (options.persist) {
      this.host.settings.readingRulerPositionRatio = this.pxToRatio(this.topPx);
      void this.host.saveSettings();
    }
  }
  /** Public API for keyboard commands / handle double-tap. */
  center() {
    this.moveToPx(this.movableRange() / 2, { persist: true });
  }
  nudge(direction) {
    const range = this.movableRange();
    this.moveToPx(this.topPx + direction * range * KEYBOARD_STEP_RATIO, { persist: true });
  }
  /* ------------------------------------------------------------------ */
  /* Pointer handling                                                    */
  /* ------------------------------------------------------------------ */
  bindPointerEvents() {
    if (!this.el || !this.handle) return;
    const host = this.host;
    host.registerDomEvent(this.handle, "pointerdown", (e) => {
      var _a, _b;
      if (e.button !== 0) return;
      this.dragging = true;
      this.dragPointerId = e.pointerId;
      this.dragStartPointerY = e.clientY;
      this.dragStartTopPx = this.topPx;
      (_a = this.el) == null ? void 0 : _a.classList.add("frt-ruler-dragging");
      try {
        (_b = this.handle) == null ? void 0 : _b.setPointerCapture(e.pointerId);
      } catch (e2) {
      }
      e.preventDefault();
      e.stopPropagation();
    });
    host.registerDomEvent(this.handle, "pointermove", (e) => {
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      const delta = e.clientY - this.dragStartPointerY;
      this.moveToPx(this.dragStartTopPx + delta);
      e.preventDefault();
    });
    const endDrag = (e) => {
      var _a, _b;
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      this.dragging = false;
      this.dragPointerId = null;
      (_a = this.el) == null ? void 0 : _a.classList.remove("frt-ruler-dragging");
      try {
        (_b = this.handle) == null ? void 0 : _b.releasePointerCapture(e.pointerId);
      } catch (e2) {
      }
      this.moveToPx(this.topPx, { persist: true });
    };
    host.registerDomEvent(this.handle, "pointerup", endDrag);
    host.registerDomEvent(this.handle, "pointercancel", endDrag);
    host.registerDomEvent(this.handle, "lostpointercapture", (e) => {
      var _a;
      if (this.dragging && e.pointerId === this.dragPointerId) {
        this.dragging = false;
        this.dragPointerId = null;
        (_a = this.el) == null ? void 0 : _a.classList.remove("frt-ruler-dragging");
        this.moveToPx(this.topPx, { persist: true });
      }
    });
    host.registerDomEvent(this.handle, "dblclick", () => this.center());
    host.registerDomEvent(this.handle, "contextmenu", (e) => {
      if (this.dragging) e.preventDefault();
    });
    host.registerDomEvent(window, "pointermove", (e) => {
      if (!this.host.settings.readingRulerEnabled) return;
      if (this.effectiveMode !== "follow") return;
      if (this.dragging) return;
      if (e.pointerType === "touch") return;
      const height = this.host.settings.readingRulerHeight;
      const targetY = e.clientY - height / 2;
      this.scheduleApply(() => this.moveToPx(targetY));
    });
    const reflow = () => this.applyPosition();
    host.registerDomEvent(window, "resize", reflow);
    host.registerDomEvent(window, "orientationchange", reflow);
    if (window.visualViewport) {
      host.registerDomEvent(window.visualViewport, "resize", reflow);
    }
  }
};

// focus-read-typography/src/settings-tab.ts
var import_obsidian2 = require("obsidian");
var RULER_MODE_OPTIONS = {
  auto: "Auto (follow on desktop, drag on touch)",
  follow: "Follow pointer (desktop)",
  manual: "Manual \u2014 drag the handle"
};
var TypographySettingTab = class extends import_obsidian2.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    this.section("Typography");
    new import_obsidian2.Setting(containerEl).setName("Enable typography").setDesc("Apply font, size, line height and max width to reading and editing views.").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.typographyEnabled).onChange(async (v) => {
        this.plugin.settings.typographyEnabled = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ typographyEnabled: v });
      })
    );
    new import_obsidian2.Setting(containerEl).setName("Reading font").setDesc("Applied on top of your theme when typography is enabled.").addDropdown((dropdown) => {
      for (const option of FONT_OPTIONS) {
        dropdown.addOption(option.id, option.label);
      }
      dropdown.setValue(this.plugin.settings.fontFamily).onChange(async (v) => {
        this.plugin.settings.fontFamily = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ fontFamily: v });
        this.display();
      });
    });
    if (this.plugin.settings.fontFamily === "custom") {
      new import_obsidian2.Setting(containerEl).setName("Custom font stack").setDesc("CSS font-family value, e.g. Georgia, 'Times New Roman', serif").addText(
        (text) => text.setValue(this.plugin.settings.customFontFamily).onChange(async (v) => {
          this.plugin.settings.customFontFamily = v;
          await this.plugin.saveSettings();
          this.plugin.refreshAll({ customFontFamily: v });
        })
      );
    }
    new import_obsidian2.Setting(containerEl).setName("Load Google Fonts").setDesc("Download the selected font from Google Fonts (requires internet). Only the selected family is loaded.").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.loadGoogleFonts).onChange(async (v) => {
        this.plugin.settings.loadGoogleFonts = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ loadGoogleFonts: v });
      })
    );
    this.slider("Font size (px)", 13, 26, 1, "fontSize");
    this.slider("Line height", 1.2, 2.2, 0.05, "lineHeight");
    this.slider("Paragraph spacing", 1, 2.5, 0.1, "paragraphSpacing");
    this.slider("Max line width (chars)", 40, 120, 1, "maxWidthChars");
    this.section("Reading ruler");
    new import_obsidian2.Setting(containerEl).setName("Enable reading ruler").setDesc(
      "A horizontal highlight band over the note. Drag the round handle on its right edge to position it (works with mouse and touch)."
    ).addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.readingRulerEnabled).onChange(async (v) => {
        this.plugin.settings.readingRulerEnabled = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ readingRulerEnabled: v });
      })
    );
    new import_obsidian2.Setting(containerEl).setName("Ruler interaction mode").setDesc(
      "Follow: the band tracks your mouse. Manual: the band stays where you drag it \u2014 recommended on touch devices."
    ).addDropdown((dropdown) => {
      for (const [mode, label] of Object.entries(RULER_MODE_OPTIONS)) {
        dropdown.addOption(mode, label);
      }
      dropdown.setValue(this.plugin.settings.readingRulerMode).onChange(async (v) => {
        this.plugin.settings.readingRulerMode = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ readingRulerMode: v });
      });
    });
    this.slider("Ruler height (px)", 10, 80, 1, "readingRulerHeight");
    this.slider("Ruler opacity", 0.05, 0.9, 0.01, "readingRulerOpacity");
    new import_obsidian2.Setting(containerEl).setName("Ruler color").addColorPicker(
      (picker) => picker.setValue(this.plugin.settings.readingRulerColor).onChange(async (v) => {
        this.plugin.settings.readingRulerColor = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ readingRulerColor: v });
      })
    );
    new import_obsidian2.Setting(containerEl).setName("Reset ruler position").setDesc("Put the ruler back at its default height (slightly above the middle).").addButton(
      (button) => button.setButtonText("Reset position").onClick(async () => {
        this.plugin.settings.readingRulerPositionRatio = null;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ readingRulerPositionRatio: null });
      })
    );
    containerEl.createEl("p", {
      cls: "frt-setting-hint",
      text: `Tip: double-tap (or double-click) the ruler's handle to center it. The position is remembered per screen size, and the "Move reading ruler up/down" commands work from the command palette.`
    });
  }
  section(title) {
    this.containerEl.createEl("h2", { text: title });
  }
  slider(name, min, max, step, key) {
    const value = this.plugin.settings[key];
    new import_obsidian2.Setting(this.containerEl).setName(name).addSlider(
      (slider) => slider.setLimits(min, max, step).setValue(value).setDynamicTooltip().onChange(async (v) => {
        this.plugin.settings[key] = v;
        await this.plugin.saveSettings();
        this.plugin.refreshAll({ [key]: v });
      })
    );
  }
};

// focus-read-typography/src/main.ts
var TypographyRulerPlugin = class extends import_obsidian3.Plugin {
  async onload() {
    this.settings = normalizeSettings(await this.loadData());
    this.typography = new TypographyController(() => this.settings);
    this.ruler = new ReadingRuler(this.rulerHost());
    this.typography.apply();
    this.typography.applyGoogleFonts();
    if (this.settings.readingRulerEnabled) {
      this.ruler.mount();
    }
    this.addSettingTab(new TypographySettingTab(this.app, this));
    this.registerCommands();
  }
  async onunload() {
    this.ruler.destroy();
    this.typography.destroy();
    document.body.classList.remove(RULER_BODY_CLASS);
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  /** Wires the ruler to this plugin's lifecycle-managed registrations. */
  rulerHost() {
    return {
      settings: this.settings,
      saveSettings: () => this.saveSettings(),
      // Delegate to the plugin base class so every listener the ruler
      // registers is cleaned up automatically on unload.
      registerDomEvent: (el, type, callback, options) => this.registerDomEvent(el, type, callback, options)
    };
  }
  registerCommands() {
    this.addCommand({
      id: "toggle-typography",
      name: "Toggle typography",
      callback: async () => {
        this.settings.typographyEnabled = !this.settings.typographyEnabled;
        await this.saveSettings();
        this.typography.apply();
      }
    });
    this.addCommand({
      id: "toggle-ruler",
      name: "Toggle reading ruler",
      callback: async () => {
        this.settings.readingRulerEnabled = !this.settings.readingRulerEnabled;
        await this.saveSettings();
        this.ruler.applyVisibility();
        new import_obsidian3.Notice(`Reading ruler: ${this.settings.readingRulerEnabled ? "ON" : "OFF"}`);
      }
    });
    this.addCommand({
      id: "center-ruler",
      name: "Center reading ruler",
      callback: () => {
        this.ensureRulerVisible();
        this.ruler.center();
      }
    });
    this.addCommand({
      id: "ruler-up",
      name: "Move reading ruler up",
      callback: () => {
        this.ensureRulerVisible();
        this.ruler.nudge(-1);
      }
    });
    this.addCommand({
      id: "ruler-down",
      name: "Move reading ruler down",
      callback: () => {
        this.ensureRulerVisible();
        this.ruler.nudge(1);
      }
    });
  }
  ensureRulerVisible() {
    if (!this.settings.readingRulerEnabled) {
      this.settings.readingRulerEnabled = true;
      void this.saveSettings();
    }
    this.ruler.applyVisibility();
  }
  /** Called by the settings tab after any relevant setting changed. */
  refreshAll(changed) {
    if (changed.readingRulerHeight !== void 0 || changed.readingRulerColor !== void 0 || changed.readingRulerOpacity !== void 0) {
      this.ruler.applyConfig();
    }
    if (changed.readingRulerMode !== void 0) {
      this.ruler.applyPosition();
    }
    if (changed.fontFamily !== void 0 || changed.customFontFamily !== void 0 || changed.loadGoogleFonts !== void 0) {
      this.typography.applyGoogleFonts();
    }
    this.typography.apply();
  }
};
