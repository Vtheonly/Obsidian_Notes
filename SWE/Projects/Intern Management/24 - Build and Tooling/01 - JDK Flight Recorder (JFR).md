---
tags: [concept, build, profiling, jfr]
type: concept
status: complete
related:
  - [[28 - Observability/00 - MOC - Observability]]
---

# JDK Flight Recorder (JFR)

## What it is

**JFR** (JDK Flight Recorder) is Java's built-in profiler. Low overhead (< 1%), production-safe. Records events (GC, allocations, locks, I/O) for later analysis.

## Usage

```bash
# Start app with JFR
java -XX:StartFlightRecording=duration=60s,filename=app.jfr -jar app.jar

# Or attach to a running JVM
jcmd <pid> JFR.start duration=60s filename=app.jfr
```

## Analysis

Open `app.jfr` in **JDK Mission Control** (JMC) — a GUI tool for analyzing recordings.

What you can see:
- CPU samples (which methods are hot).
- Allocations (which methods allocate most).
- GC pauses (frequency, duration).
- Lock contention (which locks are contended).
- I/O (file, socket — which calls block).
- Exception counts.

## When to use

- **Performance investigation** — "why is the app slow?"
- **Production profiling** — JFR's overhead is low enough for prod.
- **Memory leaks** — heap analysis.

## Alternatives

- **async-profiler** — open-source, low-overhead CPU/heap profiler.
- **VisualVM** — older, simpler.
- **YourKit / JProfiler** — commercial, powerful.

## Project Connection

For the refactored app, JFR can diagnose:
- DB query bottlenecks (which queries are slow).
- Connection pool contention.
- UI freezes (which events block the Application Thread).

## Further reading

- JEP 328 (JFR).
- JDK Mission Control documentation.
