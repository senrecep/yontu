---
name: yontu
description: The lettercutter's slate. A Turkish humanizer and TDK linter for AI agents, presented as stone and chisel.
colors:
  limestone: "#e9e4da"
  limestone-deep: "#ddd6c9"
  limestone-lip: "#f4efe6"
  ink: "#1b1a17"
  ink-soft: "#4a463f"
  groove: "#c4bcad"
  slate: "#1f2a44"
  slate-raw: "#1a2339"
  terminal: "#121a2b"
  chalk: "#f4ebdd"
  chalk-soft: "#b9b3a6"
  cut: "#e8833a"
  cut-ink: "#974310"
  night-ground: "#141c2e"
  night-ground-deep: "#10172a"
  night-ground-hi: "#263250"
  night-ink: "#ece6da"
  night-groove: "#0b1120"
  term-error: "#f7a8a0"
  term-warn: "#ebcb86"
  term-info: "#a9bdd9"
typography:
  display:
    fontFamily: "Piazzolla Variable, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(36px, 5vw, 60px)"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "Piazzolla Variable, Iowan Old Style, Georgia, serif"
    fontSize: "36px"
    fontWeight: 600
    lineHeight: "40px"
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Piazzolla Variable, Iowan Old Style, Georgia, serif"
    fontSize: "24px"
    fontWeight: 600
    lineHeight: "32px"
  body:
    fontFamily: "Geist Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: "24px"
  body-lead:
    fontFamily: "Geist Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: "28px"
  label:
    fontFamily: "Geist Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: "20px"
  code:
    fontFamily: "Geist Mono Variable, ui-monospace, SF Mono, Menlo, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "20px"
rounded:
  xs: "2px"
  sm: "4px"
  md: "8px"
  lg: "12px"
spacing:
  "0": "0"
  "2": "2px"
  "4": "4px"
  "8": "8px"
  "12": "12px"
  "16": "16px"
  "24": "24px"
  "32": "32px"
  "40": "40px"
  "48": "48px"
  "64": "64px"
  "80": "80px"
  "96": "96px"
components:
  button-chalk:
    backgroundColor: "{colors.chalk}"
    textColor: "{colors.slate}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
  button-chalk-hover:
    backgroundColor: "#ffffff"
  code-copy-on-slate:
    backgroundColor: "{colors.chalk}"
    textColor: "{colors.slate}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
  code-copy-on-stone:
    backgroundColor: "{colors.slate}"
    textColor: "{colors.chalk}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
  tablet:
    backgroundColor: "{colors.slate}"
    textColor: "{colors.chalk}"
    padding: "24px"
  slab-dressed:
    backgroundColor: "{colors.chalk}"
    textColor: "{colors.slate}"
    padding: "24px"
  slab-rough:
    backgroundColor: "{colors.slate-raw}"
    textColor: "{colors.chalk}"
    padding: "24px"
  route-card:
    backgroundColor: "{colors.slate-raw}"
    textColor: "{colors.chalk-soft}"
    padding: "24px"
  terminal-output:
    backgroundColor: "{colors.terminal}"
    textColor: "{colors.chalk}"
    rounded: "{rounded.sm}"
    padding: "16px"
  nav-pill:
    backgroundColor: "{colors.limestone}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "4px 4px 4px 12px"
  nav-link-current:
    backgroundColor: "{colors.slate}"
    textColor: "{colors.chalk}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
---

# Design System: yontu

## Overview

**Creative North Star: "The Lettercutter's Slate"**

The page is a lettercutter's slate: the README is the stone and yontu is the chisel. A flat warm limestone ground carries the reading text. Navy slate fields own whole bands and panels. Cream letters sit on the slate as if incised. Burnt orange appears only for material that was cut away (struck-through phrases, the full stop in the risk line, small icons). The world is editorial and quiet, with no illustration and no decoration beyond the cuts themselves.

Density is measured: a 1200px container, generous 64 to 96px band padding, and short 680px measures for explanatory copy. The before and after slab replaces a conventional tagline hero and feature-card grid. Proof is shown as real terminal output on slate tablets, not as claims.

The build follows the direction contract. Where it diverges (see Do's and Don'ts, last list) the build is recorded as it ships.

**Key Characteristics:**
- Flat surfaces only; depth comes from tone shifts between limestone, deep limestone and slate, and from incised grooves.
- Corners are either nearly square (2 to 4px) or chiselled by octagonal clip-path; never pillowy.
- Serif for headings only, sans for reading, mono for real terminal and code content.
- Light and dark schemes both supported through `prefers-color-scheme`; the slate is identical in both.
- The heading gradient and Phosphor regular icons are fixed commitments of the brand.

## Colors

A restrained stone palette: warm limestone and ink for reading, one navy slate and cream chalk for carved fields, and a single orange reserved for what was removed.

### Primary
- **Lettercutter Slate** (#1f2a44): Slate bands, tablets, active nav item, chalk-on-slate contrast. Identical in light and dark schemes.
- **Cream Chalk** (#f4ebdd): Text and incised letters on slate; the fill of the primary button and the dressed slab.

### Secondary
- **Cut Orange** (#e8833a): Struck-through "cut" phrases and the cut marker on dark fields. Decorative or large-text use on slate only.
- **Cut Ink Orange** (#974310): The accessible orange for text and icons on limestone (benefit icons, active mobile menu item, the risk-line full stop). In dark scheme the token resolves to Cut Orange.

### Neutral
- **Limestone** (#e9e4da): Page ground in light scheme. Deep Limestone (#ddd6c9) fills the alternate band and hover states; Limestone Lip (#f4efe6) is the highlight line under a groove.
- **Ink** (#1b1a17) and **Soft Ink** (#4a463f): Primary and secondary text on limestone.
- **Groove** (#c4bcad): The dark cut of an incised rule.
- **Raw Slate** (#1a2339), **Terminal** (#121a2b): Darker nested fields on slate (rough slab, route cards, terminal and code rows).
- **Soft Chalk** (#b9b3a6): Secondary text on slate.
- **Night ground** (#141c2e), **Night deep** (#10172a), **Night raised** (#263250), **Night ink** (#ece6da), **Night groove** (#0b1120): The dark scheme remaps ground, text and rules to a navy ground; slate bands stay slate.
- **Terminal semantics**: error (#f7a8a0), warning (#ebcb86), info (#a9bdd9). Used only inside terminal output.

### Named Rules
**The Cut Rule.** Orange means material removed. It is not an accent for buttons, links or decoration.

**The Light Orange Rule.** On limestone, orange text is always Cut Ink (#974310) for AA; the bright orange is only for slate grounds.

**The Heading Gradient Rule.** Display headings carry a vertical text gradient: light scheme #000000 to #666666, dark scheme #ffffff to #9b9b9b, with a solid ink fallback. This is an owner mandate; do not alter its stops.

## Typography

**Display Font:** Piazzolla Variable (with Iowan Old Style, Georgia, serif)
**Body Font:** Geist Variable (with ui-sans-serif, system-ui)
**Label/Mono Font:** Geist Mono Variable (with ui-monospace, SF Mono, Menlo)

**Character:** A sturdy editorial serif carries the voice of the carved word; Geist stays neutral for reading; mono is reserved for what a terminal actually prints. All three are self-hosted through @fontsource-variable with Turkish coverage. Turkish pages disable common ligatures so the fi ligature does not swallow the dotted i.

### Hierarchy
- **Display** (600, 36px / 48px / 60px at mobile / 640 / 1024, line-height 40px then 1, -0.015em): Hero claim and tagline reveal.
- **Headline** (600, 30px mobile, 36px from 768px, line-height 36px / 40px, -0.01em): Section h2. The risk line scales to 48px.
- **Title** (600, 24px / 32px; 20px / 28px for small h3; 18px / 28px for FAQ questions): Slab titles, benefits, steps, routes.
- **Body** (400, 16px / 24px; lead 18px / 28px up to 20px in the hero): Paragraphs capped at 600 to 680px; secondary copy in Soft Ink.
- **Label** (600, 14px / 20px, sentence case, no tracking): Captions, slab labels, legends, nav links.
- **Code** (mono, 12 to 14px, 18px for the large install command): Terminal output, install commands, ledger, rule tags.

### Named Rules
**The Serif Is For Headings Rule.** Piazzolla appears on headings, the claim, step numerals and the large 404 numeral, plus the quoted sample sentences inside slabs. Body paragraphs never use it.

**The Real Output Rule.** Mono is used only for genuine command or terminal content, not as a stylistic label voice.

**The Two Weights Rule.** Weights are 400, 500 (step numerals, rule tags) and 600. Nothing heavier, and no italics anywhere.

## Layout

A single 1200px centred container with 16px side padding, 32px from 768px. Sections are full-width bands with 64px vertical padding, 96px from 1024px. Grids collapse to one column below 1024px (hero, slabs, FAQ, proof), 900px for the three steps, 768px for benefits and routes, and nav links fold into a full-screen menu below 960px. The hero is a split: copy at up to 680px left, a slate tablet of real lint output right.

Spacing follows a fixed scale: 0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96. Gaps inside components sit at 4 to 24; gaps between blocks at 32 to 64; band padding at 64 to 96. Type follows the Tailwind scale (12, 14, 16, 18, 20, 24, 30, 36, 48, 60, plus 96 for the 404 numeral).

Motion uses one easing, cubic-bezier(0.22, 1, 0.36, 1), with three durations: 300ms for colour and small state, 500ms for layout and menu items, 700ms for reveals. Scroll reveals lift 32px and fade in; the tagline lights word by word; cut phrases strike through in sequence on the slab. With `prefers-reduced-motion: reduce` every transition and animation collapses to 0.01ms and smooth scroll is off; reveals are set up only when motion is allowed and scripting runs.

## Elevation & Depth

Flat. There are no drop shadows. Depth is conveyed by tone: limestone, deeper limestone, slate, and nested raw slate or terminal fields inside slate. The one exception in form is the incised groove (below), which is a rule, not elevation. Dark scheme uses a navy ground rather than black.

### Named Rules
**The Incised Groove Rule.** Section dividers are a 2px full-width dark cut (Groove) with a 1px light lip (Limestone Lip) directly beneath. A groove always spans the full width of its container. Never draw a one-sided border or a single hairline in its place.

**The Flat Ground Rule.** Backgrounds are solid colours. No gradients on surfaces, no images behind text; the only gradient is on heading glyphs.

## Shapes

Two silhouettes. Small controls (buttons, code rows, terminal blocks, inline code, tags) use 2 to 4px radii. Panels use a chiselled corner: an octagon clip-path with 12px cuts (`--bevel`) for tablets and the dressed slab, 8px cuts (`--bevel-sm`) for route cards and step code rows. The rough slab uses an irregular hand-cut polygon to depict unfinished stone, and only for the "before" state. Nav and larger code rows use 8 to 12px radii as the only softer shapes.

## Components

### Buttons
- **Shape:** Near-square (4px radius), 8px 12px padding, 16px / 24px, weight 600.
- **Primary (chalk):** Cream fill with slate text, used on slate fields. Hover turns white over 300ms.
- **Copy button:** Inverts to the field: chalk on slate code rows, slate on stone rows; icon swaps from copy to check when done.
- **Focus:** 2px outline offset 2px, slate on light grounds, chalk on slate and in dark scheme.

### Slate tablet and slabs
Slate panel, 24px padding (32px from 768px), chiselled corner. Dressed slab is chalk on slate text with bevel; rough slab is raw slate with the irregular clip.

### Terminal output
Terminal-colour block, 4px radius, 16px padding, mono 12px (14px from 768px), semantic colours for error, warn and info lines.

### Navigation
A floating pill fixed 16px from the top: limestone at 76% mix, 1px ink hairline, 12px radius, links in 14px 600 with 8px radius hover fill; current page is slate with chalk text. Below 960px a menu toggle opens a full-screen limestone sheet with 30px serif links, staggered at 60ms steps.

### FAQ
Native details elements separated by grooves; a CSS plus mark rotates into a minus over 300ms.

### Signature: the cut phrase
Struck-through text (2px line) in Cut Orange on slate, the visual device for removed wording; the legend and rule tags (mono, 12px, 1px outline, 2px radius) label which rule cut it.

## Do's and Don'ts

### Do:
- **Do** use Piazzolla 600 only for headings and the claim; Geist for reading; mono only for real terminal content.
- **Do** use #974310 for any orange text on limestone, and #e8833a only on slate.
- **Do** separate sections with full-width incised grooves.
- **Do** use `--bevel` (12px) or `--bevel-sm` (8px) clip-paths for panels, and 2 to 4px radii for small controls.
- **Do** keep surfaces flat and let tone shift carry hierarchy.
- **Do** use Phosphor regular icons, inlined, with `aria-hidden`.
- **Do** animate with cubic-bezier(0.22, 1, 0.36, 1) at 300 / 500 / 700ms and honour reduced motion.
- **Do** keep the heading gradient stops exactly as mandated.

### Don't:
- **Don't** use orange as a general accent, link colour or button fill; it marks removed material.
- **Don't** use italics or weights above 600.
- **Don't** use one-sided borders or single hairlines as section rules.
- **Don't** add drop shadows, glows or surface gradients.
- **Don't** set body copy in the serif or labels in mono.
- **Don't** use pure black or pure white as a ground; dark scheme grounds on navy (#141c2e).

### Not canonized (defects the build carries)
- The floating nav uses a backdrop blur and a translucent fill (glass treatment); it is shipped but is not a rule for new surfaces.
- Several one-off hex values sit outside the token set (#2b385a hover, #4a5470 slab label, #e3d8c6 inline code, #ffffff hovers); they are build residue, not palette members, and the label colour should be re-checked for contrast on chalk.
- Terminal semantic colours are for terminal output only.
