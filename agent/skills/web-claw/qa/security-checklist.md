# Security Checklist

Run before production deploy (Phase 3). The site does not collect data by default, but every published site has a security posture worth setting deliberately.

## HTTP security headers

Verify at https://securityheaders.com — target grade **A** or **A+**.

- [ ] `Content-Security-Policy` set. Minimum:
      ```
      default-src 'self';
      script-src 'self' 'unsafe-inline' <analytics-origin>;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
      connect-src 'self' <analytics-origin>;
      frame-ancestors 'none';
      base-uri 'self';
      form-action 'self';
      ```
- [ ] `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`.
- [ ] `X-Content-Type-Options: nosniff`.
- [ ] `X-Frame-Options: SAMEORIGIN` (or replaced by `frame-ancestors` in CSP).
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`.
- [ ] `Permissions-Policy` denies camera, microphone, geolocation, interest-cohort by default.

## Transport

- [ ] HTTPS only (no HTTP access).
- [ ] HTTP → HTTPS redirect at the host level.
- [ ] HSTS enabled.
- [ ] No mixed-content warnings in browser console.
- [ ] SSL/TLS configuration: A+ at https://www.ssllabs.com/ssltest/.

## Secrets and bundles

- [ ] No `.env` files committed.
- [ ] No API keys in the client bundle. Grep the deployed JS for known key prefixes (`sk_`, `pk_`, `AIza`, etc.).
- [ ] Environment variables: only `NEXT_PUBLIC_*` (Next.js) or `PUBLIC_*` (Astro) keys exposed to the client.
- [ ] No internal endpoints leaked in client bundle (`/api/admin/*` etc.).

## Form security

For each form:

- [ ] Server-side validation (do not trust the client).
- [ ] Rate limiting on the endpoint.
- [ ] Honeypot field (hidden input that must be empty).
- [ ] Captcha (Cloudflare Turnstile or hCaptcha) on high-value forms.
- [ ] Email confirmation for sign-ups, where applicable.
- [ ] CSRF protection for any state-changing endpoint (most form endpoints qualify).

## Third-party scripts

- [ ] All `<script src>` from external origins use `crossorigin="anonymous"` (so the browser does not leak credentials).
- [ ] All `<link rel="stylesheet">` and `<script>` from external origins have `integrity="sha384-…"` where the version is pinned.
- [ ] No script tags from origins not in the CSP.

## Cookies (if any)

- [ ] All cookies set `Secure`, `HttpOnly` (if not client-readable), `SameSite=Strict` or `Lax`.
- [ ] Cookie consent banner if visitors are from the EU/UK and the site uses cookies that aren't strictly necessary.

## Privacy

- [ ] Privacy policy linked from the footer.
- [ ] Terms of service linked from the footer (if applicable).
- [ ] Cookie banner only if cookies are actually used.
- [ ] Analytics provider is privacy-respecting (Plausible / Fathom) OR a consent banner gates GA.
- [ ] No third-party tracking pixels added by accident.

## Dependencies

- [ ] `pnpm audit` (or `npm audit`) shows no high/critical vulnerabilities.
- [ ] Dependabot / Renovate configured for the repo.

## Deployment

- [ ] Deploy account uses 2FA.
- [ ] Domain registrar uses 2FA.
- [ ] DNS provider uses 2FA.
- [ ] Database / forms backend access keys rotated since project start.

## Sign-off

- Pass: every applicable item checked.
- Fail: any unaddressed item without a documented N/A reason.
