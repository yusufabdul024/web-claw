# Accessibility (WCAG 2.2 AA)

The baseline for every Web Claw project. The QA Agent gates each phase against these checks; the Designer, Animator, and Implementer agents build with these in mind from the start.

## The four POUR principles

1. **Perceivable** — Information presented in ways users can perceive (alt text, captions, contrast).
2. **Operable** — UI is operable by everyone (keyboard, touch, voice).
3. **Understandable** — Content and operation are understandable (clear labels, consistent navigation).
4. **Robust** — Content is robust enough for assistive tech to interpret (valid HTML, ARIA when needed).

## The non-negotiable list

### Color and contrast
- Body text ≥ 4.5:1 against its background.
- Large text (18pt+ or 14pt+ bold) ≥ 3:1.
- UI components (button borders, focus rings, form borders) ≥ 3:1.
- Don't use color alone to convey meaning. Pair with icon, label, or shape.

### Focus
- Every interactive element has a visible focus indicator.
- Focus indicator is ≥ 3:1 contrast against adjacent colors.
- Tab order matches visual order.
- No focus traps (modals must be escapable with Esc; focus must return to the trigger).
- Skip-to-content link present and focusable as the first tabstop.

### Keyboard
- Every interactive element reachable by Tab.
- Every interactive element activatable by Enter (links) or Space (buttons).
- Custom widgets (dropdowns, dialogs, accordions) follow ARIA Authoring Practices keyboard patterns.

### Touch
- Tap targets ≥ 44×44 CSS px (WCAG 2.5.5 AAA; 24px AA minimum, but ship 44).
- Adjacent tap targets have ≥ 8px gap.

### Semantics
- One `<h1>` per page.
- Headings nested correctly (no skipping `<h2>` to `<h4>`).
- Form inputs have associated `<label>`.
- Buttons are `<button>`, not `<div onClick>`.
- Links are `<a href>`, not `<button>` (and vice versa).
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>` on every page.

### Alt text
- Decorative images: `alt=""` (empty alt, present).
- Functional images (clickable icons): describe the action ("Close", "Open menu").
- Content images: describe the content concisely.
- Background images of meaningful content: use real `<img>` with alt, not CSS `background-image`.

### Forms
- Labels visible (avoid placeholder-as-label).
- Required fields marked (`aria-required="true"` and a visible `*` or `(required)`).
- Errors announced via `aria-live="polite"` or `role="alert"`.
- Error messages link to the relevant field (`aria-describedby`).
- Don't disable submit buttons; let the user submit and explain the error.

### Motion
- Honor `prefers-reduced-motion: reduce`. Don't just stop — replace with a static or quiet alternative.
- No flashes more than 3 times per second (seizure risk).
- Auto-playing video must be muted, have controls, and be pauseable.
- Carousels must be pauseable.

### Language
- `<html lang="en">` (or the appropriate locale).
- Mark sections in another language with `lang` attribute.

## Specific to award-winning sites

### Scroll-jacking
Scroll-jacking is the single most-frequently broken accessibility pattern on award-winning sites. Rules:

1. Reduced-motion users get a non-jacked alternative.
2. Keyboard users must be able to skip the jacked section (focus advances past it).
3. Scroll-jacked sections must respect `Esc` (unpin) and respond to high scroll velocity (give up the lock).
4. Screen readers must reach all content within a jacked section without depending on scroll. If captions are positioned absolutely and revealed via opacity, they should be in the DOM as static text underneath.

### Custom cursors
1. Mobile gets a different affordance (haptic + expanded tap target).
2. Custom cursor must be hidden when `prefers-reduced-motion: reduce`.
3. Custom cursor must not hide the actual cursor for users on assistive devices (eye-trackers).

### Custom scrollbars / smooth scroll
1. Lenis et al. must honor reduced-motion. If reduced, fall back to native scroll.
2. Anchored links (`#section`) must still work — instant jumps preserved.
3. Browser keyboard scroll (Space, PgDn, arrow keys) must still work. Lenis already supports this, but verify.

### Glassmorphism and blur backdrops
- Backdrops must not reduce contrast below AA. Measure the worst-case (text over the blurred area of a busy image).

### Videos as design
- Always have a poster image.
- Always `muted` + `playsinline` + `autoplay` only if matter.
- Always have a captions track (`<track kind="captions">`) — even decorative videos benefit from descriptive captions where speech is present.

### Animations on enter / exit
- Test what a screen reader announces during entrance. The text should be readable from the start; opacity:0 + announce-on-reveal is fine for sighted users but should not gate AT users.

## Tools

- **axe DevTools** (Chrome extension) — fastest live audit.
- **pa11y** — CLI; pairs with CI.
- **@axe-core/playwright** — runs axe inside Playwright tests; the CI standard.
- **WAVE** (WebAIM) — visual audit overlay.
- **Lighthouse** — included a11y category, lower-fidelity than axe.
- **NVDA** (Windows) / **VoiceOver** (macOS, iOS) / **TalkBack** (Android) — test with a real screen reader at least once per project.

## Common findings (and fixes)

| Finding                                                | Fix                                                                  |
|--------------------------------------------------------|----------------------------------------------------------------------|
| "Buttons must have discernible text"                   | Add visible text or `aria-label="…"` to icon-only buttons.            |
| "Form elements must have labels"                       | Wrap in `<label>` or use `aria-labelledby`.                          |
| "Heading levels should only increase by one"           | Don't skip from `<h2>` to `<h4>`.                                    |
| "Elements must have sufficient color contrast"         | Bump lightness in OKLCH; re-measure.                                  |
| "Page must have means to bypass repeated blocks"       | Add skip-to-content link as first tabstop.                            |
| "Frame must have a unique title"                       | Add `title` to any `<iframe>`.                                       |
| "img must have alt"                                    | `alt="…"` for content; `alt=""` for decorative.                      |
| "Touch target too small"                               | Increase tap target to 44×44 with padding (CSS).                     |
| "Animations don't honor prefers-reduced-motion"        | Add media query branches.                                            |

## CI gate

Sample Playwright + axe-core test:

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('home page has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

Add one per page. Fail the build on any violation.

## What "passes" doesn't mean accessible

Axe and pa11y catch about 30–40% of real a11y issues. The other 60–70% require:

- Keyboard test the full golden path.
- Screen reader test the home page once per phase.
- Reduced motion test at every phase.
- High-contrast mode test (Windows High Contrast or forced-colors media query).

Run these manually. They are not optional.

## High-contrast mode (`forced-colors: active`)

In high-contrast mode (Windows, some assistive setups), the browser overrides background and text colors. Implications:

- Background images, gradients, shadows are dropped.
- `currentColor` works correctly.
- Use `forced-colors: active` media query to ensure essential UI is still legible.
- Test in Chrome: `chrome://settings/?search=high-contrast` or use `Emulate forced-colors` in Rendering panel.

```css
@media (forced-colors: active) {
  .button {
    border: 1px solid CanvasText;
  }
}
```
