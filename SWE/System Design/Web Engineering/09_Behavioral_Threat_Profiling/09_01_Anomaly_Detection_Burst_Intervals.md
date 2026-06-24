## 8.1. Time-Series Anomaly Detection and Burst Intervals

Detecting network attacks using static signatures (like blacklists) is fragile. Sophisticated defense engines analyze the **behavioral time-series signatures** of network devices to identify anomalies and malicious activity.

---

### 1. Analyzing Inter-Packet Arrival Times (Burst Intervals)

Most automated network attack tools (such as ARP poisoning utilities like Ettercap, Cain & Abel, or custom python scripts) are configured to inject spoofed packets at a high, consistent frequency to ensure the target host's cache remains poisoned.

By calculating the precise time delta (the **Burst Interval**) between consecutive packets received from a specific MAC address, we can construct a behavioral signature:

$$\Delta t_n = t_n - t_{n-1}$$

```
Legitimate Host Traffic (Sparse, variable intervals):
Frame 1 (t=0) ──────► Frame 2 (t=14.2s) ───────────► Frame 3 (t=19.8s)
Burst Intervals: [14.2s, 5.6s]

Attacker Tool Traffic (Dense, highly consistent intervals):
Frame 1 (t=0) ──► Frame 2 (t=0.5s) ──► Frame 3 (t=1.0s) ──► Frame 4 (t=1.5s)
Burst Intervals: [0.50s, 0.50s, 0.50s]
```

* **Legitimate Traffic:** Characterized by sparse, highly variable intervals, triggered by human actions (like browsing a website or clicking a link).
* **Attacker Tool Traffic:** Characterized by dense, highly consistent intervals, reflecting the automated timers of the attack software.

---

### 2. Algorithmic Burst Interval Analysis

To detect these behavioral signatures, the threat intelligence engine maintains a rolling queue of incoming packet timestamps for each local MAC address:

```python
# Rolling burst-interval queue logic
def record_event(self, now):
    if self.timestamps:
        last = self.timestamps[-1]
        delta = now - last
        self.burst_intervals.append(round(delta, 4))
        # Keep only the last 100 intervals to bound memory
        self.burst_intervals = self.burst_intervals[-100:]
    self.timestamps.append(now)
```

By tracking the statistical variance of this queue, the engine can identify automated attack scripts, even if the attacker alters the packet payloads to bypass static signature rules.

---

###  Common Student Pitfalls & Pro-Tips
* **Network Jitter Noise:** In real-world networks (especially busy Wi-Fi environments), physical congestion and wireless interference can introduce random timing delays, known as **Jitter**. When designing a timing-based anomaly detector, always implement a tolerance threshold (noise filter) to prevent natural network jitter from triggering false positive alerts.

---
