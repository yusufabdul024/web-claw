# Tech Stack Matrix

How the Implementer Agent picks a stack. The matrix is opinionated by purpose — pick the row that matches the project, not the framework that's trending.

## The decision axes

1. **Content shape** — is this a marketing site (low routing, low state), a content site (many pages, structured content), or an app-marketing hybrid?
2. **Motion intensity** — restrained / active / maximalist (from `discovery.md`).
3. **Deploy target** — Vercel, Cloudflare Pages, Netlify, static export, self-hosted.
4. **CMS** — none, MDX files, headless (Sanity / Contentful / Hygraph / Storyblok), or a backend product like Notion-as-CMS.
5. **Team competence** — React-first vs HTML-first vs Svelte-first.

## The matrix

| Content shape         | Motion intensity | Recommended framework                      |
|-----------------------|------------------|-------------------------------------------|
| Single landing page   | Restrained       | Astro + Tailwind (or vanilla HTML + Vite) |
| Single landing page   | Active           | Next.js (App Router) + Tailwind            |
| Single landing page   | Maximalist       | Vite + Vanilla TS (max control) OR Next.js |
| Marketing site (5–10) | Restrained       | Astro + Tailwind                           |
| Marketing site (5–10) | Active           | Next.js (App Router) + Tailwind            |
| Marketing site (5–10) | Maximalist       | Next.js (App Router) + RTF if 3D needed    |
| Content-heavy / blog  | Any              | Astro + Tailwind + MDX                     |
| Portfolio             | Active+          | Next.js + Framer Motion or GSAP            |
| Brand / agency site   | Maximalist       | Next.js + GSAP + R3F                       |
| SaaS marketing        | Active           | Next.js (App Router) + Tailwind            |

## Why these picks

### Astro
- Best static perf — ships zero JS by default. JS is opt-in per island.
- MDX as first-class. Content collections type-safe.
- Pairs well with low/medium-motion projects where JS is not the design.
- Pairs poorly with maximalist motion across pages — the islands model adds complexity.

### Next.js (App Router)
- The default React full-stack framework.
- Built-in image optimization (`next/image`), font optimization (`next/font`), font preload, route prefetch.
- App Router server components reduce client JS substantially.
- Pairs well with active and maximalist motion (libraries integrate cleanly).
- Slight runtime overhead vs Astro; offset by RSC streaming.

### SvelteKit
- Smallest runtime among React-like frameworks.
- Excellent DX. Less plug-and-play motion ecosystem than React.
- Recommend only if the team is Svelte-fluent.

### Vite + Vanilla
- Maximum control, minimum dependencies.
- Right for single-page maximalist sites where every JS byte is hand-curated.

## Recommended dependency clusters

### Cluster A — Astro Marketing
```
astro
@astrojs/tailwind
@astrojs/mdx
@astrojs/sitemap
@astrojs/image (or astro:assets in v3+)
tailwindcss
```

### Cluster B — Next.js Marketing (Active motion)
```
next
react
react-dom
tailwindcss
framer-motion       (or gsap)
lenis
lucide-react
clsx
```

### Cluster C — Next.js Marketing (Maximalist motion)
```
next
react
react-dom
tailwindcss
gsap
lenis
framer-motion       # for micro-interactions; gsap for big choreography
@react-three/fiber
@react-three/drei
three
lucide-react
clsx
```

### Cluster D — Vite + Vanilla Maximalist
```
vite
typescript
gsap
lenis
three  (optional)
```

### Cluster E — Astro + MDX content site
```
astro
@astrojs/tailwind
@astrojs/mdx
@astrojs/sitemap
@astrojs/rss
shiki     # syntax highlighting
remark-gfm
```

## Auxiliary packages (almost always)

- `@axe-core/playwright` or `@axe-core/cli` — a11y testing.
- `@playwright/test` — visual + smoke testing.
- TypeScript strict mode.
- ESLint with the framework's recommended config.
- Prettier with `prettier-plugin-tailwindcss` if Tailwind.
- `zod` if forms are non-trivial.

## Auxiliary packages (sometimes)

- `@vercel/analytics` — first-party perf data on Vercel.
- `plausible-tracker` or `@fathom/client` — privacy-respecting analytics.
- `resend` + `react-email` — transactional email if the site has forms.
- `posthog-js` — product analytics (overkill for pure marketing).
- `@sanity/client` + `@portabletext/react` — Sanity headless CMS.
- `@contentful/rich-text-react-renderer` — Contentful.

## CMS picks

| CMS                      | When to use                                                                   |
|--------------------------|-------------------------------------------------------------------------------|
| MDX files in `content/`  | Default. Author copy is technical. Up to ~100 pages. Free.                    |
| Sanity                   | Non-technical authors, structured content, real-time preview.                 |
| Storyblok                | Visual editor priority, marketing teams.                                      |
| Hygraph                  | API-first, GraphQL preference.                                                |
| Contentful               | Enterprise; legacy reason; team already on it.                                |
| Payload                  | Self-host preference, TS-first, headless + admin in one.                      |
| Notion + Notion API      | Tiny team, content lives in Notion already. Has limits — not for blog at scale. |

## Pinning versions

Always pin to a caret-major range in `package.json`:

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "gsap": "^3.12.5",
    "lenis": "^1.1.0",
    "framer-motion": "^11.5.0"
  }
}
```

Use `pnpm` as the package manager when possible — fastest, disk-efficient, lockfile is the most readable of the major three.

## Deploy targets

### Vercel
- Pairs natively with Next.js (best-case scenario: zero-config).
- Preview URLs per PR.
- Free tier is generous for marketing sites.
- Image optimization included.
- For Astro: also supported, set `output: 'server'` and add the Vercel adapter if you need SSR; static export works zero-config.

### Cloudflare Pages
- Cheaper for high traffic.
- Pairs with Astro (static, fastest), Next.js (with adapter), SvelteKit (with adapter).
- Workers integration if you need edge functions.

### Netlify
- Pairs with everything. Slightly slower than Vercel/Cloudflare for previews.

### Static export
- For sites with no server-side needs. Build once, deploy to any static host or S3.

## Form / submission targets

When the site has a contact form:

- **Resend** — modern, dev-friendly, `react-email` for templates.
- **Formspree** — no backend, drop-in.
- **Web3Forms / Formspark** — free tiers, JSON POST.
- **Custom API route** (Next.js / Astro server endpoint) — when you want to validate, log, and forward.

Always:
- Server-side validate.
- Rate-limit.
- Honeypot field for bot filtering.
- Real captcha if PII or high-value forms.

## Quick decision example (worked)

**Brief:** B2B SaaS marketing site, 7 pages, "active" motion intensity, Vercel deploy, team is React-fluent, no CMS today.

**Decision:**
- Framework: **Next.js 15 (App Router)** — content shape and motion intensity fit; team is React.
- Styling: **Tailwind 4**.
- Motion: **Framer Motion** for components, **Lenis** for smooth scroll, no GSAP (the motion spec doesn't require pinned scroll or timeline orchestration).
- Content: **MDX files** under `content/` — no CMS yet; can swap later.
- Deploy: **Vercel**.
- Forms: **Resend** + `react-email`.
- A11y: **@axe-core/playwright** in CI.

Total install:
```bash
pnpm create next-app@latest <project> --typescript --tailwind --app
cd <project>
pnpm add framer-motion@^11 lenis@^1.1 lucide-react clsx zod resend react-email
pnpm add -D @axe-core/playwright @playwright/test prettier-plugin-tailwindcss
```

That's the entire dependency set for the project. ~10 prod packages, no surprises.
