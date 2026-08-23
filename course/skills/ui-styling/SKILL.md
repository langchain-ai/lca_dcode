---
name: ui-styling
description: Apply the Ledger design system to any user interface in the app —
  restyling pages, building new pages, tables, forms, buttons, badges, empty
  states, or status indicators. Contains the complete visual specification:
  colour tokens, typography, spacing, component specs, and accessibility rules.
  Use for any task that changes something a person looks at, including the
  final step of a mostly-backend feature. Not for pure API or data-layer work.
---

# The Ledger design system

Ledger is a personal expense tracker. It should read like a well-set financial
newspaper: an editorial serif for headings, a clean grotesque for interface
text, and monospaced tabular figures for every number on the page. Dense, calm,
paper-like. Colour is used sparingly and always means something.

This document is the complete specification. Implement it exactly — the token
values below are the source of truth, not the current contents of
`src/ledger/static/app.css`.

**No build step, no framework, no CDN except the font stylesheet.** One
handwritten CSS file, plain Jinja templates.

---

## 1. Typography

### Families

Load from Google Fonts. Add this to `<head>` in `base.html`, before the
stylesheet link:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
--font-display: "Newsreader", Georgia, "Times New Roman", serif;
--font-ui: "Public Sans", ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif;
--font-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
```

The fallbacks matter — if the network is unavailable the app must still look
deliberate. Test with the font link removed.

### Assignment

| Element | Family | Notes |
| --- | --- | --- |
| `h1`, `h2`, `h3` | `--font-display` | Weight 400. The serif carries the character; don't bold it. |
| Body text, labels, buttons, nav | `--font-ui` | |
| Every number: amounts, dates, counts, percentages | `--font-mono` | Always with `font-variant-numeric: tabular-nums` |
| Code, file paths | `--font-mono` | |

### Scale

```css
--text-micro: 0.6875rem;  /* uppercase labels, table headers */
--text-small: 0.8125rem;  /* hints, secondary lines, footer */
--text-body:  0.9375rem;  /* default */
--text-lede:  1.0625rem;  /* intro paragraphs */
--text-h2:    1.25rem;
--text-h1:    1.75rem;
--text-figure: 2.25rem;   /* dashboard stat values */
```

Body line-height `1.55`. Headings `1.2`. Figures `1.1`.

### The micro-label

Table headers, form labels, and stat labels all share one treatment. It is the
app's signature — use it for any new label:

```css
font: 500 var(--text-micro)/1.3 var(--font-ui);
text-transform: uppercase;
letter-spacing: 0.08em;
color: var(--ink-soft);
```

Headings and buttons are sentence case, never Title Case.

---

## 2. Colour

```css
/* Neutrals */
--surface:    #F6F7F5;  /* page background */
--raised:     #FFFFFF;  /* cards, table background */
--ink:        #14191C;  /* primary text, headings */
--ink-mid:    #545F68;  /* secondary text */
--ink-soft:   #838F99;  /* labels, placeholders, disabled */
--rule:       #E3E7E4;  /* hairline borders */
--rule-firm:  #C7CFCA;  /* emphasis borders, table header underline */

/* Brand */
--brand:      #14503C;  /* primary actions, links, active nav */
--brand-deep: #0D3628;  /* hover and pressed states */
--wash:       #EBF1EE;  /* selected rows, tinted panels */

/* Semantic */
--credit:     #14503C;  /* money in */
--debit:      #9E2B25;  /* money out */
--warn:       #8A5B00;  /* over budget, needs attention */
--warn-wash:  #FBF2E3;  /* background behind a warning */
```

### Rules

- **Never write a raw colour value** in a template or a new rule. Every colour
  comes from a token. If you need one that doesn't exist, stop and say so
  rather than inventing it.
- `--brand` and `--credit` are deliberately the same value. Money arriving is
  the product's happy path, so the brand colour *is* the positive colour. This
  is intentional; don't "fix" it by splitting them.
- `--debit` is for negative amounts only. It is not a general error or danger
  colour, and it is not for delete buttons.
- `--warn` is for states that need attention but aren't wrong — an over-budget
  category, a row that will be skipped on import.
- Three greys, and only three. Don't add a fourth.
- No gradients. No colour that isn't in this table.

---

## 3. Space, borders, elevation

```css
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-5: 1.5rem;
--space-6: 2rem;
--space-7: 3rem;
--space-8: 4rem;

--radius-control: 3px;
--radius-card: 6px;
--radius-pill: 999px;

--border: 1px solid var(--rule);
--border-firm: 1px solid var(--rule-firm);

--shadow: 0 1px 2px rgba(20, 25, 28, 0.05);
```

Every margin, padding, and gap uses a space token. No `13px`, no `1.37rem`.

There is exactly one shadow, and it is nearly invisible. Use it on raised cards
only. Never on buttons, inputs, or table rows. No other elevation exists.

No transitions and no animation anywhere. The interface is static.

---

## 4. Layout

- Page content lives in `main`, `max-width: 64rem`, centred, with
  `padding: var(--space-7) var(--space-5) var(--space-8)`.
- The masthead and footer use the same max-width so their rules line up with the
  content edge.
- Prefer flexbox. Use grid only for genuine two-dimensional layouts, such as a
  budget card grid.
- Mobile: below `40rem`, the masthead stacks and tables scroll horizontally
  inside a wrapper rather than squashing. Never hide a column.

---

## 5. Components

Keep these exact class names. Existing templates already use most of them, and
renaming them turns a styling change into a markup change.

### Masthead — `.masthead`, `.wordmark`

Horizontal bar, `--border` on the bottom. The wordmark is `--font-display`,
weight 600, `--text-h2`, colour `--ink`. Nav links are `--font-ui`,
`--text-small`, `--ink-mid`; hover goes to `--ink`. The active link — the one
with `aria-current="page"` — is `--brand`, weight 500, with a 2px `--brand`
underline sitting on the masthead's bottom border.

### Page heading

`h1` in `--font-display` at `--text-h1`, weight 400, margin-bottom
`--space-5`. An optional `.eyebrow` above it uses the micro-label treatment.

### Data table — `.ledger`

The most important component in the app.

- Full width, `border-collapse: collapse`, background `--raised`.
- `thead th`: micro-label treatment, `--border-firm` underneath, padding
  `var(--space-2) var(--space-3)`.
- `tbody td`: padding `var(--space-3)`, `--border` underneath, vertical-align
  baseline.
- Row hover: background `--wash`.
- Numeric cells and their headers get `.num`: `--font-mono`, tabular figures,
  right-aligned, `white-space: nowrap`.
- Date cells get `.date`: `--font-mono`, tabular, `--ink-mid`.
- `.note` — a secondary line under a cell's main content: `--text-small`,
  `--ink-soft`, `display: block`.
- `.row-action` — a cell holding a row control: `width: 1%`, right-aligned.

### Amounts — `.positive`, `.negative`

Applied alongside `.num`. `.positive` is `--credit`, `.negative` is `--debit`.
Both weight 500. Always render money through the `money` Jinja filter; never
divide by 100 in a template.

### Stat block — `.summary`, `.stat`, `.stat-label`, `.stat-value`

`.summary` is a flex row, `gap: var(--space-7)`, wrapping. `.stat-label` uses
the micro-label treatment. `.stat-value` is `--font-mono`, `--text-figure`,
weight 500, tabular, colour `--ink` unless it carries `.positive`/`.negative`.

### Card — `.card`

New component. Background `--raised`, `--border`, `--radius-card`,
`padding: var(--space-4)`, `--shadow`. Use for budget entries, report panels,
and grouped content. A `.card-title` inside uses the micro-label treatment.

### Forms — `.entry`, `.field`, `.field.grow`

`.entry` is a horizontal flex row of fields in a `.card`, aligned to the
baseline of the controls, `gap: var(--space-3)`. `.field` is a column of label
plus input, `gap: var(--space-1)`. `.grow` flexes to fill.

Inputs and selects: `--font-ui`, `--text-body`, padding
`var(--space-2) var(--space-3)`, `--border`, `--radius-control`, background
`--raised`. On focus the border becomes `--brand`.

Every input has a `<label>` with a matching `for`/`id`.

### Buttons

| Class | Look |
| --- | --- |
| `button`, `.btn` | Background `--brand`, text `--raised`, weight 500, padding `var(--space-2) var(--space-4)`, `--radius-control`. Hover `--brand-deep`. |
| `.btn-secondary` | Transparent background, `--border-firm`, text `--ink`. Hover background `--wash`. |
| `.link-button` | Looks like a link: no background or border, `--ink-mid`, `--text-small`, underlined in `--rule`. Hover `--debit` for destructive row actions. |

### Badge — `.badge`

New component. Inline, `--radius-pill`, `--text-micro`, uppercase, letter-spacing
`0.06em`, padding `var(--space-1) var(--space-3)`. Variants: `.badge-warn`
(background `--warn-wash`, text `--warn`, `1px solid var(--warn)`), and
`.badge-neutral` (background `--wash`, text `--brand`).

Use `.badge-warn` for over-budget status. **A badge always contains a word** —
"over budget", "skipped", "uncategorised". Never a bare coloured dot.

### Supporting classes

`.hint` — muted line under a form, `--text-small`, `--ink-soft`.
`.empty` — centred empty state, `--ink-mid`, padding `var(--space-7)` vertical.
`.gap` — narrow column, `max-width: 34rem`, for placeholder pages.
`.lede` — `--text-lede`, `--ink-mid`.
`.more` — trailing "see everything →" link, `--text-small`, `--brand`.

### Links and focus

Body links are `--brand` with `text-decoration-color: var(--rule)` and
`text-underline-offset: 3px`; hover brings the underline to `currentColor`.

```css
:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}
```

Never remove it. A control with a custom focus style still needs a visible one.

---

## 6. Accessibility

- **Never encode meaning in colour alone.** Over budget, error, skipped, warning
  — each needs a word or a label next to the colour. A red number on its own is
  not a status. This is what `.badge` exists for.
- Contrast against `--surface`, measured:

  | Token | Ratio | Use |
  | --- | --- | --- |
  | `--ink` | 16.5:1 | Anything |
  | `--brand` | 8.7:1 | Anything |
  | `--debit` | 6.9:1 | Anything |
  | `--ink-mid` | 6.1:1 | Anything |
  | `--ink-soft` | 3.1:1 | **Labels and decorative text only** |

  `--ink-soft` fails AA for body text. That's why it's restricted to micro-labels
  and placeholders. Never use it for content someone has to read.
- One `h1` per page, `h2` for sections, no skipped levels, no fake headings made
  from styled paragraphs.
- Tables use a real `<thead>` with `<th>` cells.
- Nav links carry `aria-current="page"` on the active page. Adding a page to the
  nav means adding that conditional.
- A control that destroys data says what it destroys.
- No emoji and no icon font. The single `→` in the app is a literal character.

---

## 7. Implementation

- Everything lives in `src/ledger/static/app.css`. No `<style>` blocks, no
  `style="..."` attributes, no second stylesheet.
- Structure the file in this order: `:root` tokens, reset, base elements,
  layout, components, utilities. Section comments in the existing format:

  ```css
  /* Data table -------------------------------------------------------------- */
  ```

- Templates extend `base.html` and fill `{% block content %}`. Pass `title` in
  the context — it drives the `<title>` element and the nav's active state.
- Styling changes never change behaviour. No route changes, no repository
  changes, no template logic beyond adding classes and wrapper elements.

---

## Before you call it done

- [ ] Font link added to `base.html`; all three families in use
- [ ] Headings are the serif; every figure is mono with tabular numerals
- [ ] No raw colour values anywhere in the diff — tokens only
- [ ] All spacing from the scale
- [ ] `--debit` used only for negative amounts; `--warn` for attention states
- [ ] Every warning or status carries a word, not just a colour
- [ ] One shadow, on cards only; no transitions or animation
- [ ] Focus ring visible on every interactive element
- [ ] Active nav link styled and carrying `aria-current`
- [ ] Every page checked: dashboard, transactions, categories, budgets, reports,
      and the not-built placeholders
- [ ] Page still works with the font link removed
- [ ] `make check` still green — behaviour unchanged
