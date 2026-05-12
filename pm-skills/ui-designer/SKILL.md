---
name: ui-designer
description: >
  Generate UI/UX design specifications, mid-fidelity ASCII wireframe prototypes, user flows,
  component descriptions, and interaction states from a PRD, feature brief, or rough idea.
  Use this skill when the user asks for design specs, wireframes, wants to think through a
  user flow, needs component definitions, or wants to produce a design brief for a designer
  or design system. Also trigger when the user says things like "help me design this",
  "wireframe this screen", "what should this screen look like", "sketch out the UI",
  "spec out the UX", or "write up the design requirements". Produces structured design
  documentation and ASCII wireframe prototypes that can drive Figma work or design system
  decisions — no image files needed.
---

# UI Designer Skill

Generate structured design specifications, user flows, and component documentation from product requirements.

## When to Use
- User has a PRD or feature brief and needs design specs to hand to a designer
- User wants to think through a user flow before opening Figma
- User needs component descriptions (states, interactions, edge cases) documented
- User wants to identify UX risks or accessibility requirements early
- User wants a wireframe narrative — a text description of what each screen contains

## Output Structure

### For a full design spec, produce:

**0. Mid-Fidelity Wireframe Prototype**
For each screen in the flow, produce an ASCII wireframe using box-drawing characters.
Wireframes communicate layout zones, component placement, hierarchy, and relative sizing.
They are mid-fidelity: more structured than a sketch, less detailed than a high-fidelity mockup.

Format rules:
- Use `┌─┐ │ └─┘ ├─┤` for containers and panels
- Use `[ Button Label ]` for buttons and CTAs
- Use `( ○ )` / `(●)` for radio buttons, `[ ]` / `[x]` for checkboxes
- Use `▸ Item` for list rows, `▼ / ▶` for dropdowns/disclosure
- Annotate zones with ALL CAPS labels: `NAVBAR`, `HERO`, `SIDEBAR`, `CARD`, `MODAL`
- Add a numbered annotation key below each wireframe for anything needing explanation

Example format:
```
Screen: [Name] — [375px mobile / 1280px desktop]
┌────────────────────────────────────┐
│ NAVBAR                   [≡ Menu] │
├────────────────────────────────────┤
│                                    │
│  Headline text ①                  │
│  Subheadline copy here             │
│                                    │
│  ┌──────────────────────────────┐  │
│  │ INPUT AREA                   │  │
│  │ Placeholder text…            │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  [ Primary CTA        ] ②         │
│                                    │
│  RECENT ITEMS                      │
│  ┌──────────────────────────────┐  │
│  │ ▸ Item title                 │  │
│  ├──────────────────────────────┤  │
│  │ ▸ Item title                 │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
① Streams in after submit — show loading skeleton first
② Disabled until input ≥ 10 chars
```

**1. Design Brief**
- Feature summary (1 paragraph)
- Target user and job to be done
- Design principles for this feature (2–3 specific, not generic)
- Constraints (platform, existing design system, accessibility requirements)

**2. User Flows**
For each distinct flow, produce a numbered step sequence:
```
Flow: [Name — e.g., "First-time setup"]
Actor: [User type]

1. User lands on [screen] — sees [what]
2. User [action] → system [response]
3. ...
N. User reaches [end state]

Error states:
- If [condition]: show [message/state]
- If [condition]: redirect to [screen]
```

**3. Screen Specifications**
For each screen in the flow:
```
Screen: [Name]
Route/URL: [path if applicable]

Layout:
  - [Zone]: [what it contains, in priority order]

Components:
  - [Component name]: [description, states: default / hover / active / disabled / error / empty]

Copy:
  - Headline: "[text]"
  - CTA: "[text]"
  - Empty state: "[text]"
  - Error: "[text]"

Behavior:
  - On [action]: [what happens]
  - On [event]: [system response]
```

**4. Component Inventory**
List every new or modified component:
| Component | Type | States | Notes |
|-----------|------|--------|-------|
| [name] | New / Modified / Existing | default, hover, ... | [design system ref or constraint] |

**5. Accessibility Requirements**
- Keyboard navigation path
- Screen reader labels for non-obvious elements
- Color contrast requirements for any new color usage
- Focus state requirements

**6. Design Open Questions**
- Numbered list of unresolved UX decisions that need designer input or user research

---

## Output Guidelines

- **Never produce image files** — only text-based design documentation
- **Be specific about states** — every interactive component has at minimum: default, hover, active, disabled, and error states
- **Name components** using the product's design system vocabulary if one is described
- **Flag copy gaps** — if a screen needs microcopy that isn't provided, write a placeholder and mark it `[COPY NEEDED]`
- **Surface UX risks** — if a flow has a known friction point (too many steps, ambiguous action), call it out explicitly
- **One flow per output** if the feature has multiple distinct flows — don't collapse them

## Quick Mode

If the user wants a fast sketch, produce:
1. A 5-step user flow for the happy path
2. Three screen descriptions (entry, key action, success/end state)
3. Top 3 UX risks

## Integration Points

- Start with the **prd** skill to define requirements before designing
- Hand off to the **agile-stories** skill to turn screen specs into acceptance criteria
- Use the **experiment-design** skill to plan usability tests for high-risk flows
- Use the **kano-model** framework to decide which interactions to invest in vs. keep minimal
