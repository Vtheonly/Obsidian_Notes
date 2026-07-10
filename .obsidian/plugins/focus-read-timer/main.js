const { Plugin, PluginSettingTab, Setting, MarkdownView, Notice } = require("obsidian");

/* ---------- Constants ---------- */
const FLOATING_TIMER_ID = "frt-floating-timer";
const TIMER_DRAG_HEADER_CLASS = "frt-timer-drag-header";
const ADHD_NUDGE_ID = "frt-adhd-nudge";
const DOPAMINE_BAR_ID = "frt-dopamine-bar";
const INJECTED_STYLE_ID = "frt-injected-style";

const DEFAULT_SETTINGS = {
  timerEnabled: true,
  timerWorkMinutes: 25,
  timerBreakMinutes: 5,
  timerAutoHide: true,
  timerAutoHideSeconds: 4,
  timerPauseOnBlur: true,
  timerPositionX: null,   // null = default (top-right)
  timerPositionY: null,
  focusDetectionEnabled: true,
  focusDetectionIdleSeconds: 30,
  nudgeEnabled: false,
  nudgeIdleSeconds: 60,
  nudgeIgnoreScroll: true,  // scroll while reading shouldn't reset the idle timer
  dopamineEnabled: false,
  dopamineDailyGoalMinutes: 60
};

const DEFAULT_STATS = {
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

const PLUGIN_CSS = `
/* Floating timer */
.frt-floating-timer {
  position: fixed !important;
  top: 16px; right: 16px;
  bottom: auto; left: auto;
  background: var(--background-secondary);
  border: 1px solid var(--background-modifier-border);
  border-radius: 10px;
  padding: 0 14px 10px;
  min-width: 220px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
  z-index: 9990;
  font-size: 13px;
  opacity: 1;
  transition: opacity 0.3s, box-shadow 0.2s;
  pointer-events: auto;
  user-select: none;
  -webkit-user-select: none;
  touch-action: none; /* critical: lets pointermove fire on touch without scrolling */
}

/* Drag header — covers the entire top of the timer (handle + label + time).
   This is a LARGE grab surface so the user can drag from anywhere in the
   top portion of the box, not just a tiny strip. */
.frt-timer-drag-header {
  cursor: grab;
  padding: 8px 0 6px;
  margin: 0 -14px 4px;
  padding-left: 14px;
  padding-right: 14px;
  border-bottom: 1px solid var(--background-modifier-border);
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--background-primary-alt, var(--background-modifier-border));
  border-radius: 10px 10px 0 0;
  font-size: 11px;
  color: var(--text-muted);
  touch-action: none;
}
.frt-timer-drag-header:active { cursor: grabbing; }
.frt-floating-timer.frt-dragging {
  transition: none;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
  cursor: grabbing !important;
}
.frt-drag-grip {
  font-size: 14px;
  line-height: 1;
  opacity: 0.5;
  flex-shrink: 0;
}
.frt-drag-label-text {
  flex: 1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 10px;
}

.frt-timer-time {
  font-size: 28px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  margin: 4px 0 4px;
  text-align: center;
}
.frt-timer-bar {
  height: 4px;
  background: var(--background-modifier-border);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 4px;
}
.frt-timer-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #66bb6a, #42a5f5);
  width: 0%;
  transition: width 0.3s;
}
.frt-timer-xp {
  font-size: 11px;
  color: #ff9800;
  font-weight: 600;
  text-align: center;
  min-height: 14px;
}
.frt-timer-controls {
  display: flex;
  gap: 6px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--background-modifier-border);
}
.frt-timer-btn {
  flex: 1;
  background: var(--background-modifier-border);
  color: var(--text-normal);
  border: 1px solid transparent;
  border-radius: 5px;
  padding: 6px 0;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, transform 0.05s;
  user-select: none;
  -webkit-user-select: none;
  pointer-events: auto;
  touch-action: manipulation;
}
.frt-timer-btn:hover:not(:disabled) { background: var(--background-modifier-border-hover, var(--interactive-accent-hover)); }
.frt-timer-btn:active:not(:disabled) { transform: scale(0.96); }
.frt-timer-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.frt-timer-btn-primary { background: var(--interactive-accent); color: var(--text-on-accent); }
.frt-timer-btn-primary:hover:not(:disabled) { background: var(--interactive-accent-hover); }
.frt-timer-btn-stop:hover:not(:disabled) { background: #e53935; color: white; border-color: #c62828; }
.frt-timer-btn-add:hover:not(:disabled) { background: #43a047; color: white; border-color: #2e7d32; }

/* ADHD Nudge */
.frt-adhd-nudge {
  position: fixed !important;
  top: 50% !important; left: 50% !important;
  bottom: auto !important; right: auto !important;
  transform: translate(-50%, -50%) !important;
  background: var(--background-secondary);
  border: 1px solid #ff9800;
  border-radius: 10px;
  padding: 18px 22px;
  box-shadow: 0 0 0 100vmax rgba(0, 0, 0, 0.45), 0 6px 20px rgba(0, 0, 0, 0.25);
  z-index: 9997;
  max-width: min(360px, 90vw);
  animation: frt-nudge-in 0.3s ease-out;
}
@keyframes frt-nudge-in {
  from { transform: translate(-50%, calc(-50% + 20px)) !important; opacity: 0; }
  to { transform: translate(-50%, -50%) !important; opacity: 1; }
}
.frt-nudge-title { font-weight: 600; margin-bottom: 4px; }
.frt-nudge-body { color: var(--text-muted); font-size: 13px; margin-bottom: 10px; }
.frt-nudge-actions { display: flex; gap: 8px; }
.frt-nudge-actions button {
  background: var(--interactive-accent);
  color: var(--text-on-accent);
  border: none;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
}
.frt-nudge-actions button.frt-nudge-dismiss {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--background-modifier-border);
}

/* Dopamine bar */
.frt-dopamine-bar {
  position: fixed !important;
  bottom: 0 !important; left: 0 !important; right: 0 !important;
  top: auto !important;
  height: 4px;
  background: var(--background-modifier-border);
  z-index: 9989;
  pointer-events: none;
}
.frt-dopamine-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff9800, #ff5722);
  width: 0%;
  transition: width 0.4s;
}
.frt-dopamine-bar-label {
  position: fixed !important;
  bottom: 8px !important; right: 8px !important;
  top: auto !important; left: auto !important;
  font-size: 11px;
  color: var(--text-muted);
  z-index: 9989;
  pointer-events: none;
  background: var(--background-secondary);
  padding: 2px 6px;
  border-radius: 4px;
}
`;

/* ---------- Helpers ---------- */
function formatDate(d) {
  d = d || new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
function dayDiff(a, b) {
  if (!a || !b) return 0;
  return Math.round((new Date(b + "T00:00:00").getTime() - new Date(a + "T00:00:00").getTime()) / 86400000);
}

/* ---------- Plugin ---------- */
class TimerPlugin extends Plugin {
  async onload() {
    await this.loadData_();
    this.injectCSS();

    // Timer state
    this.state = "idle";   // idle | running | paused | break
    this.remainingMs = 0;
    this.totalMs = 0;
    this.accumulatedMs = 0;
    this.lastTick = 0;
    this.raf = null;
    this.lastActivity = Date.now();         // for focus detection (timer)
    this.lastInputActivity = Date.now();    // for ADHD nudge — excludes scroll
    this.windowFocused = true;
    this.autoHideTimer = null;
    this.idleCheckInterval = null;

    // Independent reading-time tracker — feeds the dopamine bar
    // so it shows progress even when the timer module is disabled.
    this.activeSince = Date.now();
    this.lastStatsSave = 0;

    this.createTimerElement();
    this.createDopamineBar();
    this.attachListeners();
    this.applyTimerVisibility();
    this.applyDopamineVisibility();
    this.renderTimer();
    this.renderDopamineBar();
    this.rollOverStats();

    // Periodic refresh
    this.dopamineInterval = window.setInterval(() => this.renderDopamineBar(), 5000);
    this.flushInterval = window.setInterval(() => this.flushReadingTime(), 30000);

    this.addSettingTab(new TimerSettingTab(this.app, this));
    this.registerCommands();
  }

  async onunload() {
    if (this.raf) cancelAnimationFrame(this.raf);
    if (this.idleCheckInterval) clearInterval(this.idleCheckInterval);
    if (this.dopamineInterval) clearInterval(this.dopamineInterval);
    if (this.flushInterval) clearInterval(this.flushInterval);
    if (this.autoHideTimer) clearTimeout(this.autoHideTimer);
    this.flushReadingTime();
    if (this._listeners) {
      for (const [evt, fn, opts] of this._listeners) window.removeEventListener(evt, fn, opts);
    }
    const t = document.getElementById(FLOATING_TIMER_ID);
    if (t) t.remove();
    const n = document.getElementById(ADHD_NUDGE_ID);
    if (n) n.remove();
    const d = document.getElementById(DOPAMINE_BAR_ID);
    if (d) d.remove();
    const dl = document.getElementById(DOPAMINE_BAR_ID + "-label");
    if (dl) dl.remove();
    const s = document.getElementById(INJECTED_STYLE_ID);
    if (s) s.remove();
  }

  async loadData_() {
    const data = await this.loadData();
    this.settings = Object.assign({}, DEFAULT_SETTINGS, data && data.settings || {});
    this.stats = Object.assign({}, DEFAULT_STATS, data && data.stats || {});
    if (!this.stats.perDayMs) this.stats.perDayMs = {};
  }
  async saveAll() { await this.saveData({ settings: this.settings, stats: this.stats }); }

  injectCSS() {
    let s = document.getElementById(INJECTED_STYLE_ID);
    if (!s) { s = document.createElement("style"); s.id = INJECTED_STYLE_ID; document.head.appendChild(s); }
    s.textContent = PLUGIN_CSS;
  }

  createTimerElement() {
    if (document.getElementById(FLOATING_TIMER_ID)) return;
    const el = document.createElement("div");
    el.id = FLOATING_TIMER_ID;
    el.className = "frt-floating-timer";
    el.style.display = "none";
    el.innerHTML = `
      <div class="${TIMER_DRAG_HEADER_CLASS}" title="Drag to move the timer">
        <span class="frt-drag-grip">⠿</span>
        <span class="frt-drag-label-text">Reading Timer</span>
        <span class="frt-drag-grip">⠿</span>
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

    // Wire up control buttons — stop pointerdown from initiating a drag
    const controls = el.querySelector(".frt-timer-controls");
    controls.addEventListener("pointerdown", e => e.stopPropagation());
    controls.addEventListener("click", e => {
      const btn = e.target.closest(".frt-timer-btn");
      if (!btn) return;
      e.stopPropagation();
      this.handleControlClick(btn.getAttribute("data-action"));
    });

    this.applySavedPosition(el);
    this.attachDragHandlers(el);
  }

  applySavedPosition(el) {
    const { timerPositionX, timerPositionY } = this.settings;
    if (typeof timerPositionX === "number" && typeof timerPositionY === "number") {
      // Switch from corner-anchored (top/right) to explicit top/left.
      el.style.right = "auto";
      el.style.left = `${timerPositionX}px`;
      el.style.top = `${timerPositionY}px`;
    }
  }

  /* ----- Drag handling (pointer events — works for mouse + touch + pen) ----- */
  attachDragHandlers(el) {
    const header = el.querySelector("." + TIMER_DRAG_HEADER_CLASS);
    if (!header) return;

    let dragging = false;
    let offsetX = 0;
    let offsetY = 0;
    let pointerId = null;

    const onPointerDown = (e) => {
      // Only start drag on primary button (left-click / touch / pen)
      if (e.button !== undefined && e.button !== 0) return;
      dragging = true;
      pointerId = e.pointerId;

      const rect = el.getBoundingClientRect();
      offsetX = e.clientX - rect.left;
      offsetY = e.clientY - rect.top;
      el.classList.add("frt-dragging");

      // Pin to current position by switching from corner-anchored to explicit left/top
      el.style.right = "auto";
      el.style.left = `${rect.left}px`;
      el.style.top = `${rect.top}px`;

      // Capture the pointer so pointermove/pointerup keep firing even if
      // the cursor leaves the header element (e.g. when dragging fast).
      try { header.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ }

      e.preventDefault();
      e.stopPropagation();
    };

    const onPointerMove = (e) => {
      if (!dragging) return;
      if (e.pointerId !== pointerId) return;
      const x = Math.max(0, Math.min(window.innerWidth - 80, e.clientX - offsetX));
      const y = Math.max(0, Math.min(window.innerHeight - 40, e.clientY - offsetY));
      el.style.left = `${x}px`;
      el.style.top = `${y}px`;
      e.preventDefault();
    };

    const onPointerUp = async (e) => {
      if (!dragging) return;
      if (e.pointerId !== pointerId) return;
      dragging = false;
      pointerId = null;
      el.classList.remove("frt-dragging");
      try { header.releasePointerCapture(e.pointerId); } catch (err) { /* ignore */ }

      const rect = el.getBoundingClientRect();
      this.settings.timerPositionX = Math.round(rect.left);
      this.settings.timerPositionY = Math.round(rect.top);
      await this.saveAll();
    };

    // Use pointer events (unified mouse + touch + pen)
    header.addEventListener("pointerdown", onPointerDown);
    header.addEventListener("pointermove", onPointerMove);
    header.addEventListener("pointerup", onPointerUp);
    header.addEventListener("pointercancel", onPointerUp);

    // Prevent the context menu from interrupting a drag on right-click
    header.addEventListener("contextmenu", e => { if (dragging) e.preventDefault(); });
  }

  createDopamineBar() {
    if (document.getElementById(DOPAMINE_BAR_ID)) return;
    const bar = document.createElement("div");
    bar.id = DOPAMINE_BAR_ID;
    bar.className = "frt-dopamine-bar";
    bar.innerHTML = `<div class="frt-dopamine-bar-fill"></div>`;
    bar.style.display = "none";
    document.body.appendChild(bar);

    const label = document.createElement("div");
    label.id = DOPAMINE_BAR_ID + "-label";
    label.className = "frt-dopamine-bar-label";
    label.style.display = "none";
    document.body.appendChild(label);
  }

  attachListeners() {
    this._listeners = [];
    const add = (evt, fn, opts) => {
      window.addEventListener(evt, fn, opts);
      this._listeners.push([evt, fn, opts]);
    };

    // Focus-detection activity (mouse + keyboard + scroll + touch).
    // This drives `lastActivity` for the timer's focus-detection feature.
    add("mousemove", () => this.onActivity(false), { passive: true });
    add("keydown", () => this.onActivity(true),  { passive: true });
    add("scroll",   () => this.onActivity(this.settings.nudgeIgnoreScroll ? false : true), { passive: true });
    add("touchstart", () => this.onActivity(true), { passive: true });

    add("blur", () => {
      this.windowFocused = false;
      if (this.settings.timerPauseOnBlur && this.state === "running") this.pause("Window lost focus");
    });
    add("focus", () => { this.windowFocused = true; this.onActivity(true); });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        if (this.settings.timerPauseOnBlur && this.state === "running") this.pause("Tab hidden");
      } else this.onActivity(true);
    });

    this.idleCheckInterval = window.setInterval(() => this.checkIdle(), 5000);
  }

  /* ----- Visibility (timer-only, no longer gates dopamine bar) ----- */
  applyTimerVisibility() {
    const el = document.getElementById(FLOATING_TIMER_ID);
    if (!el) return;
    if (!this.settings.timerEnabled) {
      el.style.display = "none";
      this.stop();
      return;
    }
    el.style.display = "block";
    this.resetAutoHide();
    this.renderTimer();
  }

  applyDopamineVisibility() {
    const bar = document.getElementById(DOPAMINE_BAR_ID);
    const label = document.getElementById(DOPAMINE_BAR_ID + "-label");
    const visible = this.settings.dopamineEnabled;
    if (bar)   bar.style.display   = visible ? "block" : "none";
    if (label) label.style.display = visible ? "block" : "none";
    if (visible) this.renderDopamineBar();
  }

  /* ----- Timer controls ----- */
  start() {
    if (!this.settings.timerEnabled) {
      new Notice("Enable the Floating Focus Timer module first.");
      return;
    }
    this.totalMs = this.settings.timerWorkMinutes * 60000;
    this.remainingMs = this.totalMs;
    this.state = "running";
    this.lastTick = performance.now();
    this.accumulatedMs = 0;
    this.show();
    this.tick();
    new Notice(`Focus session started: ${this.settings.timerWorkMinutes} min`);
  }

  handleControlClick(action) {
    if (action === "start") this.start();
    else if (action === "pause") {
      if (this.state === "running") { this.pause(); this.renderTimer(); }
      else if (this.state === "paused") { this.resume(); this.renderTimer(); }
    } else if (action === "addtime") {
      this.addTime(30000);
      this.renderTimer();
    } else if (action === "stop") {
      if (this.state !== "idle") { this.stop(); this.renderTimer(); new Notice("Timer stopped."); }
    }
  }

  pause(reason) {
    if (this.state === "running") {
      this.state = "paused";
      if (this.raf) { cancelAnimationFrame(this.raf); this.raf = null; }
      if (reason) new Notice(`Paused: ${reason}`);
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
    if (this.raf) { cancelAnimationFrame(this.raf); this.raf = null; }
    this.state = "idle";
    this.remainingMs = 0;
    const el = document.getElementById(FLOATING_TIMER_ID);
    if (el) {
      if (!this.settings.timerEnabled) el.style.display = "none";
      else this.renderTimer();
    }
  }

  addTime(ms) {
    if (this.state === "idle" || this.state === "break") return;
    this.remainingMs += ms;
    this.totalMs += ms;
    new Notice(`Added ${Math.round(ms / 1000)}s`);
  }

  isRunning() { return this.state === "running"; }
  getState() { return this.state; }
  getRemainingMs() { return this.remainingMs; }

  tick() {
    if (this.state !== "running" && this.state !== "break") return;
    const now = performance.now();
    const elapsed = now - this.lastTick;
    this.lastTick = now;
    this.remainingMs = Math.max(0, this.remainingMs - elapsed);

    const isFocused = !this.settings.focusDetectionEnabled ||
      (this.windowFocused && (Date.now() - this.lastActivity < this.settings.focusDetectionIdleSeconds * 1000));

    if (this.state === "running" && isFocused) {
      this.accumulatedMs += elapsed;
    }

    this.renderTimer();
    if (this.remainingMs <= 0) { this.complete(); return; }
    this.raf = requestAnimationFrame(() => this.tick());
  }

  complete() {
    const isBreak = this.state === "break";
    const acc = this.accumulatedMs;
    this.stop();
    if (!isBreak) {
      // Session end — record longest focus
      this.stats.sessionsToday = (this.stats.sessionsToday || 0) + 1;
      if (acc > this.stats.longestFocusMs) this.stats.longestFocusMs = acc;
      this.saveAll();
      new Notice("Focus session complete! Take a break.");
      this.startBreak();
    } else {
      new Notice("Break over. Ready for another session?");
    }
  }

  startBreak() {
    if (!this.settings.timerEnabled) return;
    this.totalMs = this.settings.timerBreakMinutes * 60000;
    this.remainingMs = this.totalMs;
    this.state = "break";
    this.lastTick = performance.now();
    this.accumulatedMs = 0;
    this.show();
    this.tick();
  }

  show() {
    if (this.settings.timerEnabled) {
      const el = document.getElementById(FLOATING_TIMER_ID);
      if (el) el.style.display = "block";
      this.resetAutoHide();
    }
  }

  resetAutoHide() {
    if (this.settings.timerAutoHide) {
      if (this.autoHideTimer) clearTimeout(this.autoHideTimer);
      this.autoHideTimer = window.setTimeout(() => {
        const el = document.getElementById(FLOATING_TIMER_ID);
        if (el && this.state === "idle") el.style.opacity = "0.55";
      }, this.settings.timerAutoHideSeconds * 1000);
    }
  }

  /**
   * Activity handler.
   * @param {boolean} countsAsInput  true for keyboard/touch (resets nudge idle timer);
   *                                 false for scroll/mousemove (does not reset nudge
   *                                 idle timer, so the nudge can still fire while reading).
   */
  onActivity(countsAsInput) {
    this.lastActivity = Date.now();
    if (countsAsInput || !this.settings.nudgeIgnoreScroll) {
      this.lastInputActivity = Date.now();
    }
    const el = document.getElementById(FLOATING_TIMER_ID);
    if (el) { el.style.opacity = "1"; this.resetAutoHide(); }
    // Only auto-hide the nudge on a real input event, not on passive scroll
    if (countsAsInput || !this.settings.nudgeIgnoreScroll) {
      this.hideNudge();
    }
  }

  checkIdle() {
    if (!this.settings.nudgeEnabled) return;
    const idleMs = Date.now() - this.lastInputActivity;
    if (idleMs >= this.settings.nudgeIdleSeconds * 1000) {
      this.showNudge();
    }
  }

  showNudge() {
    if (document.getElementById(ADHD_NUDGE_ID)) return;
    const nudge = document.createElement("div");
    nudge.id = ADHD_NUDGE_ID;
    nudge.className = "frt-adhd-nudge";

    let body;
    if (this.state === "running" && this.remainingMs > 0) {
      const minLeft = Math.ceil(this.remainingMs / 60000);
      body = `Continue? ${minLeft} min left in session.`;
    } else {
      body = `You've been idle for ${this.settings.nudgeIdleSeconds}s. Get back to reading?`;
    }

    nudge.innerHTML = `
      <div class="frt-nudge-title">You stopped reading.</div>
      <div class="frt-nudge-body">${body}</div>
      <div class="frt-nudge-actions">
        <button class="frt-nudge-continue">Continue</button>
        <button class="frt-nudge-dismiss">Dismiss</button>
      </div>`;
    document.body.appendChild(nudge);
    nudge.querySelector(".frt-nudge-continue").addEventListener("click", () => {
      this.onActivity(true);
      nudge.remove();
    });
    nudge.querySelector(".frt-nudge-dismiss").addEventListener("click", () => nudge.remove());
  }

  hideNudge() {
    const n = document.getElementById(ADHD_NUDGE_ID);
    if (n) n.remove();
  }

  /* ----- Rendering ----- */
  renderTimer() {
    const el = document.getElementById(FLOATING_TIMER_ID);
    if (!el) return;
    const s = this.settings;

    const updateButtons = (state) => {
      const start = el.querySelector('[data-action="start"]');
      const pause = el.querySelector('[data-action="pause"]');
      const addtime = el.querySelector('[data-action="addtime"]');
      const stop = el.querySelector('[data-action="stop"]');
      if (start) {
        start.disabled = !(state === "idle" || state === "break");
        start.textContent = state === "break" ? "Skip Break" : "Start";
      }
      if (pause) {
        if (state === "running") { pause.disabled = false; pause.textContent = "Pause"; }
        else if (state === "paused") { pause.disabled = false; pause.textContent = "Resume"; }
        else { pause.disabled = true; pause.textContent = "Pause"; }
      }
      if (addtime) addtime.disabled = state === "idle" || state === "break";
      if (stop) stop.disabled = state === "idle";
    };

    if (this.state === "idle") {
      const lbl = el.querySelector(".frt-drag-label-text");
      if (lbl) lbl.textContent = "Ready — drag me";
      const tm = el.querySelector(".frt-timer-time");
      if (tm) tm.textContent = `${String(s.timerWorkMinutes).padStart(2, "0")}:00`;
      const fill = el.querySelector(".frt-timer-bar-fill"); if (fill) fill.style.width = "0%";
      const xp = el.querySelector(".frt-timer-xp"); if (xp) xp.textContent = "Click Start to begin";
      updateButtons("idle");
      return;
    }

    const totalSec = Math.ceil(this.remainingMs / 1000);
    const m = Math.floor(totalSec / 60), sec = totalSec % 60;
    const tm = el.querySelector(".frt-timer-time");
    if (tm) tm.textContent = `${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
    const lbl = el.querySelector(".frt-drag-label-text");
    if (lbl) lbl.textContent = this.state === "break" ? "Break" : this.state === "paused" ? "Paused" : "Reading";
    const pct = this.totalMs > 0 ? (1 - this.remainingMs / this.totalMs) * 100 : 0;
    const fill = el.querySelector(".frt-timer-bar-fill");
    if (fill) fill.style.width = `${pct}%`;
    const xp = el.querySelector(".frt-timer-xp");
    if (xp) xp.textContent = this.state === "break" ? "On break" : `+${Math.round(this.accumulatedMs / 60000)} min`;
    updateButtons(this.state);
  }

  renderDopamineBar() {
    if (!this.settings.dopamineEnabled) return;
    const bar = document.getElementById(DOPAMINE_BAR_ID);
    const label = document.getElementById(DOPAMINE_BAR_ID + "-label");
    if (!bar || !label) return;
    this.rollOverStats();
    const todayMin = Math.round(this.stats.todayMs / 60000);
    const goal = this.settings.dopamineDailyGoalMinutes;
    const pct = Math.min(100, Math.round((todayMin / goal) * 100));
    const fill = bar.querySelector(".frt-dopamine-bar-fill");
    if (fill) fill.style.width = `${pct}%`;
    label.textContent = `${todayMin} / ${goal} min (${pct}%)`;
  }

  /* ----- Stats / reading time ----- */
  rollOverStats() {
    const today = formatDate();
    if (this.stats.todayDate !== today) {
      if (this.stats.lastReadDate) {
        const diff = dayDiff(this.stats.lastReadDate, today);
        if (diff === 1) this.stats.streak = (this.stats.streak || 0) + 1;
        else if (diff > 1) this.stats.streak = 1;
      } else this.stats.streak = 1;
      this.stats.longestStreak = Math.max(this.stats.longestStreak || 0, this.stats.streak);
      this.stats.todayMs = 0;
      this.stats.sessionsToday = 0;
      this.stats.todayDate = today;
      this.saveAll();
    }
  }

  /**
   * Independent reading-time tracker.
   * This runs regardless of timer state, so the dopamine bar can show
   * progress even when the focus timer is disabled or idle.
   */
  flushReadingTime() {
    const now = Date.now();
    let delta = now - this.activeSince;
    // Cap at 5 min — avoids huge jumps when the laptop slept
    if (delta > 300000) delta = 300000;
    if (delta < 1000) { this.activeSince = now; return; }

    // Only count if the window is focused (don't count background tab time)
    if (!this.windowFocused) { this.activeSince = now; return; }

    this.rollOverStats();
    this.stats.totalReadingMs += delta;
    this.stats.todayMs += delta;
    this.stats.lastReadDate = formatDate();
    const today = formatDate();
    this.stats.perDayMs[today] = (this.stats.perDayMs[today] || 0) + delta;
    this.activeSince = now;

    if (now - this.lastStatsSave > 10000) {
      this.lastStatsSave = now;
      this.saveAll();
    }
    // Live-update the dopamine bar when significant time accrues
    if (this.settings.dopamineEnabled) this.renderDopamineBar();
  }

  registerCommands() {
    this.addCommand({ id: "timer-start", name: "Start Focus Session", callback: () => this.start() });
    this.addCommand({
      id: "timer-pause", name: "Pause/Resume Focus Session",
      callback: () => {
        if (this.state === "running") this.pause();
        else if (this.state === "paused") this.resume();
        else this.start();
      }
    });
    this.addCommand({ id: "timer-stop", name: "Stop Focus Session", callback: () => this.stop() });

    this.addCommand({
      id: "reset-timer-position",
      name: "Reset Timer Position to Top-Right",
      callback: async () => {
        this.settings.timerPositionX = null;
        this.settings.timerPositionY = null;
        await this.saveAll();
        const el = document.getElementById(FLOATING_TIMER_ID);
        if (el) {
          el.style.left = "";
          el.style.top = "";
          el.style.right = "16px";
          el.style.top = "16px";
        }
        new Notice("Timer moved back to top-right.");
      }
    });
  }
}

/* ---------- Settings Tab ---------- */
class TimerSettingTab extends PluginSettingTab {
  constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    this.section("Floating Focus Timer");
    this.toggle("Enable floating timer", "Show the floating timer box (draggable via its top handle).", "timerEnabled");
    this.slider("Work minutes", 5, 90, 1, "timerWorkMinutes");
    this.slider("Break minutes", 1, 30, 1, "timerBreakMinutes");
    this.toggle("Auto-hide timer", "Dim the timer box when idle.", "timerAutoHide");
    this.slider("Auto-hide after (s)", 1, 30, 1, "timerAutoHideSeconds");
    this.toggle("Pause on window blur", "Pause when Obsidian loses focus.", "timerPauseOnBlur");

    this.section("Focus Detection");
    this.toggle("Enable focus detection", "Only count time when the user is active.", "focusDetectionEnabled");
    this.slider("Idle seconds", 10, 300, 5, "focusDetectionIdleSeconds");

    this.section("ADHD Nudge");
    this.toggle("Enable idle nudge", "Pop a modal when you stop reading (works even without a running timer).", "nudgeEnabled");
    this.slider("Idle threshold (s)", 10, 300, 5, "nudgeIdleSeconds");
    this.toggle("Don't count scroll as activity", "Recommended ON — scrolling while reading shouldn't reset the idle timer.", "nudgeIgnoreScroll");

    this.section("Dopamine Bar");
    this.toggle("Enable daily goal bar", "Bottom bar showing today's reading vs goal (works independently of the timer).", "dopamineEnabled");
    this.slider("Daily goal (minutes)", 5, 240, 5, "dopamineDailyGoalMinutes");

    containerEl.createEl("p", {
      cls: "fr-setting-hint",
      text: "Drag the timer by its top header bar (the strip labeled \"Reading Timer\" with ⠿ grip icons). Use the command palette → \"Reset Timer Position\" to snap it back to the top-right corner."
    });
  }

  section(text) { this.containerEl.createEl("h2", { text }); }

  toggle(name, desc, key) {
    new Setting(this.containerEl).setName(name).setDesc(desc)
      .addToggle(cb => cb.setValue(this.plugin.settings[key])
        .onChange(async v => {
          this.plugin.settings[key] = v;
          await this.plugin.saveAll();
          // Apply the right visibility helper depending on which key changed
          if (key === "timerEnabled")   this.plugin.applyTimerVisibility();
          if (key === "dopamineEnabled") this.plugin.applyDopamineVisibility();
          if (key === "nudgeIgnoreScroll" && !v) this.plugin.onActivity(true);
          this.display();
        }));
  }
  slider(name, min, max, step, key) {
    new Setting(this.containerEl).setName(name)
      .addSlider(cb => cb.setLimits(min, max, step).setValue(this.plugin.settings[key]).setDynamicTooltip()
        .onChange(async v => {
          this.plugin.settings[key] = v;
          await this.plugin.saveAll();
          this.plugin.renderTimer();
          if (key === "dopamineDailyGoalMinutes") this.plugin.renderDopamineBar();
        }));
  }
}

module.exports = TimerPlugin;
