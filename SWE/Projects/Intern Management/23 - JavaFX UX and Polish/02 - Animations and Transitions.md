---
tags: [concept, javafx, animation, transitions]
type: concept
status: complete
---

# Animations and Transitions

## What it is

JavaFX has a built-in animation framework. Subtle animations (fade, slide, scale) make the app feel polished.

## Common transitions

```java
// Fade
FadeTransition fade = new FadeTransition(Duration.millis(300), node);
fade.setFromValue(0);
fade.setToValue(1);
fade.play();

// Translate (slide)
TranslateTransition slide = new TranslateTransition(Duration.millis(300), node);
slide.setByX(100);
slide.play();

// Scale
ScaleTransition scale = new ScaleTransition(Duration.millis(200), button);
scale.setToX(1.1);
scale.setToY(1.1);
scale.setAutoReverse(true);
scale.setCycleCount(2);
scale.play();
```

## Timeline (custom)

```java
Timeline timeline = new Timeline(
    new KeyFrame(Duration.ZERO, new KeyValue(node.opacityProperty(), 0)),
    new KeyFrame(Duration.millis(300), new KeyValue(node.opacityProperty(), 1))
);
timeline.play();
```

## When to animate

- **View transitions** — fade in new content.
- **Hover effects** — subtle scale on buttons.
- **Loading** — spinner (built-in `ProgressIndicator`).
- **Notifications** — slide-in toast.

## When NOT to animate

- **Data-heavy updates** — animation slows the user down.
- **Distracting motion** — subtle is better.
- **Reduced motion** — some users prefer no animation (accessibility). Respect OS settings.

## Project Connection

The project has a `<Glow/>` effect on form GridPanes — decorative, distracting, reduces contrast. The fix: remove the Glow. Add subtle hover animations on buttons if desired.

## Further reading

- JavaFX Animation tutorial.
