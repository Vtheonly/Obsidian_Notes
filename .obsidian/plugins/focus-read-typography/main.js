const { Plugin, PluginSettingTab, Setting, Notice } = require("obsidian");

/* ---------- Constants ---------- */
const TYPOGRAPHY_STYLE_ID = "frt-dynamic-style";
const GOOGLE_FONTS_STYLE_ID = "frt-google-fonts-style";
const READING_RULER_ID = "frt-reading-ruler";
const INJECTED_STYLE_ID = "frt-injected-style";
const BODY_CLASS = "frt-typography-on";
const RULER_BODY_CLASS = "frt-ruler-on";

const FONT_STACKS = [
  { id: "system", label: "System default", stack: "", googleFamily: null },
  { id: "lexend", label: "Lexend (recommended for ADHD)", stack: "'Lexend', sans-serif", googleFamily: "Lexend" },
  { id: "atkinson", label: "Atkinson Hyperlegible", stack: "'Atkinson Hyperlegible', sans-serif", googleFamily: "Atkinson+Hyperlegible" },
  { id: "inter", label: "Inter", stack: "'Inter', sans-serif", googleFamily: "Inter" },
  { id: "source", label: "Source Sans 3", stack: "'Source Sans 3', sans-serif", googleFamily: "Source+Sans+3" },
  { id: "ibmplex", label: "IBM Plex Sans", stack: "'IBM Plex Sans', sans-serif", googleFamily: "IBM+Plex+Sans" },
  { id: "noto", label: "Noto Sans", stack: "'Noto Sans', sans-serif", googleFamily: "Noto+Sans" },
  { id: "custom", label: "Custom font stack", stack: "", googleFamily: null }
];

const FONT_STACK_BY_ID = {
  lexend: "'Lexend', sans-serif",
  atkinson: "'Atkinson Hyperlegible', sans-serif",
  inter: "'Inter', sans-serif",
  source: "'Source Sans 3', sans-serif",
  ibmplex: "'IBM Plex Sans', sans-serif",
  noto: "'Noto Sans', sans-serif"
};

const DEFAULT_SETTINGS = {
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
  readingRulerOpacity: 0.18
};

const BASE_CSS = `
:root {
  --frt-font-size: 17px;
  --frt-line-height: 1.7;
  --frt-para-spacing: 1.4;
  --frt-max-width: 66ch;
  --frt-font-family: ;
}

body.frt-typography-on .markdown-reading-view .markdown-preview-section {
  font-size: var(--frt-font-size);
  line-height: var(--frt-line-height);
  max-width: var(--frt-max-width);
  margin-left: auto;
  margin-right: auto;
}
body.frt-typography-on .markdown-reading-view p {
  margin-bottom: calc(var(--frt-font-size) * (var(--frt-para-spacing) - 1));
}
body.frt-typography-on .markdown-reading-view li {
  margin-bottom: calc(var(--frt-font-size) * 0.25);
}
body.frt-typography-on .markdown-source-view .cm-content,
body.frt-typography-on .markdown-source-view .cm-line {
  max-width: var(--frt-max-width);
}
body.frt-typography-on .markdown-source-view .cm-content {
  font-size: var(--frt-font-size) !important;
  line-height: var(--frt-line-height) !important;
}

/* Reading ruler */
.frt-reading-ruler {
  position: fixed;
  left: 0;
  right: 0;
  height: 28px;
  top: -9999px;
  background: #ffd54f;
  opacity: 0.18;
  pointer-events: none;
  z-index: 9999;
  display: none;
  border-top: 1px solid rgba(0, 0, 0, 0.18);
  border-bottom: 1px solid rgba(0, 0, 0, 0.18);
  mix-blend-mode: multiply;
  transition: opacity 0.3s;
}
body.frt-ruler-on .frt-reading-ruler { display: block; }
body.theme-dark .frt-reading-ruler {
  border-top-color: rgba(255, 255, 255, 0.18);
  border-bottom-color: rgba(255, 255, 255, 0.18);
}
`;

/* ---------- Plugin ---------- */
class TypographyPlugin extends Plugin {
  async onload() {
    await this.loadSettings();
    this.injectBaseCSS();
    this.createRulerElement();
    this.applyGoogleFonts();
    this.applyTypography();
    this.applyRuler();
    this.applyBodyClasses();
    this.addSettingTab(new TypographySettingTab(this.app, this));
    this.registerCommands();
  }

  async onunload() {
    if (this._rulerMoveHandler) {
      window.removeEventListener("mousemove", this._rulerMoveHandler);
    }
    const ruler = document.getElementById(READING_RULER_ID);
    if (ruler) ruler.remove();
    [INJECTED_STYLE_ID, TYPOGRAPHY_STYLE_ID, GOOGLE_FONTS_STYLE_ID].forEach(id => {
      const s = document.getElementById(id);
      if (s) s.remove();
    });
    document.body.classList.remove(BODY_CLASS, RULER_BODY_CLASS);
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }
  async saveSettings() { await this.saveData(this.settings); }

  injectBaseCSS() {
    let s = document.getElementById(INJECTED_STYLE_ID);
    if (!s) {
      s = document.createElement("style");
      s.id = INJECTED_STYLE_ID;
      document.head.appendChild(s);
    }
    s.textContent = BASE_CSS;
  }

  createRulerElement() {
    if (document.getElementById(READING_RULER_ID)) return;
    const ruler = document.createElement("div");
    ruler.id = READING_RULER_ID;
    ruler.className = "frt-reading-ruler";
    document.body.appendChild(ruler);
    this._rulerMoveHandler = e => this.onRulerMove(e);
    window.addEventListener("mousemove", this._rulerMoveHandler);
  }

  applyBodyClasses() {
    document.body.classList.toggle(BODY_CLASS, this.settings.typographyEnabled);
    document.body.classList.toggle(RULER_BODY_CLASS, this.settings.readingRulerEnabled);
  }

  applyGoogleFonts() {
    const existing = document.getElementById(GOOGLE_FONTS_STYLE_ID);
    if (existing) existing.remove();
    if (!this.settings.loadGoogleFonts) return;
    const families = ["Lexend", "Atkinson+Hyperlegible", "Inter", "Source+Sans+3", "IBM+Plex+Sans", "Noto+Sans"];
    const url = "https://fonts.googleapis.com/css2?" + families.map(f => `family=${f}`).join("&") + "&display=swap";
    const style = document.createElement("style");
    style.id = GOOGLE_FONTS_STYLE_ID;
    style.textContent = `@import url('${url}');`;
    document.head.appendChild(style);
  }

  resolveFontStack() {
    const s = this.settings;
    if (s.fontFamily === "custom") return s.customFontFamily || "";
    return FONT_STACK_BY_ID[s.fontFamily] || "";
  }

  applyTypography() {
    let style = document.getElementById(TYPOGRAPHY_STYLE_ID);
    if (!style) {
      style = document.createElement("style");
      style.id = TYPOGRAPHY_STYLE_ID;
      document.head.appendChild(style);
    }
    const s = this.settings;
    const stack = this.resolveFontStack();
    const rules = [];
    rules.push(":root {");
    rules.push(`  --frt-font-size: ${s.fontSize}px;`);
    rules.push(`  --frt-line-height: ${s.lineHeight};`);
    rules.push(`  --frt-para-spacing: ${s.paragraphSpacing};`);
    rules.push(`  --frt-max-width: ${s.maxWidthChars}ch;`);
    rules.push(`  --frt-font-family: ${stack};`);
    rules.push("}");
    rules.push(`body.frt-typography-on .markdown-reading-view .markdown-preview-section {
      font-size: var(--frt-font-size) !important;
      line-height: var(--frt-line-height) !important;
      ${stack ? "font-family: var(--frt-font-family) !important;" : ""}
      max-width: var(--frt-max-width) !important;
      margin-left: auto !important;
      margin-right: auto !important;
    }`);
    rules.push(`body.frt-typography-on .markdown-reading-view p,
    body.frt-typography-on .markdown-reading-view li {
      ${stack ? "font-family: var(--frt-font-family) !important;" : ""}
    }`);
    rules.push(`body.frt-typography-on .markdown-reading-view p {
      margin-bottom: calc(var(--frt-font-size) * (var(--frt-para-spacing) - 1)) !important;
    }`);
    rules.push(`body.frt-typography-on .markdown-source-view .cm-content {
      ${stack ? "font-family: var(--frt-font-family) !important;" : ""}
      max-width: var(--frt-max-width) !important;
      font-size: var(--frt-font-size) !important;
      line-height: var(--frt-line-height) !important;
    }`);
    rules.push(`body.frt-typography-on .markdown-source-view .cm-line {
      max-width: var(--frt-max-width) !important;
    }`);
    style.textContent = rules.join("\n");
  }

  applyRuler() {
    const ruler = document.getElementById(READING_RULER_ID);
    if (!ruler) return;
    const s = this.settings;
    ruler.style.height = `${s.readingRulerHeight}px`;
    ruler.style.background = s.readingRulerColor;
    ruler.style.opacity = `${s.readingRulerOpacity}`;
    document.body.classList.toggle(RULER_BODY_CLASS, s.readingRulerEnabled);
  }

  onRulerMove(e) {
    if (!this.settings.readingRulerEnabled) return;
    const ruler = document.getElementById(READING_RULER_ID);
    if (!ruler) return;
    const h = this.settings.readingRulerHeight;
    ruler.style.top = `${e.clientY - h / 2}px`;
  }

  registerCommands() {
    this.addCommand({
      id: "toggle-typography",
      name: "Toggle Typography",
      callback: async () => {
        this.settings.typographyEnabled = !this.settings.typographyEnabled;
        await this.saveSettings();
        this.applyBodyClasses();
      }
    });
    this.addCommand({
      id: "toggle-ruler",
      name: "Toggle Reading Ruler",
      callback: async () => {
        this.settings.readingRulerEnabled = !this.settings.readingRulerEnabled;
        await this.saveSettings();
        this.applyRuler();
        new Notice(`Reading Ruler: ${this.settings.readingRulerEnabled ? "ON" : "OFF"}`);
      }
    });
  }
}

/* ---------- Settings Tab ---------- */
class TypographySettingTab extends PluginSettingTab {
  constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    this.section("Typography");
    this.toggle("Enable Typography", "Apply font, size, line height, and max width.", "typographyEnabled");
    this.dropdown("Reading font", FONT_STACKS.map(f => ({ id: f.id, label: f.label })), "fontFamily");
    if (this.plugin.settings.fontFamily === "custom") {
      this.text("Custom font stack", "customFontFamily");
    }
    this.toggle("Load Google Fonts", "Inject Google Fonts stylesheet (requires internet).", "loadGoogleFonts");
    this.slider("Font size (px)", 13, 26, 1, "fontSize");
    this.slider("Line height", 1.2, 2.2, 0.05, "lineHeight");
    this.slider("Paragraph spacing", 1, 2.5, 0.1, "paragraphSpacing");
    this.slider("Max line width (chars)", 40, 120, 1, "maxWidthChars");

    this.section("Reading Ruler");
    this.toggle("Enable Reading Ruler", "Mouse-following horizontal bar.", "readingRulerEnabled");
    this.slider("Ruler height (px)", 10, 80, 1, "readingRulerHeight");
    this.color("Ruler color", "readingRulerColor");
    this.slider("Ruler opacity", 0.05, 0.6, 0.01, "readingRulerOpacity");
  }

  section(text) { this.containerEl.createEl("h2", { text }); }

  toggle(name, desc, key) {
    new Setting(this.containerEl).setName(name).setDesc(desc)
      .addToggle(cb => cb.setValue(this.plugin.settings[key])
        .onChange(async v => { this.plugin.settings[key] = v; await this.plugin.saveSettings(); this.plugin.applyBodyClasses(); this.display(); }));
  }
  slider(name, min, max, step, key) {
    new Setting(this.containerEl).setName(name)
      .addSlider(cb => cb.setLimits(min, max, step).setValue(this.plugin.settings[key]).setDynamicTooltip()
        .onChange(async v => { this.plugin.settings[key] = v; await this.plugin.saveSettings();
          if (key === "readingRulerHeight" || key === "readingRulerColor" || key === "readingRulerOpacity") this.plugin.applyRuler();
          else this.plugin.applyTypography();
        }));
  }
  text(name, key) {
    new Setting(this.containerEl).setName(name)
      .addText(cb => cb.setValue(this.plugin.settings[key])
        .onChange(async v => { this.plugin.settings[key] = v; await this.plugin.saveSettings(); this.plugin.applyTypography(); }));
  }
  color(name, key) {
    new Setting(this.containerEl).setName(name)
      .addColorPicker(cb => cb.setValue(this.plugin.settings[key])
        .onChange(async v => { this.plugin.settings[key] = v; await this.plugin.saveSettings(); this.plugin.applyRuler(); }));
  }
  dropdown(name, options, key) {
    new Setting(this.containerEl).setName(name)
      .addDropdown(cb => {
        for (const opt of options) cb.addOption(opt.id, opt.label);
        cb.setValue(this.plugin.settings[key])
          .onChange(async v => { this.plugin.settings[key] = v; await this.plugin.saveSettings(); this.plugin.applyTypography(); this.display(); });
      });
  }
}

module.exports = TypographyPlugin;
