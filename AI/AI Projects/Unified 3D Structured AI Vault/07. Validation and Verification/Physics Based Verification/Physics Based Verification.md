---
tags: [verification, physics]
---

# Physics-Based Verification

> **Definition.** *Physics-based verification* uses physical simulation to verify that the model satisfies physical laws: static equilibrium, heat transfer, fluid flow, acoustics.

## Static Equilibrium

For a structural model:

- Compute expected loads (dead, live, wind, seismic).
- Solve $K u = f$ for displacements.
- Check stresses are within material limits.
- Check reactions at supports are non-negative (no tension at a foundation).

If the model fails, the structure is physically unstable.

## Thermal Simulation

For an energy model:

- Compute heat transfer through walls, windows, roof.
- Check indoor temperatures stay within comfort range.
- Check energy consumption is within budget.

## Acoustic Simulation

For an acoustic model:

- Compute reverberation times.
- Check speech intelligibility in classrooms.
- Check noise levels in residential units.

## Strengths

- Catches errors that pure geometric or topological checks miss.
- Provides quantitative measures (stress, temperature, dB).

## Limitations

- Requires material properties, boundary conditions, loads.
- Expensive (FEA is slow for large models).
- Sensitive to modeling assumptions.

See [[Structural Validation]], [[Formal Verification]], [[Hybrid Verification]].

## Related Concepts

- [[Structural Validation]]
- [[Formal Verification]]
- [[Hybrid Verification]]
