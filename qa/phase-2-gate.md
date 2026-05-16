# Phase 2 QA Gate — Motion and Interaction Check

Run this gate after Phase 2 build, before presenting to user. Fix all ❌ before advancing.

**Goal:** All animations match the spec, perform at 60fps, degrade gracefully for reduced motion, and don't break performance budgets.

---

## 1. Animations vs. spec

- [ ] Every entrance choreography from `animations.md` is implemented (correct delay, duration, easing)
- [ ] Every section reveal fires at the correct scroll trigger point
- [ ] The SIGNATURE section matches `animations.md §signature` exactly — timing, scrubbed frames, captions

---

## 2. Performance with animations

Run: `scripts/audit-perf.py <preview-url>` on mobile preset with animations active. (Script exits 3 if any floor in `references/budgets.yaml -> lighthouse.mobile.*` or `core_web_vitals.*` is missed.)

- [ ] Lighthouse mobile floors met per `budgets.yaml -> lighthouse.mobile.*`
- [ ] Core Web Vitals pass per `budgets.yaml -> core_web_vitals.*` (LCP, CLS, INP)
- [ ] No janky scroll (run `scripts/run-playwright.py <preview-url>` for the smoke E2E + manually inspect Chrome Performance tab for long tasks > 50ms during animation)
- [ ] Bundle budgets met: `scripts/check-bundle.py --dir <frontend-root>` exits 0

---

## 3. Reduced motion

Run: `scripts/check-reduced-motion.py <preview-url>`. The script must exit 0 — it asserts no content disappears under reduced motion and that fewer than 5% of sampled elements still have animation/transition durations > 100ms.

- [ ] `scripts/check-reduced-motion.py` exits 0
- [ ] Every animation has a fallback (not just disabled — replaced with static alternative)
- [ ] Pinned scroll sections unpin and show static stacked content
- [ ] Page is fully readable and navigable with all animations removed
- [ ] Entrance elements are visible immediately (not hidden behind opacity:0 with no fallback)

---

## 4. Micro-interactions

- [ ] Button hover: scale + color shift, ≤ 200ms
- [ ] Link hover: underline draw or color shift
- [ ] Input focus: visible ring, correct color
- [ ] Card hover: elevation shift, ≤ 200ms

---

## 5. Signature section

- [ ] Renders without console errors (verify with `scripts/run-playwright.py <preview-url>`)
- [ ] Works on Chrome desktop, Chrome Android (emulated Pixel 6a), Safari desktop (re-run Playwright with `--browser webkit` to cover Safari)
- [ ] Escape key / high scroll velocity exits the pinned section (if applicable)
- [ ] Mobile version of signature section renders (may be simplified per spec)

---

## 6. Visual critique pass

Run the `qa/visual-critique-rubric.md` rubric against the deployed preview. Write result to `qa/visual-critique-phase-2.md`.

- [ ] Median score across all 10 axes ≥ 4
- [ ] No axis below 3
- [ ] Notes captured for any axis at 3 (improvement direction for Phase 3)

---

## 7. Smooth scroll (if Lenis is in stack)

- [ ] Lenis is active on desktop
- [ ] Lenis is disabled when `prefers-reduced-motion: reduce` (native scroll takes over)
- [ ] No rubber-band conflict on Safari

---

## Gate-by-script summary

| Script | Must exit | Covers |
|--------|-----------|--------|
| `scripts/audit-perf.py <preview>` | 0 | Sections 2 (Lighthouse + CWV) |
| `scripts/check-reduced-motion.py <preview>` | 0 | Section 3 |
| `scripts/run-playwright.py <preview>` | 0 | Sections 5 (smoke), partial 2 |
| `scripts/check-bundle.py --dir <frontend>` | 0 | Section 2 (bundle) |

---

## Gate Result

If all items pass: advance to EXECUTION:PHASE-3. Update `memory.md`.

If any item fails: hand to Implementer Agent with this report. Fix all ❌. Re-run gate.

Write result to `qa/phase-2-report.md`.
