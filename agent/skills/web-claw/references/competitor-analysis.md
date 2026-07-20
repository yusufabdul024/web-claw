# Competitor Analysis — Web Claw v3

Run during `RESEARCH:COMPETITORS`, immediately after inspiration intake. Purpose: understand the field the client competes in, find the positioning gap the site can own, and sharpen the target-audience USPs before any taste decision is made.

Output: `research/competitor-analysis.md`. Findings feed `research/taste-calibration.md` (audience + USPs) and the anti-style lane of `research/moodboard.md` (what not to look like).

---

## 1. Identify Competitors

Three buckets, 2–4 sites each:

| Bucket | Definition | Source |
|---|---|---|
| **Direct** | Sells the same thing to the same audience | Client names them in the brief; verify with the client |
| **Adjacent** | Different offer, same audience and buying moment | Search + client confirmation |
| **Aspirational** | The brand the client wants to be compared to | Client's inspiration list, award galleries, agency portfolios |

Verify the list with the client before auditing (see `references/client-collaboration.md`, loop step "verify findings"). Auditing the wrong competitors wastes the whole phase.

## 2. Audit Each Competitor

For every site, record:

- **Value proposition** — what the hero claims, and whether it passes the 3-second test.
- **Primary action** — what the site pushes the visitor to do, and how hard.
- **Information architecture** — pages, nav depth, content order.
- **Visual language** — color, type, imagery, density, use of whitespace and depth.
- **Motion** — loader, reveals, scroll behavior, micro-interactions; quiet or loud.
- **Strengths** — what genuinely works (be honest; clients respect it).
- **Weaknesses** — where it is generic, slow, confusing, or ugly.
- **Screenshot or URL + date accessed** — evidence, into `sources.json` (`kind: "competitor"`).

## 3. Find the Gap

The deliverable is not the audit — it is the conclusion:

1. **Positioning gap** — what does every competitor say, and what true claim can this client make that none of them do? This pressure-tests the brief's value proposition (brief Q6): if a competitor already owns that sentence, flag it to the client now.
2. **Experience gap** — what does no competitor's *site* do? If every direct competitor is a static template, a premium animated experience is itself differentiation. If all are loud, quiet confidence wins.
3. **Audience USPs** — for the confirmed target audience: which of the client's strengths do competitors fail to serve? Rank the top 3. These become the site's supporting sections.
4. **Anti-style entries** — visual/motion patterns the competitors share that this site must avoid, so the client is never mistaken for them. Feed these into the moodboard's anti-style lane.

## 4. Output Structure (`research/competitor-analysis.md`)

```markdown
# Competitor Analysis — <project>

## Competitor set (verified with client YYYY-MM-DD)
| Name | Bucket | URL | One-line read |

## Audits
### <Competitor name>
Value prop / Primary action / IA / Visual / Motion / Strengths / Weaknesses / Evidence

## Conclusions
### Positioning gap
### Experience gap
### Target-audience USPs (ranked)
### Anti-style (what we must not look like)

## Open questions for the client
```

## 5. Rules

- **Differentiate, don't copy.** Competitor sites are a map of taken territory, not a source of patterns to lift. Copying inspiration is a taste question (see `references/inspiration-research.md`); copying competitors is a positioning failure *and* a legal risk.
- Audit the live site, not the brand's reputation. The analysis is about what a visitor experiences today.
- Aspirational competitors may also appear in the moodboard as inspiration — one site can be evidence in both files, serving different questions.
- Fast mode: build the competitor set from the brief + search, log the unverified list as an assumption in `decisions/`, and flag it in the completion review.
