# CI workflow templates for consumer projects

These workflows are **not** Web Claw's own repo CI. They are templates that ship with the skill so a consumer project (the website you build with Web Claw) can drop them straight into its own `.github/workflows/` directory.

## Files

| File             | Purpose                                                          |
|------------------|------------------------------------------------------------------|
| `lighthouse.yml` | Runs `scripts/audit-perf.py` against a deploy preview on every PR. Gates against `references/budgets.yaml -> lighthouse.*`. |
| `playwright.yml` | Runs the Playwright E2E smoke (`scripts/run-playwright.py`), `scripts/check-a11y.py`, and `scripts/check-reduced-motion.py` against a deploy preview. |

## How to use

In a project that has Web Claw installed (so `web-claw/scripts/*` exist at the skill's host-native path):

```bash
mkdir -p .github/workflows
cp <web-claw-skill-root>/assets/ci-templates/lighthouse.yml .github/workflows/
cp <web-claw-skill-root>/assets/ci-templates/playwright.yml .github/workflows/
```

Set a repository secret named `PREVIEW_URL` (or use the workflow's `workflow_dispatch.inputs.url`). Without that secret, the workflows no-op rather than fail.

## Why they don't live in Web Claw's own `.github/workflows/`

If they did, GitHub Actions would run them on every Web Claw skill repo PR, where they would either fail (no preview URL) or noisily no-op. The skill repo runs its own validation CI under `.github/workflows/build.yml` instead.
