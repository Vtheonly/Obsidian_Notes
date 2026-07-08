const { Plugin, PluginSettingTab, Setting, MarkdownView, Notice, ItemView } = require("obsidian");

// Constants & Configuration Types
const DASHBOARD_VIEW_TYPE = "fr-dashboard-view";
const TYPOGRAPHY_STYLE_ID = "fr-dynamic-style";
const GOOGLE_FONTS_STYLE_ID = "fr-google-fonts-style";
const READING_RULER_ID = "fr-reading-ruler";
const LINE_FOCUS_OVERLAY_ID = "fr-line-focus-overlay";
const SMART_HIGHLIGHT_STYLE_ID = "fr-smart-highlight-style";
const FLOATING_TIMER_ID = "fr-floating-timer";
const ADHD_NUDGE_ID = "fr-adhd-nudge";
const PROGRESS_STYLE_ID = "fr-progress-style";

const INJECTED_STYLE_ID = "fr-injected-plugin-style";
// Full plugin CSS embedded as a string so the plugin works even if styles.css
// fails to load in Obsidian (caching, mobile quirks, wrong filename, etc.).
// Kept in sync with styles.css — edit there and re-run the embed script.
const PLUGIN_CSS = `/* ===========================================================
   Focus Read — ADHD-friendly reading styles for Obsidian
   =========================================================== */

:root {
  --fr-font-size: 17px;
  --fr-line-height: 1.7;
  --fr-para-spacing: 1.4;
  --fr-max-width: 66ch;
  --fr-font-family: ;
  --fr-def-color: #e8f5e9;
  --fr-bold-color: #fff8c4;
  --fr-line-focus-opacity: 0.35;
  --fr-line-focus-lines: 3;
}

/* ---------- Bionic Reading ---------- */
.fr-bionic {
  font-weight: 700;
}
body.fr-bionic-on .markdown-reading-view .fr-bionic {
  font-weight: 700;
}

/* ---------- Reading Ruler ---------- */
.fr-reading-ruler {
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
body.fr-ruler-on .fr-reading-ruler {
  display: block;
}

/* ---------- Definition highlight ---------- */
body.fr-definitions-on .markdown-reading-view p.fr-definition {
  background: var(--fr-def-color);
  border-left: 3px solid #66bb6a;
  border-radius: 6px;
  padding: 10px 14px;
  margin: 0.6em 0;
}

/* ---------- Bold highlight ---------- */
body.fr-bold-highlight-on .markdown-reading-view strong,
body.fr-bold-highlight-on .markdown-reading-view b {
  background: var(--fr-bold-color);
  border-radius: 3px;
  padding: 0 3px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.04);
}

/* ---------- Typography polish ---------- */
body.fr-typography-on .markdown-reading-view .markdown-preview-section {
  font-size: var(--fr-font-size);
  line-height: var(--fr-line-height);
  max-width: var(--fr-max-width);
  margin-left: auto;
  margin-right: auto;
}
body.fr-typography-on .markdown-reading-view p {
  margin-bottom: calc(var(--fr-font-size) * (var(--fr-para-spacing) - 1));
}
body.fr-typography-on .markdown-reading-view li {
  margin-bottom: calc(var(--fr-font-size) * 0.25);
}
body.fr-typography-on .markdown-source-view .cm-content,
body.fr-typography-on .markdown-source-view .cm-line {
  max-width: var(--fr-max-width);
}

/* ---------- Focus Mode (hide everything except note + timer + progress) ---------- */
body.fr-focus-mode .workspace-ribbon,
body.fr-focus-mode .workspace-split.mod-left-split,
body.fr-focus-mode .workspace-split.mod-right-split,
body.fr-focus-mode .workspace-tabs.mod-top,
body.fr-focus-mode .status-bar,
body.fr-focus-mode .view-header-nav,
body.fr-focus-mode .view-actions,
body.fr-focus-mode .workspace-tab-header-container {
  display: none !important;
}

/* ---------- Smart Highlight (karaoke) ---------- */
.fr-smart-current {
  background: #fff3a3 !important;
  border-radius: 3px;
  box-shadow: 0 0 0 2px rgba(255, 200, 0, 0.25);
  transition: background 0.2s;
}
.fr-smart-prev {
  opacity: 0.5;
}

/* ---------- Line Focus overlay ---------- */
.fr-line-focus-overlay {
  position: fixed;
  left: 0;
  right: 0;
  height: 100px;
  top: -9999px;
  pointer-events: none;
  z-index: 9990;
  background: rgba(255, 255, 255, 0.001);
  box-shadow: 0 0 0 100vmax rgba(0, 0, 0, var(--fr-line-focus-opacity, 0.35));
  display: none;
}
body.fr-line-focus-on .fr-line-focus-overlay {
  display: block;
}
body.theme-dark .fr-line-focus-overlay {
  box-shadow: 0 0 0 100vmax
    rgba(0, 0, 0, calc(var(--fr-line-focus-opacity, 0.35) * 1.4));
}

/* ---------- Hover Definition popup ---------- */
.fr-hover-def {
  background: var(--background-secondary);
  border: 1px solid var(--background-modifier-border);
  border-radius: 6px;
  padding: 8px 12px;
  max-width: 320px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
  font-size: 13px;
}
.fr-hover-def-title {
  font-weight: 600;
  margin-bottom: 4px;
}
.fr-hover-def-body {
  color: var(--text-muted);
}

/* ---------- Floating Focus Timer ---------- */
/* Moved to top-right so it stays visible while scrolling and out of the way of the bottom progress bar. */
.fr-floating-timer {
  position: fixed !important;
  top: 16px !important;
  right: 16px !important;
  bottom: auto !important;
  left: auto !important;
  background: var(--background-secondary);
  border: 1px solid var(--background-modifier-border);
  border-radius: 10px;
  padding: 10px 14px;
  min-width: 200px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
  z-index: 9990;
  font-size: 13px;
  opacity: 1;
  transition: opacity 0.3s;
  /* Ensure buttons stay clickable even when the box is dimmed by auto-hide. */
  pointer-events: auto;
}
.fr-timer-label {
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.fr-timer-time {
  font-size: 24px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  margin: 2px 0 6px;
}
.fr-timer-bar {
  height: 4px;
  background: var(--background-modifier-border);
  border-radius: 2px;
  overflow: hidden;
}
.fr-timer-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #66bb6a, #42a5f5);
  width: 0%;
  transition: width 0.3s;
}
.fr-timer-xp {
  margin-top: 4px;
  font-size: 11px;
  color: #ff9800;
  font-weight: 600;
}

/* ---------- Timer control buttons (Start / Pause / Stop) ---------- */
/* Clickable in-timer controls so the user doesn't need the Command Palette. */
.fr-timer-controls {
  display: flex;
  gap: 6px;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--background-modifier-border);
}
.fr-timer-btn {
  flex: 1;
  background: var(--background-modifier-border);
  color: var(--text-normal);
  border: 1px solid transparent;
  border-radius: 5px;
  padding: 5px 0;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.15s,
    transform 0.05s;
  user-select: none;
  -webkit-user-select: none;
}
.fr-timer-btn:hover:not(:disabled) {
  background: var(--background-modifier-border-hover, var(--interactive-accent-hover));
}
.fr-timer-btn:active:not(:disabled) {
  transform: scale(0.96);
}
.fr-timer-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.fr-timer-btn-primary {
  background: var(--interactive-accent);
  color: var(--text-on-accent);
}
.fr-timer-btn-primary:hover:not(:disabled) {
  background: var(--interactive-accent-hover);
  color: var(--text-on-accent);
}
.fr-timer-btn-stop:hover:not(:disabled) {
  background: #e53935;
  color: white;
  border-color: #c62828;
}

/* ---------- ADHD Nudge ---------- */
/* Centered modal with a dimmed backdrop so it's impossible to miss. */
.fr-adhd-nudge {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  bottom: auto !important;
  right: auto !important;
  transform: translate(-50%, -50%) !important;
  background: var(--background-secondary);
  border: 1px solid #ff9800;
  border-radius: 10px;
  padding: 18px 22px;
  /* The first box-shadow layer paints a translucent full-screen backdrop without needing a separate element. */
  box-shadow: 0 0 0 100vmax rgba(0, 0, 0, 0.45), 0 6px 20px rgba(0, 0, 0, 0.25);
  z-index: 9997;
  max-width: min(360px, 90vw);
  animation: fr-nudge-in 0.3s ease-out;
}
@keyframes fr-nudge-in {
  from {
    transform: translate(-50%, calc(-50% + 20px)) !important;
    opacity: 0;
  }
  to {
    transform: translate(-50%, -50%) !important;
    opacity: 1;
  }
}
.fr-nudge-title {
  font-weight: 600;
  margin-bottom: 4px;
}
.fr-nudge-body {
  color: var(--text-muted);
  font-size: 13px;
  margin-bottom: 10px;
}
.fr-nudge-actions {
  display: flex;
  gap: 8px;
}
.fr-nudge-actions button {
  background: var(--interactive-accent);
  color: var(--text-on-accent);
  border: none;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
}
.fr-nudge-actions button.fr-nudge-dismiss {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--background-modifier-border);
}

/* ---------- XP popup ---------- */
/* Stacked on the left so it doesn't fight the top-right timer. left: 60px clears the desktop workspace ribbon. */
.fr-xp-popup {
  position: fixed !important;
  top: 80px !important;
  left: 60px !important;
  right: auto !important;
  bottom: auto !important;
  background: linear-gradient(135deg, #ff9800, #ff5722);
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  box-shadow: 0 6px 20px rgba(255, 87, 34, 0.4);
  z-index: 9995;
  text-align: center;
  transform: translateY(-20px);
  opacity: 0;
  transition:
    transform 0.3s,
    opacity 0.3s;
}
.fr-xp-popup.fr-xp-show {
  transform: translateY(0);
  opacity: 1;
}
.fr-xp-amount {
  font-size: 20px;
  font-weight: 700;
}
.fr-xp-label {
  font-size: 11px;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ---------- Combo popup ---------- */
/* Stacked below XP popup on the left. */
.fr-combo-popup {
  position: fixed !important;
  top: 140px !important;
  left: 60px !important;
  right: auto !important;
  bottom: auto !important;
  background: linear-gradient(135deg, #9c27b0, #673ab7);
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  box-shadow: 0 6px 20px rgba(103, 58, 183, 0.4);
  z-index: 9995;
  text-align: center;
  transform: translateY(-20px);
  opacity: 0;
  transition:
    transform 0.3s,
    opacity 0.3s;
}
.fr-combo-popup.fr-combo-show {
  transform: translateY(0);
  opacity: 1;
}
.fr-combo-day {
  font-size: 18px;
  font-weight: 700;
}
.fr-combo-mult {
  font-size: 11px;
  opacity: 0.9;
}

/* ---------- Visual Completion ---------- */
.fr-completion {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0);
  z-index: 9996;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.4s;
}
.fr-completion.fr-completion-show {
  opacity: 1;
}
.fr-completion-inner {
  background: var(--background-secondary);
  border: 2px solid #66bb6a;
  border-radius: 12px;
  padding: 30px 40px;
  text-align: center;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  animation: fr-completion-pop 0.5s ease-out;
}
@keyframes fr-completion-pop {
  0% {
    transform: scale(0.6);
    opacity: 0;
  }
  60% {
    transform: scale(1.08);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
.fr-completion-title {
  font-size: 14px;
  color: #66bb6a;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.fr-completion-note {
  font-size: 22px;
  font-weight: 700;
  margin: 6px 0;
}
.fr-completion-stat {
  color: var(--text-muted);
  font-size: 13px;
}

/* ---------- Reading Dashboard ---------- */
.fr-dashboard {
  padding: 12px;
  font-size: 13px;
}
.fr-dash-section {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin: 14px 0 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid var(--background-modifier-border);
}
.fr-dash-section:first-child {
  margin-top: 0;
}
.fr-dash-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin: 4px 0;
}
.fr-dash-label {
  color: var(--text-muted);
}
.fr-dash-value {
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}
.fr-dash-bar-row {
  margin: 8px 0;
}
.fr-dash-bar {
  height: 6px;
  background: var(--background-modifier-border);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 4px;
}
.fr-dash-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #66bb6a, #42a5f5);
  transition: width 0.4s;
}
.fr-dash-achievements {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.fr-dash-ach {
  background: var(--background-modifier-border);
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 11px;
}

/* ---------- Heatmap ---------- */
.fr-heatmap {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-top: 4px;
}
.fr-heat-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.fr-heat-day {
  font-size: 9px;
  color: var(--text-muted);
}
.fr-heat-bar {
  width: 100%;
  height: 50px;
  background: var(--background-modifier-border);
  border-radius: 3px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}
.fr-heat-fill {
  width: 100%;
  background: #66bb6a;
  transition:
    height 0.3s,
    opacity 0.3s;
}
.fr-heat-min {
  font-size: 9px;
  color: var(--text-muted);
}

/* ---------- Settings tab helpers ---------- */
.fr-setting-hint {
  color: var(--text-muted);
  font-size: var(--font-ui-smaller);
  padding: 8px 0 0 0;
}
.fr-setting-ach-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 8px;
}
.fr-setting-ach {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  background: var(--background-secondary);
  border-radius: 4px;
}
.fr-setting-ach-icon {
  font-size: 16px;
}
.fr-setting-ach-name {
  font-weight: 600;
  flex: 0 0 140px;
}
.fr-setting-ach-desc {
  color: var(--text-muted);
  font-size: 12px;
}

/* ---------- Dark-theme tweaks ---------- */
body.theme-dark .fr-reading-ruler {
  border-top-color: rgba(255, 255, 255, 0.18);
  border-bottom-color: rgba(255, 255, 255, 0.18);
}

/* ---------- Bold highlight (Works in Reading and Live Preview) ---------- */
body.fr-bold-highlight-on .markdown-reading-view strong,
body.fr-bold-highlight-on .markdown-reading-view b,
body.fr-bold-highlight-on .markdown-source-view .cm-strong {
  background: var(--fr-bold-color);
  border-radius: 3px;
  padding: 0 3px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.04);
}

/* ---------- Typography polish (Applies font sizing to editor view as well) ---------- */
body.fr-typography-on .markdown-source-view .cm-content {
  font-size: var(--fr-font-size) !important;
  line-height: var(--fr-line-height) !important;
}
`;

const BODY_CLASSES = {
  typography: "fr-typography-on",
  ruler: "fr-ruler-on",
  boldHighlight: "fr-bold-highlight-on",
  definitions: "fr-definitions-on",
  bionic: "fr-bionic-on",
  focusMode: "fr-focus-mode",
  smartHighlight: "fr-smart-highlight-on",
  lineFocus: "fr-line-focus-on"
};

const AMBIENT_SOUNDS = [
  { id: "off", label: "Off", url: "" },
  { id: "rain", label: "Rain", url: "https://cdn.pixabay.com/audio/2022/03/15/audio_115b9eaf4e.mp3" },
  { id: "cafe", label: "Cafe", url: "https://cdn.pixabay.com/audio/2022/03/24/audio_7e9e8e95e6.mp3" },
  { id: "brown", label: "Brown Noise", url: "https://cdn.pixabay.com/audio/2022/10/30/audio_347111aaa2.mp3" },
  { id: "forest", label: "Forest", url: "https://cdn.pixabay.com/audio/2021/10/19/audio_99dfc3e03b.mp3" },
  { id: "white", label: "White Noise", url: "https://cdn.pixabay.com/audio/2022/03/10/audio_406722f53e.mp3" }
];

const ACHIEVEMENTS = [
  { id: "first_hour", name: "First Hour", desc: "Read for 60 minutes total.", check: stats => stats.totalReadingMs >= 3600000 },
  { id: "streak_7", name: "7-Day Streak", desc: "Read 7 days in a row.", check: stats => stats.streak >= 7 },
  { id: "notes_100", name: "100 Notes", desc: "Finish 100 notes.", check: stats => stats.notesCompleted >= 100 },
  { id: "ten_hours", name: "10 Hours", desc: "Read for 10 hours total.", check: stats => stats.totalReadingMs >= 36000000 },
  { id: "night_owl", name: "Night Owl", desc: "Read after 11pm.", check: stats => (new Date().getHours() >= 23 || new Date().getHours() < 4) },
  { id: "deep_focus", name: "Deep Focus", desc: "Single focus session over 20 min.", check: stats => stats.longestFocusMs >= 1200000 }
];

const MODULE_TOGGLES = [
  ["timerEnabled", "Module: Floating Focus Timer"],
  ["progressEnabled", "Module: Reading Progress Bar"],
  ["focusModeEnabled", "Module: Focus Mode"],
  ["heatmapEnabled", "Module: Reading Heatmap"],
  ["xpEnabled", "Module: XP System"],
  ["comboEnabled", "Module: Combo / Streak"],
  ["miniGoalsEnabled", "Module: Mini Goals"],
  ["curiosityEnabled", "Module: Random Curiosity Button"],
  ["ambientEnabled", "Module: Ambient Audio"],
  ["statsEnabled", "Module: Reading Statistics"],
  ["smartHighlightEnabled", "Module: Smart Highlight (Karaoke)"],
  ["lineFocusEnabled", "Module: Reading Line Focus"],
  ["hoverDefsEnabled", "Module: Hover Definitions"],
  ["rewardsEnabled", "Module: Reading Rewards"],
  ["journalEnabled", "Module: Session Journal"],
  ["nudgeEnabled", "Module: ADHD Nudge"],
  ["dopamineEnabled", "Module: Dopamine Bar"],
  ["readingSpeedEnabled", "Module: Reading Speed (WPM)"],
  ["achievementsEnabled", "Module: Achievements"],
  ["difficultyEnabled", "Module: Difficulty Meter"],
  ["focusDetectionEnabled", "Module: Focus Detection"],
  ["smoothScrollEnabled", "Module: Smooth Scrolling"],
  ["visualCompletionEnabled", "Module: Visual Completion"],
  ["dashboardEnabled", "Module: Reading Dashboard"]
];

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
  bionicEnabled: false,
  bionicRatio: 0.4,
  bionicMinWordLength: 4,
  readingRulerEnabled: false,
  readingRulerHeight: 28,
  readingRulerColor: "#ffd54f",
  readingRulerOpacity: 0.18,
  typographyEnabled: true,
  fontFamily: "system",
  customFontFamily: "",
  loadGoogleFonts: false,
  fontSize: 17,
  lineHeight: 1.7,
  maxWidthChars: 66,
  paragraphSpacing: 1.4,
  colorizeDefinitions: false,
  definitionColor: "#e8f5e9",
  highlightBold: false,
  boldHighlightColor: "#fff8c4",
  autoFoldOnOpen: false,
  ttsRate: 1,
  ttsPitch: 1,
  ttsVoiceURI: "",
  timerEnabled: false,
  timerWorkMinutes: 25,
  timerBreakMinutes: 5,
  timerAutoHide: true,
  timerAutoHideSeconds: 4,
  timerPauseOnBlur: true,
  progressEnabled: false,
  progressEstimateRemaining: true,
  progressShowSectionsLeft: true,
  focusModeEnabled: false,
  heatmapEnabled: false,
  xpEnabled: false,
  comboEnabled: false,
  miniGoalsEnabled: false,
  curiosityEnabled: false,
  ambientEnabled: false,
  ambientVolume: 0.5,
  ambientSound: "off",
  statsEnabled: false,
  smartHighlightEnabled: false,
  lineFocusEnabled: false,
  lineFocusLines: 3,
  lineFocusOpacity: 0.35,
  hoverDefsEnabled: false,
  rewardsEnabled: false,
  journalEnabled: false,
  journalFolder: "Reading Journal",
  nudgeEnabled: false,
  nudgeIdleSeconds: 60,
  dopamineEnabled: false,
  dopamineDailyGoalMinutes: 60,
  readingSpeedEnabled: false,
  achievementsEnabled: false,
  difficultyEnabled: false,
  focusDetectionEnabled: false,
  focusDetectionIdleSeconds: 30,
  smoothScrollEnabled: false,
  smoothScrollSpeed: 40,
  visualCompletionEnabled: false,
  dashboardEnabled: false,
  dashboardPosition: "right"
};

const DEFAULT_STATS = {
  totalReadingMs: 0,
  todayMs: 0,
  todayDate: "",
  wordsRead: 0,
  notesCompleted: 0,
  xp: 0,
  level: 1,
  streak: 0,
  lastReadDate: "",
  longestStreak: 0,
  perDayMs: {},
  perNoteMs: {},
  perNoteProgress: {},
  achievements: [],
  wpmSamples: [],
  sessionsToday: 0,
  longestFocusMs: 0,
  currentComboMultiplier: 1
};

// Date & Time Utility Helpers
function formatDate(date) {
  const d = date || new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function dayDiff(startStr, endStr) {
  if (!startStr || !endStr) return 0;
  const start = new Date(startStr + "T00:00:00");
  const end = new Date(endStr + "T00:00:00");
  return Math.round((end.getTime() - start.getTime()) / 86400000);
}

// Deep-clone a plain object/array so nested arrays (achievements, wpmSamples, perDayMs, ...)
// never share references with the DEFAULT_STATS template across plugin reloads.
function deepClone(obj) {
  if (obj === null || typeof obj !== "object") return obj;
  if (Array.isArray(obj)) return obj.map(deepClone);
  const out = {};
  for (const key of Object.keys(obj)) out[key] = deepClone(obj[key]);
  return out;
}

// Text & Difficulty Analyzer
function analyzeText(text, avgWpm = 220) {
  const words = (text.match(/\b[\p{L}\p{N}'’-]+\b/gu) || []).length;
  const headings = (text.match(/^#{1,6}\s+/gm) || []).length;
  const headingMatches = text.match(/^#+/gm);
  const headingDepth = headingMatches ? Math.max(...headingMatches.map(h => h.length)) : 0;
  const codeBlocks = (text.match(/```[\s\S]*?```/g) || []).length;
  const mathBlocks = (text.match(/\$\$[\s\S]*?\$\$/g) || []).length;
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const avgSentenceLength = sentences.length ? words / sentences.length : 0;

  let difficultyScore = 0;
  if (headingDepth >= 4) difficultyScore += 2;
  else if (headingDepth >= 3) difficultyScore += 1;

  if (codeBlocks >= 5) difficultyScore += 2;
  else if (codeBlocks >= 1) difficultyScore += 1;

  if (mathBlocks >= 3) difficultyScore += 2;
  else if (mathBlocks >= 1) difficultyScore += 1;

  if (avgSentenceLength > 28) difficultyScore += 1;
  if (words > 2500) difficultyScore += 1;

  const difficulty = difficultyScore >= 5 ? "Hard" : difficultyScore >= 2 ? "Medium" : "Easy";
  const estimatedMinutes = Math.max(1, Math.round(words / Math.max(80, avgWpm)));

  return { words, headings, headingDepth, codeBlocks, mathBlocks, avgSentenceLength, difficulty, estimatedMinutes };
}

function stripMarkdown(text) {
  let output = text;
  output = output.replace(/```[\s\S]*?```/g, " (code block) ");
  output = output.replace(/`([^`]+)`/g, "$1");
  output = output.replace(/!\[[^\]]*\]\([^)]*\)/g, " (image) ");
  output = output.replace(/\[\[([^\]]+)\]\]/g, "$1");
  output = output.replace(/\[([^\]]+)\]\([^)]*\)/g, "$1");
  output = output.replace(/^#{1,6}\s+/gm, "");
  output = output.replace(/^>\s?/gm, "");
  output = output.replace(/^\s*[-*+]\s+/gm, "");
  output = output.replace(/\*\*([^*]+)\*\*/g, "$1");
  output = output.replace(/\*([^*]+)\*/g, "$1");
  output = output.replace(/__([^_]+)__/g, "$1");
  output = output.replace(/_([^_]+)_/g, "$1");
  output = output.replace(/~~([^~]+)~~/g, "$1");
  output = output.replace(/==([^=]+)==/g, "$1");
  output = output.replace(/^\|.*\|$/gm, " ");
  output = output.replace(/\n{3,}/g, "\n\n");
  return output;
}

// XP System Helpers
function xpForLevel(level) {
  return Math.round(100 * Math.pow(level, 1.5));
}

function getLevelInfo(xp) {
  let level = 1;
  while (xp >= xpForLevel(level + 1)) {
    level++;
  }
  const currentLevelXp = xpForLevel(level);
  const nextLevelXp = xpForLevel(level + 1);
  const into = xp - currentLevelXp;
  const need = nextLevelXp - currentLevelXp;
  return { level, into, need };
}

// GameManager Class — Sound and Visual popups
class GameManager {
  constructor(app, getSettings) {
    this.app = app;
    this.getSettings = getSettings;
    this.audioEl = null;
  }

  showXpPopup(amount, label = "Focused Reading") {
    if (!this.getSettings().xpEnabled) return;
    const popup = document.createElement("div");
    popup.className = "fr-xp-popup";
    popup.innerHTML = `<div class="fr-xp-amount">+${amount} XP</div><div class="fr-xp-label">${label}</div>`;
    document.body.appendChild(popup);
    setTimeout(() => popup.classList.add("fr-xp-show"), 10);
    setTimeout(() => {
      popup.classList.remove("fr-xp-show");
      setTimeout(() => popup.remove(), 400);
    }, 1800);
  }

  showComboPopup(streak, multiplier) {
    if (!this.getSettings().comboEnabled) return;
    const popup = document.createElement("div");
    popup.className = "fr-combo-popup";
    popup.innerHTML = `<div class="fr-combo-day">Day ${streak}</div><div class="fr-combo-mult">x${multiplier.toFixed(1)} multiplier</div>`;
    document.body.appendChild(popup);
    setTimeout(() => popup.classList.add("fr-combo-show"), 10);
    setTimeout(() => {
      popup.classList.remove("fr-combo-show");
      setTimeout(() => popup.remove(), 400);
    }, 2200);
  }

  showCompletion(title, xp, wordCount) {
    if (!this.getSettings().visualCompletionEnabled) return;
    const completion = document.createElement("div");
    completion.className = "fr-completion";
    completion.innerHTML = `<div class="fr-completion-inner"><div class="fr-completion-title">Completed</div><div class="fr-completion-note">${title}</div><div class="fr-completion-stat">100% · +${xp} XP · ${wordCount.toLocaleString()} words</div></div>`;
    document.body.appendChild(completion);
    setTimeout(() => completion.classList.add("fr-completion-show"), 10);
    setTimeout(() => {
      completion.classList.remove("fr-completion-show");
      setTimeout(() => completion.remove(), 600);
    }, 2500);
  }

  setAmbient(id) {
    const settings = this.getSettings();
    if (!settings.ambientEnabled || id === "off") {
      this.stopAmbient();
      return;
    }
    const sound = AMBIENT_SOUNDS.find(s => s.id === id);
    if (sound) {
      if (!this.audioEl) {
        this.audioEl = new Audio();
        this.audioEl.loop = true;
      }
      if (this.audioEl.src !== sound.url) {
        this.audioEl.src = sound.url;
        this.audioEl.volume = settings.ambientVolume;
        this.audioEl.play().catch(() => {
          new Notice("Could not play ambient sound. Click anywhere in Obsidian first.");
        });
      }
    }
  }

  stopAmbient() {
    if (this.audioEl) {
      this.audioEl.pause();
      this.audioEl.src = "";
    }
  }

  setVolume(vol) {
    if (this.audioEl) {
      this.audioEl.volume = vol;
    }
  }
}

// StatsManager Class
class StatsManager {
  constructor(app, getSettings, getStats, saveStats) {
    this.app = app;
    this.getSettings = getSettings;
    this.getStats = getStats;
    this.saveStats = saveStats;
  }

  rollOver() {
    const stats = this.getStats();
    const today = formatDate();
    if (stats.todayDate !== today) {
      if (stats.lastReadDate) {
        const diff = dayDiff(stats.lastReadDate, today);
        if (diff === 1) {
          stats.streak += 1;
        } else if (diff > 1) {
          stats.streak = 1;
        }
      } else {
        stats.streak = 1;
      }
      stats.longestStreak = Math.max(stats.longestStreak, stats.streak);
      stats.todayMs = 0;
      stats.sessionsToday = 0;
      stats.wordsRead = 0;
      stats.todayDate = today;
    }
  }

  async addReadingTime(ms, file) {
    const stats = this.getStats();
    this.rollOver();
    stats.totalReadingMs += ms;
    stats.todayMs += ms;
    stats.lastReadDate = formatDate();

    const todayStr = formatDate();
    stats.perDayMs[todayStr] = (stats.perDayMs[todayStr] || 0) + ms;
    if (file) {
      stats.perNoteMs[file.path] = (stats.perNoteMs[file.path] || 0) + ms;
    }

    if (this.getSettings().xpEnabled) {
      const xpGained = Math.max(1, Math.round(ms / 60000));
      stats.xp += xpGained;
      const lvlInfo = getLevelInfo(stats.xp);
      if (lvlInfo.level > stats.level) {
        stats.level = lvlInfo.level;
        new Notice(`Level Up! You are now level ${lvlInfo.level}.`);
      }
    }

    if (this.getSettings().comboEnabled) {
      stats.currentComboMultiplier = 1 + Math.min(stats.streak, 30) * 0.1;
    }

    const hour = new Date().getHours();
    if (hour >= 23 || hour < 4) {
      if (!stats.achievements.includes("night_owl")) {
        stats.achievements.push("night_owl");
        new Notice("Achievement unlocked: Night Owl");
      }
    }

    await this.checkAchievements();
    await this.saveStats(stats);
  }

  async addWordsRead(count) {
    const stats = this.getStats();
    this.rollOver();
    stats.wordsRead += count;
    await this.saveStats(stats);
  }

  async markNoteCompleted(file) {
    const stats = this.getStats();
    this.rollOver();
    stats.notesCompleted += 1;
    if (this.getSettings().xpEnabled) {
      stats.xp += 50;
      new Notice("Note completed! +50 XP");
    }
    await this.checkAchievements();
    await this.saveStats(stats);
  }

  async setNoteProgress(file, progress) {
    const stats = this.getStats();
    stats.perNoteProgress[file.path] = Math.max(stats.perNoteProgress[file.path] || 0, progress);
    await this.saveStats(stats);
  }

  async recordLongestFocus(ms) {
    const stats = this.getStats();
    if (ms > stats.longestFocusMs) {
      stats.longestFocusMs = ms;
      await this.saveStats(stats);
    }
  }

  async recordWpm(wpm) {
    if (wpm <= 0 || wpm > 1000) return;
    const stats = this.getStats();
    stats.wpmSamples.push(wpm);
    if (stats.wpmSamples.length > 200) {
      stats.wpmSamples = stats.wpmSamples.slice(-200);
    }
    await this.saveStats(stats);
  }

  async checkAchievements() {
    if (!this.getSettings().achievementsEnabled) return;
    const stats = this.getStats();
    let hasNew = false;
    for (const ach of ACHIEVEMENTS) {
      if (!stats.achievements.includes(ach.id)) {
        if (ach.check(stats)) {
          stats.achievements.push(ach.id);
          new Notice(`Achievement unlocked: ${ach.name}`);
          hasNew = true;
        }
      }
    }
    if (hasNew) {
      await this.saveStats(stats);
    }
  }

  getAverageWpm() {
    const stats = this.getStats();
    if (!stats.wpmSamples.length) return 220;
    const sum = stats.wpmSamples.reduce((a, b) => a + b, 0);
    return Math.round(sum / stats.wpmSamples.length);
  }
}

// TimerManager Class
class TimerManager {
  constructor(app, getSettings, onStatsAdd, onSessionEnd) {
    this.app = app;
    this.getSettings = getSettings;
    this.onStatsAdd = onStatsAdd;
    this.onSessionEnd = onSessionEnd;
    this.timerEl = null;
    this.state = "idle";
    this.remainingMs = 0;
    this.totalMs = 0;
    this.raf = null;
    this.lastTick = 0;
    this.accumulatedMs = 0;
    this.lastActivity = Date.now();
    this.windowFocused = true;
    this.autoHideTimer = null;
    this.onTickCb = null;
    this.onCompleteCb = null;
    this.onActivityCb = null;
    this.idleCheckInterval = null;
    this.progressWrap = null;
    this.progressFill = null;
    this.progressInfo = null;
    this.tick = this.tick.bind(this);
  }

  load() {
    this.timerEl = document.createElement("div");
    this.timerEl.id = FLOATING_TIMER_ID;
    this.timerEl.className = "fr-floating-timer";
    this.timerEl.style.display = "none";
    this.timerEl.innerHTML = `
      <div class="fr-timer-label">Reading</div>
      <div class="fr-timer-time">00:00</div>
      <div class="fr-timer-bar"><div class="fr-timer-bar-fill"></div></div>
      <div class="fr-timer-xp"></div>
      <div class="fr-timer-controls">
        <button class="fr-timer-btn fr-timer-btn-primary" data-action="start">Start</button>
        <button class="fr-timer-btn" data-action="pause">Pause</button>
        <button class="fr-timer-btn fr-timer-btn-stop" data-action="stop">Stop</button>
      </div>
    `;
    document.body.appendChild(this.timerEl);

    // Wire up the in-timer buttons so the user can Start/Pause/Resume/Stop
    // directly from the floating box — no Command Palette needed.
    const controlsEl = this.timerEl.querySelector(".fr-timer-controls");
    if (controlsEl) {
      controlsEl.addEventListener("click", e => {
        const btn = e.target.closest(".fr-timer-btn");
        if (!btn) return;
        // Stop the click from bubbling up — otherwise it could re-trigger auto-hide
        // timers in a way that immediately dims the box right after a click.
        e.stopPropagation();
        const action = btn.getAttribute("data-action");
        this.handleControlClick(action);
      });
    }

    // Render the initial idle state so the timer box looks correct the moment it's shown.
    this.renderTimer();

    const events = ["mousemove", "keydown", "scroll", "touchstart"];
    events.forEach(evt => {
      window.addEventListener(evt, () => this.onActivity(), { passive: true });
    });

    window.addEventListener("blur", () => {
      this.windowFocused = false;
      if (this.getSettings().timerPauseOnBlur && this.state === "running") {
        this.pause("Window lost focus");
      }
    });

    window.addEventListener("focus", () => {
      this.windowFocused = true;
      this.onActivity();
    });

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        if (this.getSettings().timerPauseOnBlur && this.state === "running") {
          this.pause("Tab hidden");
        }
      } else {
        this.onActivity();
      }
    });

    this.idleCheckInterval = window.setInterval(() => this.checkIdle(), 5000);

    const style = document.createElement("style");
    style.id = PROGRESS_STYLE_ID;
    style.textContent = `
      .fr-progress-bar-wrap { position: fixed !important; bottom: 0 !important; top: auto !important; left: 0 !important; right: 0 !important; height: 4px; background: transparent; z-index: 9998; pointer-events: none; }
      .fr-progress-bar-fill { height: 100%; background: linear-gradient(90deg, #66bb6a, #42a5f5); width: 0%; transition: width 0.2s; }
      .fr-progress-info { position: fixed !important; bottom: 10px !important; top: auto !important; right: 8px !important; left: auto !important; font-size: 11px; color: var(--text-muted); z-index: 9998; pointer-events: none; }
    `;
    document.head.appendChild(style);
  }

  onTick(cb) { this.onTickCb = cb; }
  onComplete(cb) { this.onCompleteCb = cb; }
  setActivityCallback(cb) { this.onActivityCb = cb; }

  applyVisibility() {
    if (!this.timerEl) return;
    if (!this.getSettings().timerEnabled) {
      // Module is off — fully hide and stop any running session.
      this.timerEl.style.display = "none";
      this.stop();
      return;
    }
    // Module is ON — always show the timer box so the user can see it's active.
    // Previously this hid the box whenever state was "idle", which made toggling the
    // setting appear to do nothing (the user had to know to run "Start Focus Session").
    this.show();
    this.renderTimer();
  }

  start() {
    const settings = this.getSettings();
    if (!settings.timerEnabled) {
      new Notice("Enable the Floating Focus Timer module first (Settings → Focus Read, or the “Toggle: Module: Floating Focus Timer” command).");
      return;
    }
    this.totalMs = settings.timerWorkMinutes * 60000;
    this.remainingMs = this.totalMs;
    this.state = "running";
    this.lastTick = performance.now();
    this.accumulatedMs = 0;
    this.show();
    this.tick();
    new Notice(`Focus session started: ${settings.timerWorkMinutes} min`);
  }

  // Central handler for the in-timer Start/Pause/Stop buttons.
  // Maps the single "Pause" button to the right action depending on current state:
  //   running  → pause
  //   paused   → resume
  //   idle/break → no-op (button is disabled in those states)
  handleControlClick(action) {
    if (action === "start") {
      // From idle → start fresh. From break → cut the break short and start a focus session.
      this.start();
    } else if (action === "pause") {
      if (this.state === "running") {
        this.pause();
        this.renderTimer();
      } else if (this.state === "paused") {
        this.resume();
        this.renderTimer();
      }
    } else if (action === "stop") {
      if (this.state !== "idle") {
        this.stop();
        this.renderTimer();
        new Notice("Timer stopped.");
      }
    }
  }

  pause(reason) {
    if (this.state === "running") {
      this.state = "paused";
      if (this.raf) {
        cancelAnimationFrame(this.raf);
        this.raf = null;
      }
      if (reason) {
        new Notice(`Paused: ${reason}`);
      }
    }
  }

  resume() {
    if (this.state === "paused") {
      this.state = "running";
      this.lastTick = performance.now();
      this.tick();
    }
  }

  stop() {
    if (this.raf) {
      cancelAnimationFrame(this.raf);
      this.raf = null;
    }
    this.state = "idle";
    this.remainingMs = 0;
    // Don't unconditionally hide the timer element here. Visibility is owned by
    // applyVisibility(). If the module is still enabled we want to keep showing
    // the idle "Ready" box so the user knows the timer is still armed — only
    // hide when the user has actually disabled the module.
    if (this.timerEl) {
      if (!this.getSettings().timerEnabled) {
        this.timerEl.style.display = "none";
      } else {
        this.renderTimer();
      }
    }
  }

  isRunning() {
    return this.state === "running";
  }

  getElapsedMs() {
    return this.accumulatedMs;
  }

  getState() {
    return this.state;
  }

  getRemainingMs() {
    return this.remainingMs;
  }

  tick() {
    if (this.state !== "running" && this.state !== "break") return;
    const now = performance.now();
    const elapsed = now - this.lastTick;
    this.lastTick = now;
    this.remainingMs = Math.max(0, this.remainingMs - elapsed);

    const settings = this.getSettings();
    const isFocused = !settings.focusDetectionEnabled || 
      (this.windowFocused && (Date.now() - this.lastActivity < settings.focusDetectionIdleSeconds * 1000));

    // Only accumulate focus time and reading stats during an actual focus session, not a break.
    if (this.state === "running" && isFocused) {
      this.accumulatedMs += elapsed;
      const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
      this.onStatsAdd(elapsed, activeView ? activeView.file : null);
    }

    this.renderTimer();
    if (this.onTickCb) this.onTickCb();

    if (this.remainingMs <= 0) {
      this.complete();
      return;
    }
    this.raf = requestAnimationFrame(this.tick);
  }

  complete() {
    const isBreak = this.state === "break";
    const accumulated = this.accumulatedMs;
    this.stop();
    // Only fire session-end stats/XP/journal once — when the focus session ends, not when the break ends.
    if (!isBreak) {
      this.onSessionEnd(accumulated);
    }
    if (this.onCompleteCb) this.onCompleteCb(isBreak);
    if (isBreak) {
      new Notice("Break over. Ready for another session?");
    } else {
      new Notice("Focus session complete! Take a break.");
      this.startBreak();
    }
  }

  startBreak() {
    const settings = this.getSettings();
    if (!settings.timerEnabled) return;
    this.totalMs = settings.timerBreakMinutes * 60000;
    this.remainingMs = this.totalMs;
    this.state = "break";
    this.lastTick = performance.now();
    // Reset accumulation so break time isn't mixed into the next session's focus stats.
    this.accumulatedMs = 0;
    this.show();
    this.tick();
  }

  show() {
    if (this.getSettings().timerEnabled && this.timerEl) {
      this.timerEl.style.display = "block";
      this.resetAutoHide();
    }
  }

  resetAutoHide() {
    const settings = this.getSettings();
    if (settings.timerAutoHide) {
      if (this.autoHideTimer) clearTimeout(this.autoHideTimer);
      this.autoHideTimer = window.setTimeout(() => {
        // Only dim when truly idle (not during an active focus session or break countdown).
        // Keep opacity at 0.55 so the Start button stays readable/clickable — full dim
        // would make the in-timer controls useless when the user comes back to start a session.
        if (this.timerEl && this.state === "idle") {
          this.timerEl.style.opacity = "0.55";
        }
      }, settings.timerAutoHideSeconds * 1000);
    }
  }

  onActivity() {
    this.lastActivity = Date.now();
    if (this.timerEl) {
      this.timerEl.style.opacity = "1";
      this.resetAutoHide();
    }
    this.hideNudge();
    if (this.onActivityCb) this.onActivityCb();
  }

  checkIdle() {
    const settings = this.getSettings();
    if (settings.nudgeEnabled && (Date.now() - this.lastActivity >= settings.nudgeIdleSeconds * 1000) && this.state === "running") {
      this.showNudge();
    }
  }

  showNudge() {
    if (document.getElementById(ADHD_NUDGE_ID)) return;
    const nudge = document.createElement("div");
    nudge.id = ADHD_NUDGE_ID;
    nudge.className = "fr-adhd-nudge";
    const minLeft = Math.ceil(this.remainingMs / 60000);
    nudge.innerHTML = `
      <div class="fr-nudge-title">You stopped reading.</div>
      <div class="fr-nudge-body">Continue? ${minLeft} min left in session.</div>
      <div class="fr-nudge-actions">
        <button class="fr-nudge-continue">Continue</button>
        <button class="fr-nudge-dismiss">Dismiss</button>
      </div>
    `;
    document.body.appendChild(nudge);

    const continueBtn = nudge.querySelector(".fr-nudge-continue");
    if (continueBtn) {
      continueBtn.addEventListener("click", () => {
        this.onActivity();
        nudge.remove();
      });
    }
    const dismissBtn = nudge.querySelector(".fr-nudge-dismiss");
    if (dismissBtn) {
      dismissBtn.addEventListener("click", () => {
        nudge.remove();
      });
    }
  }

  hideNudge() {
    const nudge = document.getElementById(ADHD_NUDGE_ID);
    if (nudge) nudge.remove();
  }

  renderTimer() {
    if (!this.timerEl) return;
    const settings = this.getSettings();

    // Helper: update the Start / Pause / Stop buttons to match the current state.
    // The single "Pause" button relabels to "Resume" when paused so the user knows
    // it doubles as the resume control.
    const updateButtons = (state) => {
      const startBtn = this.timerEl.querySelector('[data-action="start"]');
      const pauseBtn = this.timerEl.querySelector('[data-action="pause"]');
      const stopBtn = this.timerEl.querySelector('[data-action="stop"]');

      if (startBtn) {
        // Start button is enabled when idle (start fresh) or during a break (skip break).
        const startEnabled = state === "idle" || state === "break";
        startBtn.disabled = !startEnabled;
        startBtn.textContent = state === "break" ? "Skip Break" : "Start";
      }
      if (pauseBtn) {
        if (state === "running") {
          pauseBtn.disabled = false;
          pauseBtn.textContent = "Pause";
        } else if (state === "paused") {
          pauseBtn.disabled = false;
          pauseBtn.textContent = "Resume";
        } else {
          // idle or break — pausing doesn't make sense
          pauseBtn.disabled = true;
          pauseBtn.textContent = "Pause";
        }
      }
      if (stopBtn) {
        // Stop only makes sense when something is actually running.
        stopBtn.disabled = state === "idle";
      }
    };

    // Idle state: show a clear "Ready" box with the configured work duration and a
    // hint about how to start. Previously the timer rendered 00:00 / "+0 XP" while
    // idle, which looked like the timer was broken.
    if (this.state === "idle") {
      const labelDiv = this.timerEl.querySelector(".fr-timer-label");
      if (labelDiv) labelDiv.textContent = "Ready";

      const timeDiv = this.timerEl.querySelector(".fr-timer-time");
      if (timeDiv) {
        const workMins = settings.timerWorkMinutes;
        timeDiv.textContent = `${String(workMins).padStart(2, "0")}:00`;
      }

      const fillBar = this.timerEl.querySelector(".fr-timer-bar-fill");
      if (fillBar) fillBar.style.width = "0%";

      const xpDiv = this.timerEl.querySelector(".fr-timer-xp");
      if (xpDiv) xpDiv.textContent = "Click Start to begin";
      updateButtons("idle");
      return;
    }

    const totalSeconds = Math.ceil(this.remainingMs / 1000);
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    const timeStr = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;

    const timeDiv = this.timerEl.querySelector(".fr-timer-time");
    if (timeDiv) timeDiv.textContent = timeStr;

    const labelDiv = this.timerEl.querySelector(".fr-timer-label");
    if (labelDiv) {
      if (this.state === "break") labelDiv.textContent = "Break";
      else if (this.state === "paused") labelDiv.textContent = "Paused";
      else labelDiv.textContent = "Reading";
    }

    const percent = this.totalMs > 0 ? (1 - this.remainingMs / this.totalMs) * 100 : 0;
    const fillBar = this.timerEl.querySelector(".fr-timer-bar-fill");
    if (fillBar) fillBar.style.width = `${percent}%`;

    const minAccumulated = Math.round(this.accumulatedMs / 60000);
    const xpDiv = this.timerEl.querySelector(".fr-timer-xp");
    if (xpDiv) {
      if (this.state === "break") {
        xpDiv.textContent = "On break";
      } else {
        xpDiv.textContent = `+${minAccumulated} XP`;
      }
    }
    updateButtons(this.state);
  }

  attachProgress() {
    if (!this.getSettings().progressEnabled) {
      this.detachProgress();
      return;
    }
    if (!this.progressWrap) {
      this.progressWrap = document.createElement("div");
      this.progressWrap.className = "fr-progress-bar-wrap";
      this.progressFill = document.createElement("div");
      this.progressFill.className = "fr-progress-bar-fill";
      this.progressWrap.appendChild(this.progressFill);

      this.progressInfo = document.createElement("div");
      this.progressInfo.className = "fr-progress-info";

      document.body.appendChild(this.progressWrap);
      document.body.appendChild(this.progressInfo);

      this.scrollHandler = () => this.updateProgress();
      window.addEventListener("scroll", this.scrollHandler, { passive: true });
      window.addEventListener("resize", this.scrollHandler);
      this.app.workspace.on("layout-change", this.scrollHandler);
    }
    this.updateProgress();
  }

  detachProgress() {
    if (this.progressWrap) this.progressWrap.remove();
    if (this.progressInfo) this.progressInfo.remove();
    this.progressWrap = null;
    this.progressFill = null;
    this.progressInfo = null;
    if (this.scrollHandler) {
      window.removeEventListener("scroll", this.scrollHandler);
      window.removeEventListener("resize", this.scrollHandler);
      this.app.workspace.off("layout-change", this.scrollHandler);
    }
  }

  updateProgress() {
    const settings = this.getSettings();
    if (!settings.progressEnabled || !this.progressFill) return;
    const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!activeView) {
      this.progressWrap.style.display = "none";
      this.progressInfo.style.display = "none";
      return;
    }
    this.progressWrap.style.display = "block";
    this.progressInfo.style.display = "block";

    const doc = document.documentElement;
    const limit = doc.scrollHeight - doc.clientHeight;
    const percent = limit > 0 ? (doc.scrollTop / limit) * 100 : 100;
    this.progressFill.style.width = `${percent}%`;

    const remainingPercent = 100 - percent;
    const progressText = `${Math.round(percent)}%`;

    if (settings.progressEstimateRemaining && activeView.file) {
      this.app.vault.cachedRead(activeView.file).then(content => {
        const words = (content.match(/\b\w+\b/g) || []).length;
        const wordsLeft = Math.round((remainingPercent / 100) * words);
        const minsLeft = Math.max(1, Math.round(wordsLeft / 220));
        let label = `${progressText} · ~${minsLeft} min left`;
        if (settings.progressShowSectionsLeft) {
          const sections = (content.match(/^#{1,6}\s+/gm) || []).length;
          label += ` · ${sections} sections`;
        }
        if (this.progressInfo) this.progressInfo.textContent = label;
      });
    } else if (settings.progressShowSectionsLeft && activeView.file) {
      this.app.vault.cachedRead(activeView.file).then(content => {
        const sections = (content.match(/^#{1,6}\s+/gm) || []).length;
        if (this.progressInfo) this.progressInfo.textContent = `${progressText} · ${sections} sections`;
      });
    } else {
      if (this.progressInfo) this.progressInfo.textContent = progressText;
    }
  }

  unload() {
    this.stop();
    if (this.timerEl) this.timerEl.remove();
    this.timerEl = null;
    this.detachProgress();
    const nudge = document.getElementById(ADHD_NUDGE_ID);
    if (nudge) nudge.remove();
    const pStyle = document.getElementById(PROGRESS_STYLE_ID);
    if (pStyle) pStyle.remove();
    if (this.idleCheckInterval) clearInterval(this.idleCheckInterval);
  }
}

// VisualManager Class — Visual adjustments and reading aids
class VisualManager {
  constructor(app, getSettings) {
    this.app = app;
    this.getSettings = getSettings;
    this.rulerEl = null;
    this.smartHighlightCleanup = null;
    this.lineFocusCleanup = null;
    this.hoverDefsCleanup = null;
    this.smoothScrollState = { active: false, raf: null };
    this.boundRulerMove = this.onRulerMove.bind(this);
  }

  load(plugin) {
    this.rulerEl = document.createElement("div");
    this.rulerEl.id = READING_RULER_ID;
    this.rulerEl.className = "fr-reading-ruler";
    document.body.appendChild(this.rulerEl);
    window.addEventListener("mousemove", this.boundRulerMove);
    plugin.register(() => window.removeEventListener("mousemove", this.boundRulerMove));
  }

  applyAll() {
    this.applyGoogleFonts();
    this.applyTypography();
    this.applyRuler();
    this.applyBodyClasses();
    this.applySmartHighlight();
    this.applyLineFocus();
  }

  applyBodyClasses() {
    const settings = this.getSettings();
    document.body.classList.toggle(BODY_CLASSES.typography, settings.typographyEnabled);
    document.body.classList.toggle(BODY_CLASSES.ruler, settings.readingRulerEnabled);
    document.body.classList.toggle(BODY_CLASSES.boldHighlight, settings.highlightBold);
    document.body.classList.toggle(BODY_CLASSES.definitions, settings.colorizeDefinitions);
    document.body.classList.toggle(BODY_CLASSES.bionic, settings.bionicEnabled);
    document.body.classList.toggle(BODY_CLASSES.focusMode, settings.focusModeEnabled);
    document.body.classList.toggle(BODY_CLASSES.smartHighlight, settings.smartHighlightEnabled);
    document.body.classList.toggle(BODY_CLASSES.lineFocus, settings.lineFocusEnabled);
  }

  applyGoogleFonts() {
    const existing = document.getElementById(GOOGLE_FONTS_STYLE_ID);
    if (existing) existing.remove();
    if (!this.getSettings().loadGoogleFonts) return;

    const families = ["Lexend", "Atkinson+Hyperlegible", "Inter", "Source+Sans+3", "IBM+Plex+Sans", "Noto+Sans"];
    const query = families.map(f => `family=${f}`).join("&") + "&display=swap";
    const url = "https://fonts.googleapis.com/css2?" + query;

    const style = document.createElement("style");
    style.id = GOOGLE_FONTS_STYLE_ID;
    style.textContent = `@import url('${url}');`;
    document.head.appendChild(style);
  }

  resolveFontStack() {
    const settings = this.getSettings();
    if (settings.fontFamily === "custom") {
      return settings.customFontFamily || "";
    }
    return FONT_STACK_BY_ID[settings.fontFamily] || "";
  }

  applyTypography() {
    let style = document.getElementById(TYPOGRAPHY_STYLE_ID);
    if (!style) {
      style = document.createElement("style");
      style.id = TYPOGRAPHY_STYLE_ID;
      document.head.appendChild(style);
    }
    const settings = this.getSettings();
    const stack = this.resolveFontStack();
    const cssRules = [];

    cssRules.push(":root {");
    cssRules.push(`  --fr-font-size: ${settings.fontSize}px;`);
    cssRules.push(`  --fr-line-height: ${settings.lineHeight};`);
    cssRules.push(`  --fr-para-spacing: ${settings.paragraphSpacing};`);
    cssRules.push(`  --fr-max-width: ${settings.maxWidthChars}ch;`);
    cssRules.push(`  --fr-font-family: ${stack};`);
    cssRules.push(`  --fr-def-color: ${settings.definitionColor};`);
    cssRules.push(`  --fr-bold-color: ${settings.boldHighlightColor};`);
    cssRules.push(`  --fr-line-focus-opacity: ${settings.lineFocusOpacity};`);
    cssRules.push(`  --fr-line-focus-lines: ${settings.lineFocusLines};`);
    cssRules.push("}");

    cssRules.push(`body.fr-typography-on .markdown-reading-view .markdown-preview-section {
      font-size: var(--fr-font-size) !important;
      line-height: var(--fr-line-height) !important;
      ${stack ? "font-family: var(--fr-font-family) !important;" : ""}
      max-width: var(--fr-max-width) !important;
      margin-left: auto !important;
      margin-right: auto !important;
    }`);

    cssRules.push(`body.fr-typography-on .markdown-reading-view p,
    body.fr-typography-on .markdown-reading-view li {
      ${stack ? "font-family: var(--fr-font-family) !important;" : ""}
    }`);

    cssRules.push(`body.fr-typography-on .markdown-reading-view p {
      margin-bottom: calc(var(--fr-font-size) * (var(--fr-para-spacing) - 1)) !important;
    }`);

    cssRules.push(`body.fr-typography-on .markdown-source-view .cm-content {
      ${stack ? "font-family: var(--fr-font-family) !important;" : ""}
      max-width: var(--fr-max-width) !important;
      font-size: var(--fr-font-size) !important;
      line-height: var(--fr-line-height) !important;
    }`);

    cssRules.push(`body.fr-typography-on .markdown-source-view .cm-line {
      max-width: var(--fr-max-width) !important;
    }`);

    style.textContent = cssRules.join("\n");
  }

  applyRuler() {
    if (!this.rulerEl) return;
    const settings = this.getSettings();
    this.rulerEl.style.height = `${settings.readingRulerHeight}px`;
    this.rulerEl.style.background = settings.readingRulerColor;
    this.rulerEl.style.opacity = `${settings.readingRulerOpacity}`;
    document.body.classList.toggle(BODY_CLASSES.ruler, settings.readingRulerEnabled);
  }

  onRulerMove(e) {
    if (!this.rulerEl || !this.getSettings().readingRulerEnabled) return;
    const height = this.getSettings().readingRulerHeight;
    this.rulerEl.style.top = `${e.clientY - height / 2}px`;
  }

  processBionic(el) {
    const settings = this.getSettings();
    if (!settings.bionicEnabled) return;

    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
      acceptNode: node => {
        let parent = node.parentElement;
        while (parent && parent !== el) {
          const tag = parent.tagName.toLowerCase();
          if (tag === "code" || tag === "pre" || tag === "math" || parent.classList.contains("math") || parent.classList.contains("fr-bionic")) {
            return NodeFilter.FILTER_REJECT;
          }
          parent = parent.parentElement;
        }
        const val = node.nodeValue;
        return (!val || val.trim().length === 0) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });

    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
      textNodes.push(node);
    }

    for (const textNode of textNodes) {
      this.bionifyTextNode(textNode, settings.bionicRatio, settings.bionicMinWordLength);
    }
  }

  bionifyTextNode(textNode, ratio, minLength) {
    const textVal = textNode.nodeValue;
    if (!textVal) return;
    const words = textVal.split(/(\s+)/);
    let changed = false;
    const fragment = document.createDocumentFragment();

    for (const segment of words) {
      if (segment === "" || /^\s+$/.test(segment)) {
        fragment.appendChild(document.createTextNode(segment));
        continue;
      }
      const match = segment.match(/^([^\p{L}\p{N}]*)([\p{L}\p{N}'’-]+)([^\p{L}\p{N}]*)$/u);
      if (!match) {
        fragment.appendChild(document.createTextNode(segment));
        continue;
      }
      const prefix = match[1];
      const word = match[2];
      const suffix = match[3];

      if (word.length < minLength) {
        fragment.appendChild(document.createTextNode(segment));
        continue;
      }

      const boldLength = Math.max(1, Math.round(word.length * ratio));
      const bNode = document.createElement("b");
      bNode.className = "fr-bionic";
      bNode.textContent = word.slice(0, boldLength);

      fragment.appendChild(document.createTextNode(prefix));
      fragment.appendChild(bNode);
      fragment.appendChild(document.createTextNode(word.slice(boldLength) + suffix));
      changed = true;
    }

    if (changed && textNode.parentNode) {
      textNode.parentNode.replaceChild(fragment, textNode);
    }
  }

  colorizeDefinitions(el) {
    if (!this.getSettings().colorizeDefinitions) return;
    el.querySelectorAll("p").forEach(p => {
      const text = (p.textContent || "").trim();
      if (/^(definition|def\.?)\b/i.test(text)) {
        p.classList.add("fr-definition");
      }
    });
  }

  applySmartHighlight() {
    if (this.smartHighlightCleanup) {
      this.smartHighlightCleanup();
      this.smartHighlightCleanup = null;
    }
    if (!this.getSettings().smartHighlightEnabled) return;

    let style = document.getElementById(SMART_HIGHLIGHT_STYLE_ID);
    if (!style) {
      style = document.createElement("style");
      style.id = SMART_HIGHLIGHT_STYLE_ID;
      document.head.appendChild(style);
    }
    style.textContent = `
      .fr-smart-current { background: #fff3a3 !important; border-radius: 3px; box-shadow: 0 0 0 2px rgba(255,200,0,0.25); transition: background 0.2s; }
      .fr-smart-prev { opacity: 0.5; }
    `;

    const trigger = () => this.updateSmartHighlight();
    window.addEventListener("scroll", trigger, { passive: true });
    window.addEventListener("resize", trigger);
    this.app.workspace.on("layout-change", trigger);

    this.smartHighlightCleanup = () => {
      window.removeEventListener("scroll", trigger);
      window.removeEventListener("resize", trigger);
      this.app.workspace.off("layout-change", trigger);
      document.querySelectorAll(".fr-smart-current, .fr-smart-prev").forEach(el => {
        el.classList.remove("fr-smart-current", "fr-smart-prev");
      });
    };

    setTimeout(trigger, 200);
  }

  updateSmartHighlight() {
    const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!activeView) return;
    const viewContainer = activeView.contentEl.querySelector(".markdown-reading-view");
    if (!viewContainer) return;

    const els = Array.from(viewContainer.querySelectorAll("p, li"));
    const centerLine = window.innerHeight / 2;
    let closestNode = null;
    let minDistance = Infinity;

    for (const el of els) {
      const rect = el.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) continue;
      const dist = Math.abs((rect.top + rect.bottom) / 2 - centerLine);
      if (dist < minDistance) {
        minDistance = dist;
        closestNode = el;
      }
    }

    document.querySelectorAll(".fr-smart-current, .fr-smart-prev").forEach(node => {
      node.classList.remove("fr-smart-current", "fr-smart-prev");
    });

    if (closestNode) {
      closestNode.classList.add("fr-smart-current");
      const prev = closestNode.previousElementSibling;
      if (prev && (prev.tagName === "P" || prev.tagName === "LI")) {
        prev.classList.add("fr-smart-prev");
      }
    }
  }

  applyLineFocus() {
    if (this.lineFocusCleanup) {
      this.lineFocusCleanup();
      this.lineFocusCleanup = null;
    }
    if (!this.getSettings().lineFocusEnabled) return;

    let overlay = document.getElementById(LINE_FOCUS_OVERLAY_ID);
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = LINE_FOCUS_OVERLAY_ID;
      overlay.className = "fr-line-focus-overlay";
      document.body.appendChild(overlay);
    }

    const mouseHandler = e => {
      const height = this.getSettings().lineFocusLines * 28;
      overlay.style.top = `${e.clientY - height / 2}px`;
      overlay.style.height = `${height}px`;
    };

    window.addEventListener("mousemove", mouseHandler);

    this.lineFocusCleanup = () => {
      window.removeEventListener("mousemove", mouseHandler);
      if (overlay) overlay.remove();
    };
  }

  attachHoverDefs() {
    if (this.hoverDefsCleanup) {
      this.hoverDefsCleanup();
      this.hoverDefsCleanup = null;
    }
    if (!this.getSettings().hoverDefsEnabled) return;

    const hoverHandler = e => this.onHoverForDef(e);
    document.addEventListener("mouseover", hoverHandler);

    this.hoverDefsCleanup = () => {
      document.removeEventListener("mouseover", hoverHandler);
    };
  }

  onHoverForDef(e) {
    const target = e.target;
    if (!target) return;
    const link = target.closest(".internal-link, a.internal-link");
    if (!link) return;

    const text = link.textContent || "";
    if (!text.trim() || link.getAttribute("data-fr-hover")) return;

    link.setAttribute("data-fr-hover", "1");
    setTimeout(() => link.removeAttribute("data-fr-hover"), 1500);

    const popup = document.createElement("div");
    popup.className = "fr-hover-def";
    popup.innerHTML = `
      <div class="fr-hover-def-title">${text}</div>
      <div class="fr-hover-def-body">Internal note — click to open.</div>
    `;

    const rect = link.getBoundingClientRect();
    popup.style.position = "fixed";
    popup.style.left = `${rect.left}px`;
    popup.style.top = `${rect.bottom + 6}px`;
    popup.style.zIndex = "9999";
    document.body.appendChild(popup);

    const removePopup = () => popup.remove();
    link.addEventListener("mouseout", removePopup, { once: true });
    setTimeout(removePopup, 4000);
  }

  async analyzeCurrentNote() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || !view.file) return null;
    const content = await this.app.vault.cachedRead(view.file);
    return analyzeText(content, 220);
  }

  toggleSmoothScroll() {
    if (this.smoothScrollState.active) {
      this.stopSmoothScroll();
      return false;
    } else {
      this.startSmoothScroll();
      return true;
    }
  }

  startSmoothScroll() {
    const settings = this.getSettings();
    this.smoothScrollState.active = true;
    let lastTime = performance.now();

    const frame = time => {
      if (!this.smoothScrollState.active) return;
      const dt = (time - lastTime) / 1000;
      lastTime = time;

      window.scrollBy(0, settings.smoothScrollSpeed * dt);

      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) {
        this.stopSmoothScroll();
        return;
      }
      this.smoothScrollState.raf = requestAnimationFrame(frame);
    };

    this.smoothScrollState.raf = requestAnimationFrame(frame);
    new Notice("Smooth scrolling started. Run command again to stop.");
  }

  stopSmoothScroll() {
    this.smoothScrollState.active = false;
    if (this.smoothScrollState.raf) {
      cancelAnimationFrame(this.smoothScrollState.raf);
      this.smoothScrollState.raf = null;
    }
  }

  unload() {
    if (this.rulerEl) this.rulerEl.remove();
    this.rulerEl = null;
    if (this.smartHighlightCleanup) this.smartHighlightCleanup();
    this.smartHighlightCleanup = null;
    if (this.lineFocusCleanup) this.lineFocusCleanup();
    this.lineFocusCleanup = null;
    if (this.hoverDefsCleanup) this.hoverDefsCleanup();
    this.hoverDefsCleanup = null;
    this.stopSmoothScroll();

    const gStyle = document.getElementById(GOOGLE_FONTS_STYLE_ID);
    if (gStyle) gStyle.remove();
    const tStyle = document.getElementById(TYPOGRAPHY_STYLE_ID);
    if (tStyle) tStyle.remove();
    const sStyle = document.getElementById(SMART_HIGHLIGHT_STYLE_ID);
    if (sStyle) sStyle.remove();
    const lOverlay = document.getElementById(LINE_FOCUS_OVERLAY_ID);
    if (lOverlay) lOverlay.remove();

    document.body.classList.remove(
      BODY_CLASSES.typography,
      BODY_CLASSES.ruler,
      BODY_CLASSES.boldHighlight,
      BODY_CLASSES.definitions,
      BODY_CLASSES.bionic,
      BODY_CLASSES.focusMode,
      BODY_CLASSES.smartHighlight,
      BODY_CLASSES.lineFocus
    );
  }
}

// DashboardView Class
class DashboardView extends ItemView {
  constructor(leaf, getData) {
    super(leaf);
    this.getData = getData;
  }

  getViewType() {
    return DASHBOARD_VIEW_TYPE;
  }

  getDisplayText() {
    return "Reading Dashboard";
  }

  getIcon() {
    return "book-open";
  }

  render() {
    const { settings, stats, remainingMs, totalMs, timerState, analyze } = this.getData();
    const lvlInfo = getLevelInfo(stats.xp);
    const xpPercent = Math.round((lvlInfo.into / lvlInfo.need) * 100);
    const todayGoalPercent = Math.min(100, Math.round((stats.todayMs / 60000) / settings.dopamineDailyGoalMinutes * 100));

    const todayMin = Math.round(stats.todayMs / 60000);
    const totalMin = Math.round(stats.totalReadingMs / 60000);
    const minLeft = Math.ceil(remainingMs / 60000);
    const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
    const noteName = (activeView && activeView.file) ? activeView.file.basename : "No note";

    const container = this.contentEl;
    container.empty();
    container.addClass("fr-dashboard");

    container.createEl("div", { cls: "fr-dash-section", text: "Reading Session" });
    const timeRow = container.createEl("div", { cls: "fr-dash-row" });
    timeRow.createEl("span", { cls: "fr-dash-label", text: "Time" });
    timeRow.createEl("span", { cls: "fr-dash-value", text: timerState === "idle" ? "—" : `${minLeft}m / ${Math.round(totalMs / 60000)}m` });

    this.bar(container, "Progress", timerState === "idle" ? 0 : (1 - remainingMs / Math.max(1, totalMs)) * 100);

    const currentNoteRow = container.createEl("div", { cls: "fr-dash-row" });
    currentNoteRow.createEl("span", { cls: "fr-dash-label", text: "Current" });
    currentNoteRow.createEl("span", { cls: "fr-dash-value", text: noteName });

    if (settings.difficultyEnabled) {
      // Render placeholder rows first; fill them in once the async analyzer resolves.
      // Previously `analysis` was a Promise and `analysis.difficulty` was always undefined.
      const diffRow = container.createEl("div", { cls: "fr-dash-row" });
      diffRow.createEl("span", { cls: "fr-dash-label", text: "Difficulty" });
      const diffValue = diffRow.createEl("span", { cls: "fr-dash-value", text: "…" });

      const estRow = container.createEl("div", { cls: "fr-dash-row" });
      estRow.createEl("span", { cls: "fr-dash-label", text: "Est. time" });
      const estValue = estRow.createEl("span", { cls: "fr-dash-value", text: "…" });

      if (typeof analyze === "function") {
        Promise.resolve(analyze()).then(analysis => {
          if (!analysis) {
            diffRow.remove();
            estRow.remove();
            return;
          }
          diffValue.textContent = analysis.difficulty;
          estValue.textContent = `${analysis.estimatedMinutes} min`;
        });
      } else {
        diffRow.remove();
        estRow.remove();
      }
    }

    if (settings.xpEnabled) {
      this.bar(container, `XP — Level ${lvlInfo.level}`, xpPercent, `+${Math.round(stats.xp)} XP`);
    }

    if (settings.dopamineEnabled) {
      this.bar(container, "Today's Goal", todayGoalPercent, `${todayMin} / ${settings.dopamineDailyGoalMinutes} min`);
    }

    if (settings.comboEnabled) {
      const streakRow = container.createEl("div", { cls: "fr-dash-row" });
      streakRow.createEl("span", { cls: "fr-dash-label", text: "Streak" });
      streakRow.createEl("span", { cls: "fr-dash-value", text: `${stats.streak} days (best ${stats.longestStreak})` });
    }

    if (settings.readingSpeedEnabled) {
      const avgWpm = stats.wpmSamples.length ? Math.round(stats.wpmSamples.reduce((a, b) => a + b, 0) / stats.wpmSamples.length) : 0;
      const speedRow = container.createEl("div", { cls: "fr-dash-row" });
      speedRow.createEl("span", { cls: "fr-dash-label", text: "Avg WPM" });
      speedRow.createEl("span", { cls: "fr-dash-value", text: avgWpm ? `${avgWpm}` : "—" });
    }

    const wordsTodayRow = container.createEl("div", { cls: "fr-dash-row" });
    wordsTodayRow.createEl("span", { cls: "fr-dash-label", text: "Words today" });
    wordsTodayRow.createEl("span", { cls: "fr-dash-value", text: `${stats.wordsRead}` });

    const notesFinRow = container.createEl("div", { cls: "fr-dash-row" });
    notesFinRow.createEl("span", { cls: "fr-dash-label", text: "Notes finished" });
    notesFinRow.createEl("span", { cls: "fr-dash-value", text: `${stats.notesCompleted}` });

    const totalTimeRow = container.createEl("div", { cls: "fr-dash-row" });
    totalTimeRow.createEl("span", { cls: "fr-dash-label", text: "Total time" });
    totalTimeRow.createEl("span", { cls: "fr-dash-value", text: `${totalMin} min` });

    if (settings.achievementsEnabled && stats.achievements.length) {
      container.createEl("div", { cls: "fr-dash-section", text: "Achievements" });
      const achWrap = container.createEl("div", { cls: "fr-dash-achievements" });
      for (const id of stats.achievements) {
        const matching = ACHIEVEMENTS.find(a => a.id === id);
        if (matching) {
          achWrap.createEl("div", { cls: "fr-dash-ach", text: matching.name, attr: { title: matching.desc } });
        }
      }
    }

    if (settings.heatmapEnabled) {
      container.createEl("div", { cls: "fr-dash-section", text: "Last 7 days" });
      this.renderHeatmap(container, stats);
    }
  }

  bar(el, label, percent, valueStr) {
    const row = el.createEl("div", { cls: "fr-dash-bar-row" });
    row.createEl("span", { cls: "fr-dash-label", text: label });
    if (valueStr) {
      row.createEl("span", { cls: "fr-dash-value", text: valueStr });
    }
    const outer = row.createEl("div", { cls: "fr-dash-bar" });
    const inner = outer.createEl("div", { cls: "fr-dash-bar-fill" });
    inner.style.width = `${Math.min(100, Math.max(0, percent))}%`;
  }

  renderHeatmap(el, stats) {
    const heatmap = el.createEl("div", { cls: "fr-heatmap" });
    const baseDate = new Date();
    const pastDates = [];
    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    for (let i = 6; i >= 0; i--) {
      const target = new Date(baseDate);
      target.setDate(baseDate.getDate() - i);
      pastDates.push(formatDate(target));
    }

    let maxMs = 1;
    for (const d of pastDates) {
      maxMs = Math.max(maxMs, stats.perDayMs[d] || 0);
    }

    for (const d of pastDates) {
      const ms = stats.perDayMs[d] || 0;
      const ratio = ms / maxMs;
      const cell = heatmap.createEl("div", { cls: "fr-heat-cell" });

      const nativeDay = new Date(d + "T00:00:00").getDay();
      const mappedIndex = nativeDay === 0 ? 6 : nativeDay - 1;
      cell.createEl("div", { cls: "fr-heat-day", text: weekdays[mappedIndex] });

      const barWrap = cell.createEl("div", { cls: "fr-heat-bar" });
      const fill = barWrap.createEl("div", { cls: "fr-heat-fill" });
      fill.style.height = `${Math.max(8, ratio * 100)}%`;
      fill.style.opacity = `${0.3 + ratio * 0.7}`;

      cell.createEl("div", { cls: "fr-heat-min", text: `${Math.round(ms / 60000)}m` });
    }
  }

  async onOpen() {
    this.render();
  }

  async onClose() {}
}

// FocusReadSettingTab Class
class FocusReadSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    this.section("Reading Aids");
    this.toggle("Enable Bionic Reading", "Bold the first part of each word.", "bionicEnabled");
    this.slider("Bold ratio", 0.2, 0.6, 0.05, "bionicRatio");
    this.slider("Min word length", 2, 8, 1, "bionicMinWordLength");
    this.toggle("Enable Reading Ruler", "Mouse-following horizontal bar.", "readingRulerEnabled");
    this.slider("Ruler height (px)", 10, 80, 1, "readingRulerHeight");
    this.color("Ruler color", "readingRulerColor");
    this.slider("Ruler opacity", 0.05, 0.6, 0.01, "readingRulerOpacity");
    this.toggle("Enable Typography", "Font, size, line height, max width.", "typographyEnabled");
    this.dropdown("Reading font", FONT_STACKS.map(f => ({ id: f.id, label: f.label })), "fontFamily");

    if (this.plugin.settings.fontFamily === "custom") {
      this.text("Custom font stack", "customFontFamily");
    }

    this.toggle("Load Google Fonts", "Inject Google Fonts stylesheet.", "loadGoogleFonts");
    this.slider("Font size (px)", 13, 26, 1, "fontSize");
    this.slider("Line height", 1.2, 2.2, 0.05, "lineHeight");
    this.slider("Paragraph spacing", 1, 2.5, 0.1, "paragraphSpacing");
    this.slider("Max line width (chars)", 40, 120, 1, "maxWidthChars");
    this.toggle("Highlight Definitions", 'Colorize "Definition" paragraphs.', "colorizeDefinitions");
    this.color("Definition color", "definitionColor");
    this.toggle("Highlight Bold Text", "Soft highlight on bold terms.", "highlightBold");
    this.color("Bold highlight color", "boldHighlightColor");
    this.toggle("Auto-fold headings on open", "", "autoFoldOnOpen");
    this.slider("TTS speed", 0.5, 2, 0.05, "ttsRate");
    this.slider("TTS pitch", 0.5, 2, 0.05, "ttsPitch");
    this.dropdown("TTS voice", this.ttsVoiceOptions(), "ttsVoiceURI");

    this.section("1. Floating Focus Timer");
    this.toggle("Enable floating timer", "", "timerEnabled");
    this.slider("Work minutes", 5, 90, 1, "timerWorkMinutes");
    this.slider("Break minutes", 1, 30, 1, "timerBreakMinutes");
    this.toggle("Auto-hide timer", "", "timerAutoHide");
    this.slider("Auto-hide after (s)", 1, 30, 1, "timerAutoHideSeconds");
    this.toggle("Pause on window blur", "", "timerPauseOnBlur");

    this.section("2 & 3. Reading Progress Bar");
    this.toggle("Enable progress bar", "", "progressEnabled");
    this.toggle("Show estimated time remaining", "", "progressEstimateRemaining");
    this.toggle("Show sections left count", "", "progressShowSectionsLeft");

    this.section("4. Focus Mode");
    this.toggle("Enable Focus Mode (hides UI)", "", "focusModeEnabled");

    this.section("5. Reading Heatmap");
    this.toggle("Enable heatmap in dashboard", "", "heatmapEnabled");

    this.section("6. XP System");
    this.toggle("Enable XP & levels", "", "xpEnabled");

    this.section("7. Combo / Streak");
    this.toggle("Enable combo multiplier", "", "comboEnabled");

    this.section("8. Mini Goals");
    this.toggle("Enable mini goals", 'Use the "Insert Mini Goal block" command.', "miniGoalsEnabled");

    this.section("9. Random Curiosity");
    this.toggle("Enable random jump commands", "", "curiosityEnabled");

    this.section("10. Ambient Audio");
    this.toggle("Enable ambient audio", "", "ambientEnabled");
    this.dropdown("Ambient sound", AMBIENT_SOUNDS.map(s => ({ id: s.id, label: s.label })), "ambientSound");
    this.slider("Volume", 0, 1, 0.05, "ambientVolume");

    this.section("11. Reading Statistics");
    this.toggle("Enable statistics tracking", "", "statsEnabled");

    this.section("12. Smart Highlight (Karaoke)");
    this.toggle("Highlight current sentence", "", "smartHighlightEnabled");

    this.section("13. Reading Line Focus");
    this.toggle("Dim everything except N lines", "", "lineFocusEnabled");
    this.slider("Focus lines", 1, 10, 1, "lineFocusLines");
    this.slider("Dim opacity", 0.1, 0.7, 0.05, "lineFocusOpacity");

    this.section("14. Hover Definitions");
    this.toggle("Show hover popup on internal links", "", "hoverDefsEnabled");

    this.section("15. Reading Rewards");
    this.toggle("Enable session rewards", "", "rewardsEnabled");

    this.section("16. Session Journal");
    this.toggle("Auto-write session journal entries", "", "journalEnabled");
    this.text("Journal folder", "journalFolder");

    this.section("17. ADHD Nudge");
    this.toggle("Enable idle nudge", "", "nudgeEnabled");
    this.slider("Idle threshold (s)", 10, 300, 5, "nudgeIdleSeconds");

    this.section("18. Dopamine Bar");
    this.toggle("Enable daily goal bar", "", "dopamineEnabled");
    this.slider("Daily goal (minutes)", 5, 240, 5, "dopamineDailyGoalMinutes");

    this.section("19. Reading Speed (WPM)");
    this.toggle("Track reading speed", "", "readingSpeedEnabled");

    this.section("20. Achievement System");
    this.toggle("Enable achievements", "", "achievementsEnabled");

    this.section("21. Difficulty Meter");
    this.toggle("Show note difficulty", "", "difficultyEnabled");

    this.section("22. Focus Detection");
    this.toggle("Pause timer on inactivity", "", "focusDetectionEnabled");
    this.slider("Idle seconds", 10, 300, 5, "focusDetectionIdleSeconds");

    this.section("23. Smooth Scrolling (Teleprompter)");
    this.toggle("Enable smooth scroll command", "", "smoothScrollEnabled");
    this.slider("Scroll speed (px/s)", 10, 200, 5, "smoothScrollSpeed");

    this.section("24. Visual Completion");
    this.toggle("Enable completion animation", "", "visualCompletionEnabled");

    this.section("Reading Dashboard");
    this.toggle("Enable Reading Dashboard", "", "dashboardEnabled");
    this.dropdown("Dashboard side", [{ id: "left", label: "Left" }, { id: "right", label: "Right" }], "dashboardPosition");

    this.section("Achievements Status");
    const achList = containerEl.createEl("div", { cls: "fr-setting-ach-list" });
    for (const ach of ACHIEVEMENTS) {
      const unlocked = this.plugin.stats.achievements.includes(ach.id);
      const row = achList.createEl("div", { cls: "fr-setting-ach" });
      row.createEl("span", { text: unlocked ? "★" : "☆", cls: "fr-setting-ach-icon" });
      row.createEl("span", { text: ach.name, cls: "fr-setting-ach-name" });
      row.createEl("span", { text: ach.desc, cls: "fr-setting-ach-desc" });
    }

    containerEl.createEl("p", {
      cls: "fr-setting-hint",
      text: 'Tip: every module can also be toggled from the Command Palette (search "Toggle:").'
    });
  }

  section(text) {
    this.containerEl.createEl("h2", { text });
  }

  toggle(name, desc, settingKey) {
    new Setting(this.containerEl)
      .setName(name)
      .setDesc(desc)
      .addToggle(cb => cb
        .setValue(this.plugin.settings[settingKey])
        .onChange(async val => {
          this.plugin.settings[settingKey] = val;
          await this.plugin.saveAll();
          this.plugin.onModuleToggled(settingKey);
          this.display();
        })
      );
  }

  slider(name, min, max, step, settingKey) {
    new Setting(this.containerEl)
      .setName(name)
      .addSlider(cb => cb
        .setLimits(min, max, step)
        .setValue(this.plugin.settings[settingKey])
        .setDynamicTooltip()
        .onChange(async val => {
          this.plugin.settings[settingKey] = val;
          await this.plugin.saveAll();
          this.plugin.onModuleToggled(settingKey);
        })
      );
  }

  text(name, settingKey) {
    new Setting(this.containerEl)
      .setName(name)
      .addText(cb => cb
        .setValue(this.plugin.settings[settingKey])
        .onChange(async val => {
          this.plugin.settings[settingKey] = val;
          await this.plugin.saveAll();
        })
      );
  }

  color(name, settingKey) {
    new Setting(this.containerEl)
      .setName(name)
      .addColorPicker(cb => cb
        .setValue(this.plugin.settings[settingKey])
        .onChange(async val => {
          this.plugin.settings[settingKey] = val;
          await this.plugin.saveAll();
          this.plugin.onModuleToggled(settingKey);
        })
      );
  }

  dropdown(name, options, settingKey) {
    new Setting(this.containerEl)
      .setName(name)
      .addDropdown(cb => {
        for (const opt of options) {
          cb.addOption(opt.id, opt.label);
        }
        cb.setValue(this.plugin.settings[settingKey])
          .onChange(async val => {
            this.plugin.settings[settingKey] = val;
            await this.plugin.saveAll();
            this.plugin.onModuleToggled(settingKey);
            this.display();
          });
      });
  }

  ttsVoiceOptions() {
    const voices = "speechSynthesis" in window ? window.speechSynthesis.getVoices() : [];
    return [
      { id: "", label: "System default" },
      ...voices.map(v => ({ id: v.voiceURI, label: `${v.name} (${v.lang})` }))
    ];
  }
}

// Primary Plugin Class (FocusReadPlugin)
class FocusReadPlugin extends Plugin {
  async onload() {
    await this.loadPersistedData();
    // Inject the plugin's full CSS via a <style> tag so the plugin is self-contained.
    // This guarantees styles are applied even if Obsidian fails to load styles.css.
    let styleEl = document.getElementById(INJECTED_STYLE_ID);
    if (!styleEl) {
      styleEl = document.createElement("style");
      styleEl.id = INJECTED_STYLE_ID;
      document.head.appendChild(styleEl);
    }
    styleEl.textContent = PLUGIN_CSS;
    console.log("[Focus Read] Plugin loaded v2.3.0 — CSS injected, timer controls ready.");

    this.statsMgr = new StatsManager(
      this.app,
      () => this.settings,
      () => this.stats,
      async () => { await this.saveAll(); }
    );
    this.statsMgr.rollOver();
    await this.saveAll();

    this.visual = new VisualManager(this.app, () => this.settings);
    this.visual.load(this);
    this.visual.applyAll();
    this.visual.attachHoverDefs();

    this.timer = new TimerManager(
      this.app,
      () => this.settings,
      async (ms, file) => {
        await this.statsMgr.addReadingTime(ms, file);
        this.maybeRefreshDashboard();
      },
      ms => this.onSessionEnd(ms)
    );
    this.timer.load();
    this.timer.applyVisibility();

    this.game = new GameManager(this.app, () => this.settings);

    this.registerView(DASHBOARD_VIEW_TYPE, leaf => new DashboardView(leaf, () => ({
      settings: this.settings,
      stats: this.stats,
      remainingMs: this.timer.getRemainingMs(),
      totalMs: this.settings.timerWorkMinutes * 60000,
      timerState: this.timer.getState(),
      // Pass the analyzer function — the dashboard awaits it so analysis is a real object, not a Promise.
      analyze: () => this.visual.analyzeCurrentNote()
    })));

    this.registerMarkdownPostProcessor(el => {
      this.visual.processBionic(el);
      this.visual.colorizeDefinitions(el);
    });

    if (this.settings.autoFoldOnOpen) {
      this.registerEvent(this.app.workspace.on("file-open", () => {
        window.setTimeout(() => this.foldAllHeadings(), 120);
      }));
    }

    this.dashboardRefreshInterval = window.setInterval(() => {
      if (this.settings.dashboardEnabled) {
        this.maybeRefreshDashboard();
      }
    }, 2000);

    this.wpmSampleInterval = window.setInterval(() => this.sampleWpm(), 20000);
    this.wpmLastWords = 0;
    this.wpmLastTime = 0;
    this.wpmLastPath = "";

    if (this.settings.dashboardEnabled) {
      this.activateDashboard();
    }

    this.registerCommands();
    this.addSettingTab(new FocusReadSettingTab(this.app, this));
  }

  async loadPersistedData() {
    const data = await this.loadData();
    if (data && data.settings && data.stats) {
      this.settings = Object.assign({}, DEFAULT_SETTINGS, data.settings);
      // Deep-clone defaults so nested objects/arrays in data.stats replace — not mutate — the templates.
      this.stats = Object.assign(deepClone(DEFAULT_STATS), deepClone(data.stats));
    } else if (data && typeof data === "object") {
      this.settings = Object.assign({}, DEFAULT_SETTINGS, data);
      this.stats = deepClone(DEFAULT_STATS);
    } else {
      this.settings = Object.assign({}, DEFAULT_SETTINGS);
      this.stats = deepClone(DEFAULT_STATS);
    }
  }

  async onunload() {
    const injectedStyle = document.getElementById(INJECTED_STYLE_ID);
    if (injectedStyle) injectedStyle.remove();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (this.timer) this.timer.unload();
    if (this.visual) this.visual.unload();
    if (this.game) this.game.stopAmbient();
    if (this.dashboardRefreshInterval) clearInterval(this.dashboardRefreshInterval);
    if (this.wpmSampleInterval) clearInterval(this.wpmSampleInterval);
    this.app.workspace.detachLeavesOfType(DASHBOARD_VIEW_TYPE);
  }

  async saveAll() {
    await this.saveData({ settings: this.settings, stats: this.stats });
  }

  onSessionEnd(ms) {
    this.statsMgr.recordLongestFocus(ms);
    if (this.settings.rewardsEnabled) {
      new Notice(`Great work! You focused for ${Math.round(ms / 60000)} min. Take a ${this.settings.timerBreakMinutes}-min break.`);
    }
    if (this.settings.xpEnabled) {
      this.game.showXpPopup(Math.max(5, Math.round(ms / 60000)), "Session complete");
    }
    if (this.settings.comboEnabled) {
      this.game.showComboPopup(this.stats.streak, this.stats.currentComboMultiplier);
    }
    if (this.settings.journalEnabled) {
      this.appendSessionJournal(ms);
    }
  }

  async appendSessionJournal(ms) {
    const folder = this.settings.journalFolder || "Reading Journal";
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    const file = view ? view.file : null;
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const filepath = `${folder}/${dateStr}.md`;
    const durationMin = Math.round(ms / 60000);
    let content = "";

    if (await this.app.vault.adapter.exists(filepath)) {
      content = await this.app.vault.adapter.read(filepath);
    } else {
      try {
        await this.app.vault.createFolder(folder);
      } catch (e) {}
      content = `# Reading Journal — ${dateStr}\n\n`;
    }

    const heading = this.currentHeadingName() || "—";
    const entry = `\n## ${now.toLocaleTimeString()}\n- ${durationMin} min\n- Note: ${file ? file.basename : "—"}\n- Stopped at: ${heading}\n`;
    await this.app.vault.adapter.write(filepath, content + entry);
  }

  currentHeadingName() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view) return "";
    const content = view.editor.getValue();
    const lineNum = view.editor.getCursor().line;
    const lines = content.split("\n").slice(0, lineNum + 1);

    for (let i = lines.length - 1; i >= 0; i--) {
      const match = lines[i].match(/^#{1,6}\s+(.+)$/);
      if (match) return match[1];
    }
    return "";
  }

  async sampleWpm() {
    if (!this.settings.readingSpeedEnabled || !this.timer.isRunning()) return;
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || !view.file) return;

    const currentWords = ((await this.app.vault.cachedRead(view.file)).match(/\b\w+\b/g) || []).length;
    const now = Date.now();

    if (this.wpmLastPath !== view.file.path) {
      this.wpmLastPath = view.file.path;
      this.wpmLastWords = currentWords;
      this.wpmLastTime = now;
      return;
    }

    const elapsedSeconds = (now - this.wpmLastTime) / 1000;
    if (elapsedSeconds < 5) return;

    const deltaWords = currentWords - this.wpmLastWords;
    if (deltaWords > 0) {
      const wpm = Math.round((deltaWords / elapsedSeconds) * 60);
      await this.statsMgr.recordWpm(wpm);
    }
    this.wpmLastWords = currentWords;
    this.wpmLastTime = now;
  }

  activateDashboard() {
    if (!this.settings.dashboardEnabled) return;
    const leaves = this.app.workspace.getLeavesOfType(DASHBOARD_VIEW_TYPE);
    if (leaves.length) {
      const view = leaves[0].view;
      if (view instanceof DashboardView) {
        view.render();
      }
      this.app.workspace.revealLeaf(leaves[0]);
      return;
    }
    const targetLeaf = this.settings.dashboardPosition === "left" 
      ? this.app.workspace.getLeftLeaf(false) 
      : this.app.workspace.getRightLeaf(false);
    if (targetLeaf) {
      targetLeaf.setViewState({ type: DASHBOARD_VIEW_TYPE });
      this.app.workspace.revealLeaf(targetLeaf);
    }
  }

  deactivateDashboard() {
    this.app.workspace.detachLeavesOfType(DASHBOARD_VIEW_TYPE);
  }

  maybeRefreshDashboard() {
    const leaves = this.app.workspace.getLeavesOfType(DASHBOARD_VIEW_TYPE);
    for (const leaf of leaves) {
      const view = leaf.view;
      if (view instanceof DashboardView) {
        view.render();
      }
    }
  }

  onModuleToggled(key) {
    if ([
      "typographyEnabled", "fontSize", "lineHeight", "paragraphSpacing", 
      "maxWidthChars", "fontFamily", "customFontFamily", "loadGoogleFonts", 
      "definitionColor", "boldHighlightColor"
    ].includes(key)) {
      this.visual.applyTypography();
    }

    if ([
      "readingRulerEnabled", "readingRulerHeight", "readingRulerColor", "readingRulerOpacity"
    ].includes(key)) {
      this.visual.applyRuler();
    }

    switch (key) {
      case "timerEnabled":
        this.timer.applyVisibility();
        break;
      case "progressEnabled":
        this.timer.attachProgress();
        break;
      case "dashboardEnabled":
        this.settings.dashboardEnabled ? this.activateDashboard() : this.deactivateDashboard();
        break;
      case "smartHighlightEnabled":
      case "lineFocusEnabled":
        this.visual.applySmartHighlight();
        this.visual.applyLineFocus();
        this.visual.applyBodyClasses();
        break;
      case "hoverDefsEnabled":
        this.visual.attachHoverDefs();
        break;
      case "ambientEnabled":
        if (this.settings.ambientEnabled) {
          if (this.settings.ambientSound !== "off") {
            this.game.setAmbient(this.settings.ambientSound);
          }
        } else {
          this.game.stopAmbient();
        }
        break;
      default:
        this.visual.applyBodyClasses();
        this.rerenderAll();
    }
    this.maybeRefreshDashboard();
  }

  foldAllHeadings() {
    if (this.app.commands && this.app.commands.executeCommandById) {
      this.app.commands.executeCommandById("editor:fold-all");
    }
  }

  unfoldAllHeadings() {
    if (this.app.commands && this.app.commands.executeCommandById) {
      this.app.commands.executeCommandById("editor:unfold-all");
    }
  }

  rerenderAll() {
    this.app.workspace.iterateAllLeaves(leaf => {
      const view = leaf.view;
      if (view instanceof MarkdownView) {
        const preview = view.previewMode;
        if (preview && typeof preview.rerender === "function") {
          preview.rerender(true);
        }
      }
    });
  }

  jumpRandomHeading() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view) {
      new Notice("Open a note first.");
      return;
    }
    const lines = view.editor.getValue().split("\n");
    const headingIndices = [];
    lines.forEach((line, index) => {
      if (/^#{1,6}\s+/.test(line)) {
        headingIndices.push(index);
      }
    });
    if (!headingIndices.length) {
      new Notice("No headings in this note.");
      return;
    }
    const randIndex = headingIndices[Math.floor(Math.random() * headingIndices.length)];
    view.editor.setCursor({ line: randIndex, ch: 0 });
    view.editor.scrollIntoView({ from: { line: randIndex, ch: 0 }, to: { line: randIndex, ch: 0 } }, true);
  }

  async openRandomNote() {
    const files = this.app.vault.getMarkdownFiles();
    if (!files.length) return;
    const randFile = files[Math.floor(Math.random() * files.length)];
    await this.app.workspace.getLeaf(false).openFile(randFile);
    new Notice(`Opened: ${randFile.basename}`);
  }

  async markNoteCompleted() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || !view.file) {
      new Notice("Open a note first.");
      return;
    }
    const text = await this.app.vault.cachedRead(view.file);
    const count = (text.match(/\b\w+\b/g) || []).length;
    this.statsMgr.markNoteCompleted(view.file);
    this.game.showCompletion(view.file.basename, 50, count);
    this.maybeRefreshDashboard();
  }

  readAloud() {
    if (!("speechSynthesis" in window)) {
      new Notice("TTS not available.");
      return;
    }
    window.speechSynthesis.cancel();
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view) {
      new Notice("Open a note first.");
      return;
    }
    const selection = view.editor.getSelection();
    const cleanText = selection || stripMarkdown(view.editor.getValue());
    if (!cleanText.trim()) {
      new Notice("Nothing to read.");
      return;
    }

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = this.settings.ttsRate;
    utterance.pitch = this.settings.ttsPitch;

    const voices = window.speechSynthesis.getVoices();
    if (this.settings.ttsVoiceURI) {
      const match = voices.find(v => v.voiceURI === this.settings.ttsVoiceURI);
      if (match) utterance.voice = match;
    }

    utterance.onstart = () => new Notice("Reading aloud...");
    utterance.onend = () => new Notice("Finished reading.");
    utterance.onerror = () => new Notice("Reading was interrupted.");
    window.speechSynthesis.speak(utterance);
  }

  registerCommands() {
    this.addCommand({
      id: "toggle-bionic",
      name: "Toggle Bionic Reading",
      callback: async () => {
        this.settings.bionicEnabled = !this.settings.bionicEnabled;
        await this.saveAll();
        this.visual.applyBodyClasses();
        this.rerenderAll();
        new Notice(`Bionic Reading: ${this.settings.bionicEnabled ? "ON" : "OFF"}`);
      }
    });

    this.addCommand({
      id: "toggle-ruler",
      name: "Toggle Reading Ruler",
      callback: async () => {
        this.settings.readingRulerEnabled = !this.settings.readingRulerEnabled;
        await this.saveAll();
        this.visual.applyRuler();
        new Notice(`Reading Ruler: ${this.settings.readingRulerEnabled ? "ON" : "OFF"}`);
      }
    });

    this.addCommand({
      id: "toggle-typography",
      name: "Toggle Typography",
      callback: async () => {
        this.settings.typographyEnabled = !this.settings.typographyEnabled;
        await this.saveAll();
        this.visual.applyTypography();
        this.visual.applyBodyClasses();
      }
    });

    this.addCommand({
      id: "toggle-bold-highlight",
      name: "Toggle Bold Highlight",
      callback: async () => {
        this.settings.highlightBold = !this.settings.highlightBold;
        await this.saveAll();
        this.visual.applyBodyClasses();
      }
    });

    this.addCommand({
      id: "toggle-definitions",
      name: "Toggle Definition Highlight",
      callback: async () => {
        this.settings.colorizeDefinitions = !this.settings.colorizeDefinitions;
        await this.saveAll();
        this.visual.applyBodyClasses();
        this.rerenderAll();
      }
    });

    this.addCommand({
      id: "tts-read",
      name: "Read Aloud",
      callback: () => this.readAloud()
    });

    this.addCommand({
      id: "tts-stop",
      name: "Stop Reading Aloud",
      callback: () => {
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        new Notice("Stopped reading.");
      }
    });

    this.addCommand({
      id: "fold-all",
      name: "Fold All Headings",
      callback: () => this.foldAllHeadings()
    });

    this.addCommand({
      id: "unfold-all",
      name: "Unfold All Headings",
      callback: () => this.unfoldAllHeadings()
    });

    const calloutTypes = [
      ["info", "Info"],
      ["tip", "Tip"],
      ["warning", "Warning"],
      ["success", "Success"],
      ["quote", "Quote"],
      ["abstract", "Abstract"],
      ["example", "Example"],
      ["bug", "Bug"],
      ["failure", "Failure"],
      ["question", "Question"]
    ];

    for (const [id, name] of calloutTypes) {
      this.addCommand({
        id: `insert-callout-${id}`,
        name: `Insert ${name} callout`,
        editorCallback: editor => {
          const selection = editor.getSelection();
          if (selection) {
            const formatted = selection.split("\n").map(line => `> ${line}`).join("\n");
            editor.replaceSelection(`> [!${id}]\n${formatted}`);
          } else {
            editor.replaceSelection(`> [!${id}]\n> `);
          }
        }
      });
    }

    this.addCommand({
      id: "insert-definition",
      name: "Insert Definition block",
      editorCallback: editor => {
        const selection = editor.getSelection();
        editor.replaceSelection(`**Definition**\n\n${selection}${selection ? "\n" : ""}`);
      }
    });

    this.addCommand({
      id: "convert-to-list",
      name: "Convert selection to scannable list",
      editorCallback: editor => {
        const selection = editor.getSelection();
        if (!selection) {
          new Notice("Select a paragraph first.");
          return;
        }
        const listItems = selection.split(/\n+/).map(line => line.trim()).filter(line => line.length > 0);
        editor.replaceSelection(listItems.map(item => `- ${item.replace(/[.;]\s*$/, "")}`).join("\n"));
      }
    });

    this.addCommand({
      id: "timer-start",
      name: "Start Focus Session",
      callback: () => this.timer.start()
    });

    this.addCommand({
      id: "timer-pause",
      name: "Pause/Resume Focus Session",
      callback: () => {
        const state = this.timer.getState();
        if (state === "running") {
          this.timer.pause();
        } else if (state === "paused") {
          this.timer.resume();
        } else {
          this.timer.start();
        }
      }
    });

    this.addCommand({
      id: "timer-stop",
      name: "Stop Focus Session",
      callback: () => this.timer.stop()
    });

    this.addCommand({
      id: "toggle-focus-mode",
      name: "Toggle Focus Mode",
      callback: async () => {
        this.settings.focusModeEnabled = !this.settings.focusModeEnabled;
        await this.saveAll();
        this.visual.applyBodyClasses();
        new Notice(`Focus Mode: ${this.settings.focusModeEnabled ? "ON" : "OFF"}`);
      }
    });

    this.addCommand({
      id: "random-heading",
      name: "Jump to Random Heading",
      callback: () => this.jumpRandomHeading()
    });

    this.addCommand({
      id: "random-note",
      name: "Open Random Note",
      callback: () => this.openRandomNote()
    });

    for (const sound of AMBIENT_SOUNDS) {
      if (sound.id !== "off") {
        this.addCommand({
          id: `ambient-${sound.id}`,
          name: `Ambient: ${sound.label}`,
          callback: async () => {
            this.settings.ambientSound = sound.id;
            await this.saveAll();
            this.game.setAmbient(sound.id);
            new Notice(`Ambient: ${sound.label}`);
          }
        });
      }
    }

    this.addCommand({
      id: "ambient-stop",
      name: "Ambient: Stop",
      callback: async () => {
        this.settings.ambientSound = "off";
        await this.saveAll();
        this.game.stopAmbient();
      }
    });

    this.addCommand({
      id: "toggle-smooth-scroll",
      name: "Toggle Smooth Scrolling (Teleprompter)",
      callback: () => {
        const isActive = this.visual.toggleSmoothScroll();
        new Notice(`Smooth scrolling: ${isActive ? "ON" : "OFF"}`);
      }
    });

    this.addCommand({
      id: "mark-note-completed",
      name: "Mark Current Note as Completed",
      callback: () => this.markNoteCompleted()
    });

    this.addCommand({
      id: "insert-mini-goal",
      name: "Insert Mini Goal block",
      editorCallback: editor => {
        const selection = editor.getSelection() || "Read until next heading";
        editor.replaceSelection(`> [!goal]\n> **Mission:** ${selection}\n> **Reward:** +25 XP\n`);
      }
    });

    this.addCommand({
      id: "toggle-dashboard",
      name: "Toggle Reading Dashboard",
      callback: async () => {
        this.settings.dashboardEnabled = !this.settings.dashboardEnabled;
        await this.saveAll();
        if (this.settings.dashboardEnabled) {
          this.activateDashboard();
        } else {
          this.deactivateDashboard();
        }
        new Notice(`Dashboard: ${this.settings.dashboardEnabled ? "ON" : "OFF"}`);
      }
    });

    for (const [key, label] of MODULE_TOGGLES) {
      this.addCommand({
        id: `toggle-module-${String(key)}`,
        name: `Toggle: ${label}`,
        callback: async () => {
          this.settings[key] = !this.settings[key];
          await this.saveAll();
          this.onModuleToggled(key);
          new Notice(`${label}: ${this.settings[key] ? "ON" : "OFF"}`);
        }
      });
    }
  }
}

module.exports = FocusReadPlugin;