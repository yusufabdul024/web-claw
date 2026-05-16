# Pre-Launch Checklist

The final gate before the site goes live at the canonical domain. Run after Phase 3 build is complete and all per-checklist gates have passed.

This is the master checklist. It composes the others.

## 1. Content

- [ ] All copy is final. No `<!-- TODO -->` or `[PLACEHOLDER]` markers.
- [ ] All logos are real (no placeholder wordmarks).
- [ ] All images are final, optimized, responsive.
- [ ] All video and audio is final.
- [ ] All form fields, labels, and error messages are reviewed for tone + copy.
- [ ] All legal pages exist: Privacy Policy, Terms of Service, Cookie Policy (if needed).

## 2. SEO

- [ ] Every page has `<title>` and `<meta name="description">`.
- [ ] Every page has unique og:image (or one canonical og:image acceptable).
- [ ] `sitemap.xml` generated and live at `/sitemap.xml`.
- [ ] `robots.txt` generated and live at `/robots.txt`.
- [ ] Structured data (JSON-LD) for Organization + WebSite at minimum.
- [ ] Search Console verified.
- [ ] Sitemap submitted to Search Console.

## 3. Analytics

- [ ] Analytics provider script installed.
- [ ] Custom events for critical CTAs configured.
- [ ] Live dashboard receiving test events.
- [ ] Speed Insights / Real-User Monitoring enabled.
- [ ] Cookie consent (if applicable) gates analytics correctly.

## 4. Forms

- [ ] Every form has a tested submission path.
- [ ] Email arrives at the configured destination.
- [ ] Validation errors render correctly.
- [ ] Rate limiting active.
- [ ] Honeypot in place.

## 5. Security (compose `security-checklist.md`)

- [ ] Pass `qa/security-checklist.md`.
- [ ] Score ≥ A on https://securityheaders.com.
- [ ] Score ≥ A on https://www.ssllabs.com.

## 6. Accessibility (compose `accessibility-checklist.md`)

- [ ] Pass `qa/accessibility-checklist.md`.
- [ ] `scripts/check-a11y.py <url>` exits 0 every page.
- [ ] `scripts/check-contrast.py --style-guide blueprint/style-guide.md` exits 0.
- [ ] Keyboard golden path tested.
- [ ] Screen reader spot-check passed (home minimum).

## 7. Performance (compose `performance-checklist.md`)

- [ ] Pass `qa/performance-checklist.md`.
- [ ] `scripts/audit-perf.py <url>` exits 0 (gates against `budgets.yaml -> lighthouse.mobile.*` and `core_web_vitals.*`).
- [ ] `scripts/check-bundle.py --dir <frontend-root>` exits 0 (gates against `budgets.yaml -> bundle.*`).

## 8. Cross-browser (compose `cross-browser-checklist.md`)

- [ ] Pass `qa/cross-browser-checklist.md`.

## 9. Responsive (compose `responsive-checklist.md`)

- [ ] Pass `qa/responsive-checklist.md`.

## 10. Motion (compose `motion-checklist.md`)

- [ ] Pass `qa/motion-checklist.md`.
- [ ] `scripts/check-reduced-motion.py <url>` exits 0.
- [ ] Every animation has reduced-motion alternative verified.

## 10a. Visual quality (compose `visual-critique-rubric.md`)

- [ ] `qa/visual-critique-rubric.md` scored: median ≥ 4, minimum ≥ 3.
- [ ] `scripts/visual-regression.py <url> --project <project>` exits 0 (or diffs reviewed).

## 11. Domain + deploy

- [ ] DNS A / CNAME records pointing to host.
- [ ] SSL certificate valid and auto-renewing.
- [ ] www → apex (or apex → www) redirect set and consistent.
- [ ] Production deploy is on the `main` branch's latest commit.
- [ ] Preview URL and production URL both work.

## 12. Monitoring

- [ ] Uptime monitor configured (UptimeRobot, Better Stack, or host's built-in).
- [ ] Error reporting (Sentry, host's logs) configured for forms / API routes.
- [ ] Build alerts: failed deploys notify the team.

## 13. Documentation

- [ ] Repo `README.md` explains: stack, how to run, how to deploy, where copy lives.
- [ ] `plan.md` and `phase-*.md` files committed to the repo.
- [ ] Onboarding note for the user: how to swap a logo, how to add a blog post, who to contact for an issue.
- [ ] Handoff bundle produced via `scripts/export-handoff.py --workspace <project> --shape tarball` (or json/markdown) if the project transfers to another team.

## 14. Backups + recovery

- [ ] Repo is on GitHub (or another remote) — not just local.
- [ ] Vercel (or chosen host) auto-rollback works (verify by deploying and rolling back).
- [ ] Forms backend (Resend / Formspree) stores submission history.

## 15. Launch communications

- [ ] User has the live URL.
- [ ] User knows how to access the analytics dashboard.
- [ ] User knows where to report bugs.
- [ ] User has the Vercel / host login (or someone they trust does).

## 16. Final smoke test on the live site

After production deploy is live at the canonical domain:

- [ ] Home loads (https://<domain>/).
- [ ] All nav links work.
- [ ] All footer links work.
- [ ] Forms submit on the live URL.
- [ ] No console errors on any page.
- [ ] No 404s in network panel.
- [ ] Analytics shows live traffic.
- [ ] DNS propagation verified globally (use dnschecker.org).

---

## Sign-off

- **Date:** <YYYY-MM-DD>
- **Live URL:** <https://...>
- **All sections passed:** [ ] Yes / [ ] No (if no, list which)
- **User confirmed launch:** [ ] Yes
- **Web Claw engagement complete:** [ ] Yes

This is a $10k-grade website.
