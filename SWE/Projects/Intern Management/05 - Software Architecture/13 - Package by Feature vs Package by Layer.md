---
tags: [concept, architecture, packaging]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[32 - Putting It All Together/11 - Target Package Structure]]
---

# Package by Feature vs Package by Layer

## What it is

How you organize your packages affects readability, maintainability, and coupling. Two common approaches:

### Package by Layer
```
com.example.internmanagement
├── controller/
│   ├── LoginController.java
│   ├── InternController.java
│   └── UserController.java
├── service/
│   ├── AuthService.java
│   ├── InternService.java
│   └── UserService.java
├── repository/
│   ├── InternRepository.java
│   ├── UserRepository.java
│   └── OracleInternRepository.java
└── domain/
    ├── Intern.java
    └── User.java
```

Pros: clear separation of layers.
Cons: to add a feature (e.g., "manage interns"), you touch 4 packages. Cohesion is low — `InternController`, `InternService`, `InternRepository` are scattered.

### Package by Feature
```
com.example.internmanagement
├── auth/
│   ├── AuthController.java
│   ├── AuthService.java
│   ├── UserRepository.java
│   └── User.java
├── interns/
│   ├── InternController.java
│   ├── InternService.java
│   ├── InternRepository.java
│   └── Intern.java
└── shared/
    └── DatabaseConfig.java
```

Pros: high cohesion — everything about interns is in one package. To add a feature, you add one package. To delete a feature, you delete one package.
Cons: layer boundaries are less obvious; harder to enforce "controllers don't call repositories directly."

## Which to choose?

- **Small apps** (< 50 classes): package by layer is fine.
- **Medium apps** (50-500 classes): package by feature is usually better.
- **Large apps** (> 500 classes): package by feature, with sub-packages for layer within each feature.

The project has 11 classes, all in one package. Package by layer would be a good first step. As the app grows to 50+ classes (after the refactoring roadmap), package by feature becomes better.

## The "Screaming Architecture" test

> "If you look at the package structure of your application, can you tell what the application does?" — Robert C. Martin

Package by layer: `controller`, `service`, `repository` — tells you the *architecture*, not the *domain*.
Package by feature: `auth`, `interns`, `users`, `reports` — tells you the *domain*. The architecture "screams" what the app does.

## The project's package structure

All 11 classes in one package (`com.example.intern_manegement_app`). No structure at all. The refactoring roadmap (Phase 2) introduces package by feature (or layer, for a small app).

## Common pitfalls

- **Cyclic package dependencies** — `interns` depends on `users`, `users` depends on `interns`. Break the cycle (extract shared code, or use events).
- **God package** — `common` or `shared` that has everything. Split.
- **Package by type** — `exceptions`, `dto`, `validators` — packages by *kind* of class, not by feature. Hard to navigate.

## Further reading

- *Clean Architecture* (Martin), "Screaming Architecture."
- *Single Responsibility Principle* applied to packages.
