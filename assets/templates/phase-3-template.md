# Phase 3 — Launch

**Project:** <name>
**Phase:** 3 of 3
**Goal:** Production-ready. All gates green. Deployed to canonical domain.
**Estimated effort:** <hours / days>
**Inputs:** Phase 2 deployed preview + all qa/ checklists
**Output:** Live site at canonical URL + Phase 3 QA report.

---

## Pre-flight

- [ ] Phase 2 sign-off complete.
- [ ] All real content (logos, photography, final copy) available.
- [ ] Canonical domain DNS access available.
- [ ] Analytics provider account ready (Plausible, Fathom, or GA4).
- [ ] Forms backend ready (Resend API key, Formspree account, or API route plan).

---

## Sequential prompts

### Step 1 — Replace placeholders with real content

1.1  Audit every page for `<!-- TODO -->` or `[PLACEHOLDER]` markers.
1.2  Replace logos with real SVGs.
1.3  Replace placeholder images with the real photography / illustrations. Run them through:
     - AVIF conversion (`scripts/extract-tokens.py` does not handle this; use `pnpm dlx sharp-cli` or similar).
     - Responsive resizes (1×, 2× per breakpoint).
1.4  Replace any draft copy with final copy.
1.5  Commit: `chore(content): replace placeholders with real assets`.

---

### Step 2 — SEO finalization

2.1  Verify `<title>` and `<meta name="description">` per page; max 60 chars / 155 chars.
2.2  Generate `app/og/<page>/route.ts` (Next.js) or static og images for every page.
2.3  Add `<meta property="og:*">` and `<meta name="twitter:*">` per page.
2.4  Add JSON-LD structured data (Organization, WebSite at minimum; Product or BlogPosting where applicable).
2.5  Generate `sitemap.xml`:

```ts
// app/sitemap.ts
import { MetadataRoute } from 'next';
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://example.com/', lastModified: new Date(), changeFrequency: 'monthly', priority: 1.0 },
    /* ... */
  ];
}
```

2.6  Generate `robots.txt`:

```ts
// app/robots.ts
import { MetadataRoute } from 'next';
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/' },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

2.7  Verify in production: `https://<domain>/sitemap.xml` resolves; `https://<domain>/robots.txt` resolves.
2.8  Submit sitemap to Google Search Console.
2.9  Commit: `feat(seo): metadata, og images, sitemap, robots`.

---

### Step 3 — Wire forms

3.1  Identify every form in the site (contact, newsletter, lead capture).
3.2  Implement server-side handlers:
     - For contact: `app/api/contact/route.ts` → validate with zod → send via Resend → confirm to user.
     - For newsletter: `app/api/subscribe/route.ts` → validate → POST to provider API.
3.3  Add rate limiting (Upstash Redis + `@upstash/ratelimit`, or Vercel KV).
3.4  Add honeypot field (hidden, must be empty).
3.5  Add a simple captcha if PII or high-value forms (Cloudflare Turnstile is free and lightweight).
3.6  Test each form end-to-end: success path, validation error, server error.
3.7  Commit: `feat(forms): wire endpoints with validation, rate limit, honeypot`.

---

### Step 4 — Analytics

4.1  Choose provider (default: Plausible for privacy-respecting analytics).
4.2  Add the script tag via the framework's analytics integration:

```tsx
// app/layout.tsx (Next.js example)
import Script from 'next/script';
// ...
<Script defer data-domain="example.com" src="https://plausible.io/js/script.js" />
```

4.3  Add custom events for critical CTAs (signup, form submit, video play).
4.4  Verify events fire by checking the provider's live dashboard during a test session.
4.5  Add Vercel Speed Insights for real-user CWV (one-line install).
4.6  Commit: `feat(analytics): Plausible + Speed Insights`.

---

### Step 5 — Security headers

5.1  In `next.config.js` (or equivalent), add:

```js
async headers() {
  return [{
    source: '/(.*)',
    headers: [
      { key: 'X-Content-Type-Options',    value: 'nosniff' },
      { key: 'X-Frame-Options',           value: 'SAMEORIGIN' },
      { key: 'Referrer-Policy',           value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy',        value: 'camera=(), microphone=(), geolocation=(), interest-cohort=()' },
      { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
      { key: 'Content-Security-Policy',   value: "<see below>" },
    ],
  }];
}
```

5.2  Build a CSP. Minimum:

```
default-src 'self';
script-src 'self' 'unsafe-inline' https://plausible.io;
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self' data:;
connect-src 'self' https://plausible.io;
frame-ancestors 'none';
base-uri 'self';
form-action 'self';
```

5.3  If using nonce-based CSP (recommended for stricter setups), set up middleware to inject a nonce per request.

5.4  Verify at https://securityheaders.com — target grade A.

5.5  Commit: `feat(security): production HTTP headers`.

---

### Step 6 — Performance final pass

6.1  Run `python <web-claw>/scripts/audit-perf.py <preview-url>` (mobile, median of 3 runs). The script reads `references/budgets.yaml` and exits non-zero if any `lighthouse.mobile.*` floor or `core_web_vitals.*` is missed.
6.2  Fix any category below its floor in `lighthouse.mobile.*`.
6.3  Re-run with `--device desktop`. Must clear the (higher) floors in `lighthouse.desktop.*`.
6.4  Check CWV in Chrome DevTools > Performance Insights, or via Vercel Speed Insights after first-traffic.
6.5  Inspect bundle: `pnpm dlx @next/bundle-analyzer` or equivalent. Verify no unexpected large dependencies.
6.6  Optimize hero image: AVIF + responsive srcset + `priority`.
6.7  Verify `<link rel="preload" as="image" ...>` on the LCP image.
6.8  Commit any fixes: `perf(<area>): <fix>`.

---

### Step 7 — Accessibility final pass

7.1  Run `pnpm dlx pa11y https://<preview-url>` for every page. Fix violations.
7.2  Run @axe-core/playwright against every route in CI. Add to the pipeline.
7.3  Keyboard test: from URL bar, Tab through every page's golden path. Verify no traps.
7.4  Screen reader test (NVDA / VoiceOver / TalkBack) on the home page minimum.
7.5  Reduced-motion test: enable in OS, click through every page.
7.6  High-contrast test: emulate `forced-colors: active`. Verify essential UI is legible.
7.7  Commit any fixes: `fix(a11y): <fix>`.

---

### Step 8 — Cross-browser + cross-device

8.1  Test on:
     - Chrome desktop (latest)
     - Safari desktop (latest)
     - Firefox desktop (latest)
     - Chrome Android (real device or BrowserStack)
     - Safari iOS (real device or BrowserStack)
8.2  On each: golden path, signature section, form submit, console for errors.
8.3  Fix any browser-specific issues. Webkit's nuance with `backdrop-filter` and View Transitions is the common culprit.
8.4  Commit fixes: `fix(<browser>): <fix>`.

---

### Step 9 — DNS + SSL + canonical URL

9.1  In Vercel (or chosen host), add the canonical domain.
9.2  Update DNS records (A or CNAME) per the host's instructions.
9.3  Verify SSL provisioning (auto-renew enabled).
9.4  Redirect www → apex (or vice versa) consistently. Configure in framework or DNS.
9.5  Verify `https://<domain>` and `https://www.<domain>` both work and redirect correctly.

---

### Step 10 — Production deploy

10.1  Merge the Phase 3 branch into `main`.
10.2  Verify Vercel auto-deploys main to production.
10.3  Smoke test the live site immediately:
     - Home loads.
     - Primary CTA works.
     - Forms submit.
     - Analytics events fire.
     - No console errors.
10.4  Open Chrome DevTools > Network. Verify HTTP/3, gzip/brotli, all assets ≤ budget.

---

### Step 11 — Final QA pass

11.1  Run the full `qa/pre-launch-checklist.md`.
11.2  Run `qa/security-checklist.md`.
11.3  Write the final QA report at `qa/phase-3-report.md`.

---

### Step 12 — Sign-off

12.1  Send the live URL to the user.
12.2  Confirm:
     - [ ] Site is live at the canonical domain.
     - [ ] Lighthouse mobile meets all four floors in `web-claw/references/budgets.yaml -> lighthouse.mobile.*` (and desktop meets `lighthouse.desktop.*`).
     - [ ] axe-core: at or below `budgets.yaml -> accessibility.axe_violations_*_max` on every page.
     - [ ] Forms submit and emails arrive.
     - [ ] Analytics events appear.
     - [ ] Real content live; no placeholders.
12.3  Update `plan.md`: "Phase 3 complete on <date>. SITE IS LIVE."

---

## Post-launch handoff

Provide the user:

- Repo URL.
- Vercel project URL.
- DNS provider note.
- Analytics dashboard URL.
- Forms backend (Resend dashboard, etc.).
- The `plan.md` and three `phase-*.md` files as the operations manual.
- A short "how to make small edits" guide (where copy lives, where to add a new blog post, where to swap a logo).

**Web Claw is complete.** This site is a $10k-grade marketing site by every measurable definition.
