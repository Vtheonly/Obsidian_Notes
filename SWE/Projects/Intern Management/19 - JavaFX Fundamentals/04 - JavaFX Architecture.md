---
tags: [concept, javafx, architecture]
type: concept
status: complete
---

# JavaFX Architecture

## The toolkit stack

```
┌─────────────────────────────────┐
│  Your Application               │
├─────────────────────────────────┤
│  JavaFX Public API              │  (javafx.*)
├─────────────────────────────────┤
│  Prism (Rendering)              │  (graphics pipeline)
├─────────────────────────────────┤
│  Glass (Windowing)              │  (OS window system)
├─────────────────────────────────┤
│  Quantum (Threading)            │  (event dispatch, pulse)
├─────────────────────────────────┤
│  JVM                            │
├─────────────────────────────────┤
│  OS                             │
└─────────────────────────────────┘
```

### Glass
The **windowing toolkit** — wraps the OS's native window system (Win32, X11, Wayland, Cocoa). Handles windows, events, input.

### Prism
The **rendering pipeline** — draws the scene graph. Backends: DirectX (Windows), OpenGL (Linux/macOS), software (fallback).

### Quantum
The **threading layer** — manages the JavaFX Application Thread, the render thread, and the pulse mechanism (60 FPS animation loop).

## The scene graph

JavaFX UIs are a **scene graph** — a tree of `Node` objects. Each node knows how to render itself. The scene graph is **not thread-safe** — only the JavaFX Application Thread may modify it.

## Project Connection

Understanding the architecture explains:
- Why only the Application Thread can touch the UI (the scene graph is not thread-safe).
- Why blocking the Application Thread freezes the UI (no pulses = no rendering).
- Why Swing + JavaFX mix badly (two different windowing/toolkit stacks).

## Further reading

- JavaFX Architecture documentation (Oracle).
