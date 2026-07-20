# Moodboard Library - Web Claw v3

## Purpose

This library gives the Researcher and Designer Agents a structured way to turn scattered inspiration into a coherent taste direction.

A moodboard is not a collage. It is a set of decisions with evidence.

## Moodboard Axes

Every moodboard should cover these axes:

1. Visual mood
2. Color/material
3. Typography
4. Layout/composition
5. Imagery/assets
6. Motion/interaction
7. Copy voice
8. Anti-style

## Direction Template

Each candidate direction in `research/moodboard.md` should use this shape:

```markdown
## Direction A - <Name>

**Three adjectives:** <adjective>, <adjective>, <adjective>
**Best for:** <audience/outcome fit>
**Confidence:** <high | medium | low>
**Build cost:** <low | medium | high>

### Evidence
- <Source title>: borrow <idea>; avoid <thing>.
- <Source title>: borrow <idea>; avoid <thing>.

### Visual System
- Color/material:
- Typography:
- Layout/composition:
- Imagery/assets:
- Motion/interaction:
- Copy voice:

### Signature Candidate
<One section or interaction this direction would make memorable.>

### Anti-Style
- We will not...
- We will not...

### Risks
- <risk + mitigation>
```

## Common Direction Families

Use these as naming seeds, not templates:

| Family | Signals | Good for | Watch out |
|--------|---------|----------|-----------|
| Editorial Precision | Large type, restraint, grid breaks, sharp copy | studios, consultants, premium services | Can feel cold or underbuilt. |
| Product Cinema | Hero media, scroll sequence, tactile product reveals | launches, SaaS, hardware, apps | Can get heavy fast. |
| Warm Systems | human color, rounded forms, approachable copy | wellness, education, community, nonprofits | Can become beige/generic. |
| Brutalist Utility | dense grids, mono/grotesk type, hard edges | developer tools, experimental brands | Can harm readability/trust. |
| Quiet Luxury | low saturation, premium type, material detail | fashion, architecture, high-ticket services | Can become empty if proof is weak. |
| Playful Mechanics | responsive micro-interactions, cursor/touch delight | creative tools, portfolios, youth brands | Can become gimmicky. |
| Technical Clarity | diagrams, code surfaces, sparse motion | dev tools, B2B technical products | Can become template-SaaS. |
| Cultural Collage | mixed media, social-native pacing, editorial cards | music, art, events, creator brands | Needs tight anti-style or it sprawls. |

## How To Decide Between Directions

Prefer the direction that:

1. best fits the user's business goal,
2. best matches the audience's expectations and sophistication,
3. has the strongest source evidence,
4. can be built within budget,
5. gives the page one clear signature device.

Do not average directions. If combining, write a governing rule:

> "Use Direction A for typography and layout, Direction B only for motion restraint."

## Moodboard Anti-Patterns

- A direction with no anti-style.
- A direction made only from one source.
- A direction that cannot be built within performance/accessibility budgets.
- A moodboard that says "modern, clean, premium" without concrete evidence.
- Three directions that differ only by color.
- Copying a competitor's visual language.

## User Presentation

When presenting the moodboard, ask:

> "Which direction feels most like the site you would be proud to share: A, B, or a blend? What must not change?"

Then write the answer into `research/taste-calibration.md`.
