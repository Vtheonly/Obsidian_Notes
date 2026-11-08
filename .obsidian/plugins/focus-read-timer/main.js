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

// focus-read-timer/src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => FocusReadTimerPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian2 = require("obsidian");

// focus-read-timer/src/settings.ts
var DEFAULT_SETTINGS = {
  timerEnabled: true,
  timerWorkMinutes: 25,
  timerBreakMinutes: 5,
  timerAutoHide: true,
  timerAutoHideSeconds: 4,
  timerPauseOnBlur: true,
  timerPositionX: null,
  timerPositionY: null,
  focusDetectionEnabled: true,
  focusDetectionIdleSeconds: 30,
  nudgeEnabled: false,
  nudgeIdleSeconds: 60,
  nudgeIgnoreScroll: true,
  dopamineEnabled: false,
  dopamineDailyGoalMinutes: 60
};
function clampInt(value, min, max, fallback) {
  if (typeof value !== "number" || !Number.isFinite(value)) return fallback;
  return Math.round(Math.min(Math.max(value, min), max));
}
function normalizeSettings(raw) {
  const merged = { ...DEFAULT_SETTINGS, ...raw != null ? raw : {} };
  merged.timerWorkMinutes = clampInt(merged.timerWorkMinutes, 1, 180, DEFAULT_SETTINGS.timerWorkMinutes);
  merged.timerBreakMinutes = clampInt(merged.timerBreakMinutes, 1, 60, DEFAULT_SETTINGS.timerBreakMinutes);
  merged.timerAutoHideSeconds = clampInt(merged.timerAutoHideSeconds, 1, 120, DEFAULT_SETTINGS.timerAutoHideSeconds);
  merged.focusDetectionIdleSeconds = clampInt(merged.focusDetectionIdleSeconds, 5, 600, DEFAULT_SETTINGS.focusDetectionIdleSeconds);
  merged.nudgeIdleSeconds = clampInt(merged.nudgeIdleSeconds, 5, 600, DEFAULT_SETTINGS.nudgeIdleSeconds);
  merged.dopamineDailyGoalMinutes = clampInt(merged.dopamineDailyGoalMinutes, 1, 720, DEFAULT_SETTINGS.dopamineDailyGoalMinutes);
  for (const key of ["timerPositionX", "timerPositionY"]) {
    const v = merged[key];
    if (v !== null && (typeof v !== "number" || !Number.isFinite(v))) {
      merged[key] = null;
    }
  }
  return merged;
}
function formatClock(ms) {
  const totalSec = Math.max(0, Math.ceil(ms / 1e3));
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

// focus-read-timer/src/timer.ts
var FocusTimer = class {
  constructor(host) {
    this.intervalId = null;
    this.phase = "idle";
    this.running = false;
    this.remainingMs = 0;
    this.totalMs = 0;
    this.focusMs = 0;
    this.lastTickAt = 0;
    this.lastRenderedSecond = -1;
    this.host = host;
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
    this.totalMs = Math.max(6e4 / 60, s.timerWorkMinutes * 6e4);
    this.remainingMs = this.totalMs;
    this.focusMs = 0;
    this.lastTickAt = this.now();
    this.lastRenderedSecond = -1;
    this.ensureTicking();
    this.emit();
  }
  startBreak() {
    const s = this.host.getSettings();
    this.phase = "break";
    this.running = true;
    this.totalMs = s.timerBreakMinutes * 6e4;
    this.remainingMs = this.totalMs;
    this.focusMs = 0;
    this.lastTickAt = this.now();
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
      this.lastTickAt = this.now();
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
  /** Called by the host on its interval (also safe to call directly). */
  tick() {
    if (this.phase === "idle" || !this.running) return;
    const now = this.now();
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
      if (finishedPhase === "work") {
        this.host.onWorkComplete(focusMs);
      } else {
        this.host.onBreakComplete();
      }
    }
  }
  ensureTicking() {
    if (this.intervalId !== null) return;
    this.intervalId = window.setInterval(() => this.tick(), 250);
  }
  /** Stops the internal interval (call on unload or when fully idle). */
  shutdown() {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }
  emit() {
    this.host.onSnapshot(this.snapshot);
  }
  now() {
    return performance.now();
  }
};

// focus-read-timer/src/stats.ts
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
  /** Explicitly restarts the accrual window (e.g. after focus loss). */
  resetWindow() {
    this.lastAccrualAt = this.nowMs();
  }
  /**
   * Rolls the daily counters over if the date changed since the last write.
   * Updates streaks. Must be called before reading/writing today's numbers.
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
   * Returns the number of ms actually recorded (0 when nothing counted).
   *
   * `windowFocused` — the Obsidian window must be focused.
   * `userActive`    — when focus detection is enabled, the user must have
   *                    been active recently (fixes the original behaviour of
   *                    counting time while the user had walked away with the
   *                    window focused).
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
  /** Records a completed focus session (longest-focus tracking). */
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
/** Persist at most every 10 s (matches original behaviour). */
_ReadingStatsTracker.SAVE_INTERVAL_MS = 1e4;
var ReadingStatsTracker = _ReadingStatsTracker;

// shared/src/viewport.ts
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

// focus-read-timer/src/widget.ts
var TIMER_ID = "frt-floating-timer";
var DRAG_HEADER_CLASS = "frt-timer-drag-header";
var TimerWidget = class {
  constructor(host) {
    this.el = null;
    this.dragging = false;
    this.dragPointerId = null;
    this.dragOffsetX = 0;
    this.dragOffsetY = 0;
    /* ------------------------------------------------------------------ */
    /* Auto-hide                                                           */
    /* ------------------------------------------------------------------ */
    this.autoHideTimer = null;
    this.host = host;
  }
  /* ------------------------------------------------------------------ */
  /* Lifecycle                                                           */
  /* ------------------------------------------------------------------ */
  mount() {
    if (document.getElementById(TIMER_ID)) return;
    const el = document.createElement("div");
    el.id = TIMER_ID;
    el.className = "frt-floating-timer";
    el.style.display = "none";
    el.innerHTML = `
      <div class="${DRAG_HEADER_CLASS}" title="Drag to move the timer">
        <span class="frt-drag-grip">\u283F</span>
        <span class="frt-drag-label-text">Reading Timer</span>
        <span class="frt-drag-grip">\u283F</span>
      </div>
      <div class="frt-timer-time">00:00</div>
      <div class="frt-timer-bar"><div class="frt-timer-bar-fill"></div></div>
      <div class="frt-timer-xp"></div>
      <div class="frt-timer-controls">
        <button class="frt-timer-btn frt-timer-btn-primary" data-action="start">Start</button>
        <button class="frt-timer-btn" data-action="pause">Pause</button>
        <button class="frt-timer-btn frt-timer-btn-add" data-action="addtime">+30s</button>
        <button class="frt-timer-btn frt-timer-btn-stop" data-action="stop">Stop</button>
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
    (_a = this.el) == null ? void 0 : _a.remove();
    this.el = null;
  }
  /* ------------------------------------------------------------------ */
  /* Visibility & position                                               */
  /* ------------------------------------------------------------------ */
  applyVisibility() {
    var _a;
    const el = (_a = this.el) != null ? _a : document.getElementById(TIMER_ID);
    if (!el) return;
    const visible = this.host.getSettings().timerEnabled;
    el.style.display = visible ? "block" : "none";
    if (visible) this.applySavedPosition();
  }
  /**
   * Restores the saved position, clamped into the current viewport — this is
   * what keeps the timer reachable after switching from a big desktop screen
   * to a phone.
   */
  applySavedPosition() {
    const el = this.el;
    if (!el) return;
    const { timerPositionX, timerPositionY } = this.host.getSettings();
    if (timerPositionX === null || timerPositionY === null) {
      el.style.left = "auto";
      el.style.top = "16px";
      el.style.right = "16px";
      return;
    }
    const rect = el.getBoundingClientRect();
    const { x, y } = clampToViewport(timerPositionX, timerPositionY, rect.width || 220, rect.height || 140);
    el.style.right = "auto";
    el.style.left = `${Math.round(x)}px`;
    el.style.top = `${Math.round(y)}px`;
  }
  /** Re-clamps the current position after a resize/orientation change. */
  reflow() {
    const el = this.el;
    if (!el || this.dragging) return;
    const { timerPositionX, timerPositionY } = this.host.getSettings();
    if (timerPositionX === null || timerPositionY === null) return;
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
    var _a;
    const el = (_a = this.el) != null ? _a : document.getElementById(TIMER_ID);
    if (!el) return;
    const s = this.host.getSettings();
    const timeEl = el.querySelector(".frt-timer-time");
    const labelEl = el.querySelector(".frt-drag-label-text");
    const fillEl = el.querySelector(".frt-timer-bar-fill");
    const xpEl = el.querySelector(".frt-timer-xp");
    const startBtn = el.querySelector('[data-action="start"]');
    const pauseBtn = el.querySelector('[data-action="pause"]');
    const addBtn = el.querySelector('[data-action="addtime"]');
    const stopBtn = el.querySelector('[data-action="stop"]');
    if (snap.phase === "idle") {
      if (labelEl) labelEl.textContent = "Ready \u2014 drag me";
      if (timeEl) timeEl.textContent = formatClock(s.timerWorkMinutes * 6e4);
      if (fillEl) fillEl.style.width = "0%";
      if (xpEl) xpEl.textContent = "Click Start to begin";
    } else {
      if (timeEl) timeEl.textContent = formatClock(snap.remainingMs);
      if (labelEl) {
        labelEl.textContent = snap.phase === "break" ? "Break" : snap.running ? "Reading" : "Paused";
      }
      const pct = snap.totalMs > 0 ? (1 - snap.remainingMs / snap.totalMs) * 100 : 0;
      if (fillEl) fillEl.style.width = `${pct}%`;
      if (xpEl) {
        xpEl.textContent = snap.phase === "break" ? "On break" : `+${Math.round(snap.focusMs / 6e4)} min`;
      }
    }
    if (startBtn) {
      startBtn.disabled = snap.phase === "idle" ? false : snap.phase === "break" ? false : !snap.running && snap.phase === "work" ? true : false;
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
    const controls = el.querySelector(".frt-timer-controls");
    if (!controls) return;
    this.host.registerDomElement(controls, "pointerdown", (e) => e.stopPropagation());
    this.host.registerDomElement(controls, "click", (e) => {
      var _a, _b;
      const btn = (_b = (_a = e.target) == null ? void 0 : _a.closest) == null ? void 0 : _b.call(_a, ".frt-timer-btn");
      if (!btn) return;
      e.stopPropagation();
      this.host.onControl(btn.getAttribute("data-action"));
    });
  }
  bindDrag(el) {
    const header = el.querySelector(`.${DRAG_HEADER_CLASS}`);
    if (!header) return;
    const register = (type, cb) => this.host.registerDomElement(header, type, cb);
    register("pointerdown", (e) => {
      if (e.button !== void 0 && e.button !== 0) return;
      this.dragging = true;
      this.dragPointerId = e.pointerId;
      const rect = el.getBoundingClientRect();
      this.dragOffsetX = e.clientX - rect.left;
      this.dragOffsetY = e.clientY - rect.top;
      el.classList.add("frt-dragging");
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
        rect.height || 140
      );
      el.style.left = `${Math.round(x)}px`;
      el.style.top = `${Math.round(y)}px`;
      e.preventDefault();
    });
    const endDrag = (e) => {
      if (!this.dragging || e.pointerId !== this.dragPointerId) return;
      this.dragging = false;
      this.dragPointerId = null;
      el.classList.remove("frt-dragging");
      try {
        header.releasePointerCapture(e.pointerId);
      } catch (e2) {
      }
      const rect = el.getBoundingClientRect();
      this.host.savePosition(Math.round(rect.left), Math.round(rect.top));
    };
    register("pointerup", endDrag);
    register("pointercancel", endDrag);
    register("lostpointercapture", (e) => {
      if (this.dragging && e.pointerId === this.dragPointerId) {
        this.dragging = false;
        this.dragPointerId = null;
        el.classList.remove("frt-dragging");
        const rect = el.getBoundingClientRect();
        this.host.savePosition(Math.round(rect.left), Math.round(rect.top));
      }
    });
    register("contextmenu", (e) => {
      if (this.dragging) e.preventDefault();
    });
  }
  /** Un-dims the widget and restarts the auto-hide countdown. */
  poke() {
    const el = this.el;
    if (!el) return;
    el.style.opacity = "1";
    this.resetAutoHide();
  }
  resetAutoHide() {
    const s = this.host.getSettings();
    if (this.autoHideTimer !== null) {
      clearTimeout(this.autoHideTimer);
      this.autoHideTimer = null;
    }
    if (!s.timerAutoHide) return;
    this.autoHideTimer = window.setTimeout(() => {
      const el = this.el;
      if (el && !this.dragging) el.style.opacity = "0.55";
    }, s.timerAutoHideSeconds * 1e3);
  }
  cancelAutoHide() {
    if (this.autoHideTimer !== null) {
      clearTimeout(this.autoHideTimer);
      this.autoHideTimer = null;
    }
  }
};

// focus-read-timer/src/nudge.ts
var NUDGE_ID = "frt-adhd-nudge";
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
    nudge.className = "frt-adhd-nudge";
    const remaining = this.host.getWorkRemainingMs();
    const body = remaining !== null && remaining > 0 ? `Continue? ${Math.ceil(remaining / 6e4)} min left in session.` : `You've been idle for ${Math.round(this.idleThresholdMs() / 1e3)}s. Get back to reading?`;
    nudge.innerHTML = `
      <div class="frt-nudge-title">You stopped reading.</div>
      <div class="frt-nudge-body">${body}</div>
      <div class="frt-nudge-actions">
        <button class="frt-nudge-continue">Continue</button>
        <button class="frt-nudge-dismiss">Dismiss</button>
      </div>`;
    document.body.appendChild(nudge);
    this.visible = true;
    const continueBtn = nudge.querySelector(".frt-nudge-continue");
    const dismissBtn = nudge.querySelector(".frt-nudge-dismiss");
    if (continueBtn) {
      this.host.registerDomElement(continueBtn, "click", () => {
        this.host.onContinue();
        this.noteInputActivity();
      });
    }
    if (dismissBtn) {
      this.host.registerDomElement(dismissBtn, "click", () => {
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

// focus-read-timer/src/dopamine.ts
var DOPAMINE_BAR_ID = "frt-dopamine-bar";
var DopamineBar = class {
  constructor() {
    this.bar = null;
    this.label = null;
  }
  mount() {
    if (document.getElementById(DOPAMINE_BAR_ID)) return;
    const bar = document.createElement("div");
    bar.id = DOPAMINE_BAR_ID;
    bar.className = "frt-dopamine-bar";
    bar.innerHTML = `<div class="frt-dopamine-bar-fill"></div>`;
    bar.style.display = "none";
    document.body.appendChild(bar);
    const label = document.createElement("div");
    label.id = `${DOPAMINE_BAR_ID}-label`;
    label.className = "frt-dopamine-bar-label";
    label.style.display = "none";
    document.body.appendChild(label);
    this.bar = bar;
    this.label = label;
  }
  destroy() {
    var _a, _b;
    (_a = this.bar) == null ? void 0 : _a.remove();
    (_b = this.label) == null ? void 0 : _b.remove();
    this.bar = null;
    this.label = null;
  }
  applyVisibility(enabled) {
    this.mountIfMissing();
    if (this.bar) this.bar.style.display = enabled ? "block" : "none";
    if (this.label) this.label.style.display = enabled ? "block" : "none";
    if (enabled) this.render(0, 1);
  }
  mountIfMissing() {
    if (!this.bar || !this.label || !document.getElementById(DOPAMINE_BAR_ID)) {
      this.bar = null;
      this.label = null;
      this.mount();
    }
  }
  render(todayMinutes, goalMinutes) {
    this.mountIfMissing();
    if (!this.bar || !this.label) return;
    const goal = Math.max(1, goalMinutes);
    const pct = Math.min(100, Math.round(todayMinutes / goal * 100));
    const fill = this.bar.querySelector(".frt-dopamine-bar-fill");
    if (fill) fill.style.width = `${pct}%`;
    this.label.textContent = `${todayMinutes} / ${goal} min (${pct}%)`;
  }
};

// focus-read-timer/src/settings-tab.ts
var import_obsidian = require("obsidian");
var TimerSettingTab = class extends import_obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    this.section("Floating focus timer");
    this.toggle("Enable floating timer", "Show the floating timer box (drag it by its top handle).", "timerEnabled", () => this.plugin.applyTimerVisibility());
    this.slider("Work minutes", 5, 90, 1, "timerWorkMinutes");
    this.slider("Break minutes", 1, 30, 1, "timerBreakMinutes");
    this.toggle("Auto-hide timer", "Dim the timer box when idle.", "timerAutoHide");
    this.slider("Auto-hide after (s)", 1, 30, 1, "timerAutoHideSeconds");
    this.toggle("Pause on window blur", "Pause when Obsidian loses focus or is hidden.", "timerPauseOnBlur");
    this.section("Focus detection");
    this.toggle("Enable focus detection", "Only accumulate focus time while you are actively reading.", "focusDetectionEnabled");
    this.slider("Idle seconds", 10, 300, 5, "focusDetectionIdleSeconds");
    this.section("Idle nudge");
    this.toggle("Enable idle nudge", "Pop a reminder when you stop reading (works even without a running timer).", "nudgeEnabled");
    this.slider("Idle threshold (s)", 10, 300, 5, "nudgeIdleSeconds");
    this.toggle("Don't count scroll as activity", "Recommended ON \u2014 scrolling while reading shouldn't reset the idle timer.", "nudgeIgnoreScroll");
    this.section("Daily goal bar");
    this.toggle("Enable daily goal bar", "Bottom bar showing today's reading vs goal (works independently of the timer).", "dopamineEnabled", () => this.plugin.applyDopamineVisibility());
    this.slider("Daily goal (minutes)", 5, 240, 5, "dopamineDailyGoalMinutes", () => this.plugin.applyDopamineVisibility());
    containerEl.createEl("p", {
      cls: "fr-setting-hint",
      text: 'Drag the timer by its top header bar (the strip labeled "Reading Timer" with the \u283F grip icons). The position is kept inside the screen automatically \u2014 including after switching between desktop and mobile. Use the command palette \u2192 "Reset timer position" to snap it back to the top-right corner.'
    });
  }
  section(title) {
    this.containerEl.createEl("h2", { text: title });
  }
  toggle(name, desc, key, after) {
    new import_obsidian.Setting(this.containerEl).setName(name).setDesc(desc).addToggle(
      (toggle) => toggle.setValue(Boolean(this.plugin.settings[key])).onChange(async (v) => {
        this.plugin.settings[key] = v;
        await this.plugin.persist();
        after == null ? void 0 : after();
      })
    );
  }
  slider(name, min, max, step, key, after) {
    new import_obsidian.Setting(this.containerEl).setName(name).addSlider(
      (slider) => slider.setLimits(min, max, step).setValue(Number(this.plugin.settings[key])).setDynamicTooltip().onChange(async (v) => {
        this.plugin.settings[key] = v;
        await this.plugin.persist();
        after == null ? void 0 : after();
      })
    );
  }
};

// focus-read-timer/src/main.ts
var FocusReadTimerPlugin = class extends import_obsidian2.Plugin {
  constructor() {
    super(...arguments);
    /* Activity tracking */
    this.lastActivityAt = 0;
    this.lastInputActivityAt = 0;
    this.windowFocused = true;
  }
  async onload() {
    var _a;
    const data = (_a = await this.loadData()) != null ? _a : {};
    this.settings = normalizeSettings(data.settings);
    this.stats = normalizeStats(data.stats);
    this.lastActivityAt = Date.now();
    this.lastInputActivityAt = Date.now();
    this.statsTracker = new ReadingStatsTracker({
      getStats: () => this.stats,
      persist: () => void this.persist()
    });
    this.statsTracker.rollOver();
    this.widget = new TimerWidget({
      getSettings: () => this.settings,
      onControl: (action) => this.handleControl(action),
      registerDomElement: (el, type, cb, options) => this.registerDomEvent(el, type, cb, options),
      savePosition: (x, y) => {
        this.settings.timerPositionX = x;
        this.settings.timerPositionY = y;
        void this.persist();
      }
    });
    this.timer = new FocusTimer({
      getSettings: () => this.settings,
      isUserFocused: () => this.isUserFocused(),
      onSnapshot: (snap) => this.onTimerSnapshot(snap),
      onWorkComplete: (focusMs) => this.onWorkComplete(focusMs),
      onBreakComplete: () => {
        new import_obsidian2.Notice("Break over. Ready for another session?");
      }
    });
    this.nudge = new NudgeController(
      {
        registerDomElement: (el, type, cb, options) => this.registerDomEvent(el, type, cb, options),
        getWorkRemainingMs: () => this.timer.phase === "work" && this.timer.running ? this.timer.remainingMs : null,
        onContinue: () => this.widget.poke()
      },
      () => this.settings.nudgeIdleSeconds * 1e3
    );
    this.dopamine = new DopamineBar();
    this.widget.mount();
    this.dopamine.mount();
    this.widget.render(this.timer.snapshot);
    this.dopamine.applyVisibility(this.settings.dopamineEnabled);
    if (this.settings.dopamineEnabled) {
      this.dopamine.render(this.statsTracker.todayMinutes(), this.settings.dopamineDailyGoalMinutes);
    }
    this.registerDomEvent(window, "pointermove", () => this.onActivity(false), { passive: true });
    this.registerDomEvent(window, "keydown", () => this.onActivity(true), { passive: true });
    this.registerDomEvent(window, "scroll", () => this.onActivity(!this.settings.nudgeIgnoreScroll), { passive: true });
    this.registerDomEvent(window, "pointerdown", () => this.onActivity(true), { passive: true });
    this.registerDomEvent(window, "blur", () => {
      this.windowFocused = false;
      if (this.settings.timerPauseOnBlur && this.timer.running) {
        this.timer.pause();
        new import_obsidian2.Notice("Paused: window lost focus");
      }
    });
    this.registerDomEvent(window, "focus", () => {
      this.windowFocused = true;
      this.onActivity(true);
    });
    this.registerDomEvent(document, "visibilitychange", () => {
      if (document.hidden) {
        if (this.settings.timerPauseOnBlur && this.timer.running) {
          this.timer.pause();
          new import_obsidian2.Notice("Paused: tab hidden");
        }
      } else {
        this.windowFocused = true;
        this.onActivity(true);
      }
    });
    const reflowWidget = () => this.widget.reflow();
    this.registerDomEvent(window, "resize", reflowWidget);
    this.registerDomEvent(window, "orientationchange", reflowWidget);
    if (window.visualViewport) {
      this.registerDomEvent(window.visualViewport, "resize", reflowWidget);
    }
    this.registerInterval(window.setInterval(() => this.nudge.checkIdle(), 5e3));
    this.registerInterval(window.setInterval(() => this.flushReadingTime(), 3e4));
    this.registerInterval(window.setInterval(() => {
      if (this.settings.dopamineEnabled) {
        this.dopamine.render(this.statsTracker.todayMinutes(), this.settings.dopamineDailyGoalMinutes);
      }
    }, 5e3));
    this.addSettingTab(new TimerSettingTab(this.app, this));
    this.registerCommands();
  }
  async onunload() {
    var _a, _b, _c, _d, _e;
    (_a = this.timer) == null ? void 0 : _a.shutdown();
    (_b = this.widget) == null ? void 0 : _b.cancelAutoHide();
    (_c = this.widget) == null ? void 0 : _c.destroy();
    (_d = this.nudge) == null ? void 0 : _d.destroy();
    (_e = this.dopamine) == null ? void 0 : _e.destroy();
    this.flushReadingTime();
    await this.persist();
  }
  /* ------------------------------------------------------------------ */
  /* Persistence                                                         */
  /* ------------------------------------------------------------------ */
  async persist() {
    await this.saveData({ settings: this.settings, stats: this.stats });
  }
  /* ------------------------------------------------------------------ */
  /* Focus / activity                                                    */
  /* ------------------------------------------------------------------ */
  isUserFocused() {
    if (!this.settings.focusDetectionEnabled) return this.windowFocused;
    return this.windowFocused && Date.now() - this.lastActivityAt < this.settings.focusDetectionIdleSeconds * 1e3;
  }
  /**
   * @param countsAsInput true for keyboard/touch (resets the nudge idle
   *                      timer); false for scroll/pointer-move.
   */
  onActivity(countsAsInput) {
    this.lastActivityAt = Date.now();
    if (countsAsInput || !this.settings.nudgeIgnoreScroll) {
      this.lastInputActivityAt = Date.now();
      this.nudge.noteInputActivity(this.lastInputActivityAt);
    }
    this.widget.poke();
  }
  flushReadingTime() {
    this.statsTracker.accrue(
      this.windowFocused && !document.hidden,
      !this.settings.focusDetectionEnabled || Date.now() - this.lastActivityAt < this.settings.focusDetectionIdleSeconds * 1e3
    );
    if (this.settings.dopamineEnabled) {
      this.dopamine.render(this.statsTracker.todayMinutes(), this.settings.dopamineDailyGoalMinutes);
    }
  }
  /* ------------------------------------------------------------------ */
  /* Timer flow                                                          */
  /* ------------------------------------------------------------------ */
  handleControl(action) {
    switch (action) {
      case "start":
        this.startWork();
        break;
      case "pause":
        this.timer.togglePauseResume();
        break;
      case "addtime":
        if (this.timer.addTime(3e4)) new import_obsidian2.Notice("Added 30s");
        break;
      case "stop":
        if (this.timer.phase !== "idle") {
          this.timer.stop();
          new import_obsidian2.Notice("Timer stopped.");
        }
        break;
    }
  }
  startWork() {
    if (!this.settings.timerEnabled) {
      new import_obsidian2.Notice("Enable the Floating Focus Timer module first.");
      return;
    }
    this.timer.startWork();
    new import_obsidian2.Notice(`Focus session started: ${this.settings.timerWorkMinutes} min`);
  }
  onTimerSnapshot(snap) {
    this.widget.render(snap);
  }
  onWorkComplete(focusMs) {
    this.statsTracker.recordSession(focusMs);
    new import_obsidian2.Notice("Focus session complete! Take a break.");
    this.timer.startBreak();
  }
  /* ------------------------------------------------------------------ */
  /* Settings helpers (used by the settings tab)                         */
  /* ------------------------------------------------------------------ */
  applyTimerVisibility() {
    if (!this.settings.timerEnabled) {
      this.timer.stop();
    }
    this.widget.applyVisibility();
  }
  applyDopamineVisibility() {
    this.dopamine.applyVisibility(this.settings.dopamineEnabled);
  }
  async resetTimerPosition() {
    this.settings.timerPositionX = null;
    this.settings.timerPositionY = null;
    await this.persist();
    this.widget.resetPosition();
    new import_obsidian2.Notice("Timer moved back to top-right.");
  }
  registerCommands() {
    this.addCommand({
      id: "timer-start",
      name: "Start focus session",
      callback: () => this.startWork()
    });
    this.addCommand({
      id: "timer-pause",
      name: "Pause/resume focus session",
      callback: () => {
        if (this.timer.phase === "idle") this.startWork();
        else this.timer.togglePauseResume();
      }
    });
    this.addCommand({
      id: "timer-stop",
      name: "Stop focus session",
      callback: () => this.timer.stop()
    });
    this.addCommand({
      id: "reset-timer-position",
      name: "Reset timer position to top-right",
      callback: () => this.resetTimerPosition()
    });
  }
};
