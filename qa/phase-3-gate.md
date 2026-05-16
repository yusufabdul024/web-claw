# Phase 3 QA Gate — Launch Readiness Check

Run this gate after Phase 3 build. This is the final gate before declaring the site done. Fix all ❌.

**Goal:** The site is production-ready. Lighthouse budgets hit. Accessibility clean. No placeholder content. Forms live. SEO correct.

---

## 1. Performance (run `scripts/audit-perf.py` — mobile, median of 3 runs)

Numeric thresholds derive from [`references/budgets.yaml`](../references/budgets.yaml). The script returns non-zero if any floor is missed.

- [ ] Lighthouse mobile Performance meets `lighthouse.mobile.performance`.
- [ ] Lighthouse mobile Accessibility meets `lighthouse.mobile.accessibility`.
- [ ] Lighthouse mobile Best Practices meets `lighthouse.mobile.best_practices`.
- [ ] Lighthouse mobile SEO meets `lighthouse.mobile.seo`.
- [ ] CWV pass per `core_web_vitals.*` (LCP, CLS, INP).

---

## 2. Accessibility (run `scripts/check-a11y.py` — paste output)

- [ ] Zero axe-core critical and serious violations
- [ ] Skip-to-content link exists and works
- [ ] All form fields have visible labels (not just placeholder text)
- [ ] Color contrast passes at all font sizes actually used
- [ ] All modals trap focus correctly and close on Escape
- [ ] Page works completely with JavaScript disabled (content visible, links work)

For full detail: load `qa/accessibility-checklist.md`.

---

## 3. Content

- [ ] Zero lorem ipsum on any page
- [ ] All placeholder images replaced with real or intentional generated assets
- [ ] All copy has been reviewed and is final
- [ ] All page titles are unique and descriptive
- [ ] All meta descriptions are written (not auto-generated from H1)

---

## 4. SEO

- [ ] `sitemap.xml` exists and is correct
- [ ] `robots.txt` exists
- [ ] All pages have unique `og:title`, `og:description`, `og:image` (run `scripts/generate-og.py --project <project>` if missing — produces `assets/og/*.png` from style-guide tokens)
- [ ] Canonical URLs set on all pages
- [ ] Structured data (JSON-LD) on home page minimum

---

## 5. Forms and integrations

- [ ] All form submissions deliver to the correct endpoint (test each)
- [ ] Form success and error states display correctly
- [ ] No exposed API keys in client bundle (grep: `grep -r "sk-" dist/` or equivalent)
- [ ] Rate limiting or CAPTCHA on forms collecting PII

---

## 6. Security basics

- [ ] CSP header in place
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] All external `<script>` tags have `integrity` attribute

For full detail: load `qa/security-checklist.md`.

---

## 7. Cross-browser (automated smoke — 3 desktop browsers; manual on mobile)

Run `scripts/run-playwright.py <production-url>` for each browser. Each invocation must exit 0.

- [ ] Chromium pass: `scripts/run-playwright.py <url> --browser chromium`
- [ ] Firefox pass: `scripts/run-playwright.py <url> --browser firefox`
- [ ] Webkit (Safari engine) pass: `scripts/run-playwright.py <url> --browser webkit`
- [ ] Chrome Android (real device or BrowserStack) — manual pass
- [ ] Safari iOS (real device or BrowserStack) — manual pass

---

## 8. Analytics and production

- [ ] Analytics wired (if discovery.md specified one)
- [ ] Production domain configured and pointing to deploy
- [ ] SSL certificate active

---

## 9. Visual regression baseline

If a baseline exists in `qa/snapshots/`, run `scripts/visual-regression.py <url> --project <project>`. Any diff above the 0.5% threshold must be reviewed.

- [ ] `scripts/visual-regression.py` exits 0 (or all diffs are explicitly approved)
- [ ] If this is the first launch, run with `--update-baseline` to seed `qa/snapshots/`

---

## 10. Visual critique pass

Run the rubric in `qa/visual-critique-rubric.md`. Write result to `qa/visual-critique-phase-3.md`.

- [ ] Median score across all 10 axes ≥ 4
- [ ] No axis below 3

---

## Gate-by-script summary

| Script | Must exit | Covers |
|--------|-----------|--------|
| `scripts/audit-perf.py <url>` | 0 | Section 1 |
| `scripts/check-a11y.py <url>` | 0 | Section 2 |
| `scripts/run-playwright.py <url> --browser {chromium\|firefox\|webkit}` | 0 each | Section 7 |
| `scripts/visual-regression.py <url> --project <project>` | 0 | Section 9 |
| `scripts/generate-og.py --project <project>` | 0 | Section 4 (OG images) |
| `scripts/check-bundle.py --dir <frontend>` | 0 | Section 5 (no exposed bundles oversized) |

---

## Gate Result

If all items pass: advance to QA:FINAL. Update `memory.md → Phase: QA:FINAL`. (Phase = DONE is set only when QA:FINAL itself exits — see `references/state-machine.md`.)

If any item fails: hand to Implementer Agent with this report. Fix all ❌. Re-run only the failed checks.

Write result to `qa/phase-3-report.md`.
