---
name: revealjs-slides
description: Author Reveal.js HTML presentations with correct slide structure, concise slide content, and complete speaker notes.
---

# Reveal.js slide authoring

Use this skill when creating or editing Reveal.js presentations stored as HTML.

## Follow Reveal.js structure

- Treat each top-level `<section>` inside `<div class="slides">` as a horizontal slide.
- Use nested `<section>` elements only when you intentionally want a vertical slide stack.
- Place speaker notes inside `<aside class="notes">` within the corresponding slide.
- If you are editing an existing presentation template, keep changes inside the slide container unless the user explicitly asks for layout or theme changes.

## Require speaker notes on every slide

Every slide must include presenter notes. Notes should usually contain:

- 3-6 sentences of talking points
- a transition into the next slide
- likely objection handling or follow-up guidance when relevant
- timing or delivery cues such as where to pause or emphasize a point

Use notes like this:

```html
<aside class="notes">
  <p>Main talking point for this slide.</p>
  <p>Transition: "Now let's look at..."</p>
  <p>If asked about X, respond with Y.</p>
</aside>
```

## Use the available presentation utility classes

Prefer the existing Reveal.js template utility classes when they are available:

- `center-slide` for title and closing slides
- `stat-number` for large numeric callouts
- `gradient-text` for emphasized phrases
- `highlight-box` for short key takeaways
- `two-column` for side-by-side layouts
- `competitor-table` for comparisons
- `tag` for pill labels
- `check-green` for positive comparison markers
- `cross-dim` for negative or missing comparison markers
- `copilot-logo` for centered logo treatments

## Keep slide content concise and visual

- Fit all content within a 960×700px slide without scrolling.
- Prefer at most 4 bullet points per slide.
- In a `two-column` layout, allow up to 5 bullets per column.
- Keep bullets short, ideally 8 words or fewer.
- Limit `highlight-box` usage to 4 per slide, and keep each one to a single line.
- Limit stat slides to 3 major stats.
- Limit competitor tables to 6 rows and keep cells to 3-4 words.
- Use `<h2>` for slide titles except on the title slide.
- Avoid external images or new dependencies; use inline SVG, Unicode, or CSS-based visuals instead.
- Use emojis sparingly and only when they add meaning.
- Prefer styling classes over emoji for polish.
- Write final content, not placeholders.
- Use HTML directly; do not rely on Markdown plugins.

## When generating a complete deck

- Read the requirements and evaluation criteria before drafting slides.
- Generate the full requested presentation, not partial fragments.
- Replace placeholder slide content with finished HTML.
- Build a clear narrative arc such as title → problem → cost → solution → how it works → value → differentiation → proof → call to action.
- Use real, verified facts, customer names, and comparisons when the task requires them; never invent evidence.
- Use presenter-specific names, contacts, and calls to action only when the user or source material provides them. Never leave placeholders.
- Make sure every slide supports at least one business or evaluation objective, especially through the speaker notes.
