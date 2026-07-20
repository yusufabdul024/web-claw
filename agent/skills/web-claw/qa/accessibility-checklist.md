# Accessibility Checklist

Run after every phase. Reference: `references/accessibility.md`.

## Automated

Numeric floors derive from [`references/budgets.yaml`](../references/budgets.yaml).

- [ ] axe DevTools / @axe-core/playwright violations at or below `budgets.yaml -> accessibility.axe_violations_critical_max + axe_violations_serious_max` on every page.
- [ ] pa11y errors at or below the same combined threshold on every page.
- [ ] Lighthouse Accessibility meets `lighthouse.mobile.accessibility` (mobile) and `lighthouse.desktop.accessibility` (desktop).

Command (from project root):

```bash
python <web-claw>/scripts/check-a11y.py https://<preview-url>
```

## Semantic structure

- [ ] One `<h1>` per page.
- [ ] Heading levels do not skip (`h2` → `h4` is a violation).
- [ ] `<html lang="…">` matches the page language.
- [ ] Landmarks present: `<header>`, `<nav>`, `<main>` (id="main"), `<footer>`.
- [ ] Skip-to-content link is the first focusable element.

## Keyboard

- [ ] Tab order matches visual order on every page.
- [ ] Every interactive element is reachable by Tab.
- [ ] Focus indicator is visible on every focusable element (≥ 3:1 contrast).
- [ ] Enter activates links; Space activates buttons.
- [ ] Esc closes modals, drawers, dropdowns.
- [ ] Focus returns to the trigger when a modal/drawer closes.
- [ ] No keyboard trap anywhere on the site.

## Forms

- [ ] Every input has a visible label (or `aria-label` if visually labelled by adjacent text).
- [ ] Required fields marked (visible `*` and `aria-required="true"`).
- [ ] Errors announced via `role="alert"` or `aria-live="polite"`.
- [ ] Error message references the field (`aria-describedby`).
- [ ] Submit buttons are not disabled before validation; let users submit and show errors.

## Images

- [ ] Decorative images: `alt=""` (present but empty).
- [ ] Content images: meaningful `alt`.
- [ ] Functional images (icon-only buttons): `aria-label` describing action.
- [ ] No `background-image` for content-bearing imagery.

## Color & contrast

- [ ] Body text ≥ 4.5:1 against background.
- [ ] Large text ≥ 3:1.
- [ ] UI components ≥ 3:1.
- [ ] Color is not the sole carrier of information (pair with icon or text).

## Motion

- [ ] `prefers-reduced-motion: reduce` is honored on every animation.
- [ ] Reduced motion REPLACES (not removes) the animation with a quiet alternative.
- [ ] No flashes > 3 per second.
- [ ] Auto-playing video is muted, has controls, is pauseable.
- [ ] Carousels are pauseable.

## Touch targets

- [ ] All tap targets ≥ 44×44 CSS px (mobile).
- [ ] Adjacent tap targets have ≥ 8px gap.

## Screen reader spot-check

(At least Home, on at least one phase.)

- [ ] H1 announces clearly.
- [ ] Primary CTA reads with meaningful label.
- [ ] Section landmarks announce.
- [ ] Form errors announce on submit.
- [ ] Page transitions don't lose announce focus.

Tools:
- macOS: VoiceOver (Cmd+F5).
- Windows: NVDA (free).
- iOS: VoiceOver (Settings > Accessibility).
- Android: TalkBack.

## High contrast / forced colors

- [ ] Site is legible with `forced-colors: active` emulated in Chrome DevTools (Rendering panel).
- [ ] Essential UI (buttons, borders) uses `currentColor` or `forced-colors` overrides.

## Sign-off

- Pass: all items checked.
- Fail: any unchecked item with no documented N/A reason.
