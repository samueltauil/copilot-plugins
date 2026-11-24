# Accessibility checklist for exercise content

Based on [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [UDL Guidelines 3.0](https://udlguidelines.cast.org/), and
plain-language practice. A checklist is not a conformance audit; test with assistive technology users when you
can.

## Images

- [ ] Informative images have alt text that states what matters in the image ("Branch selector open with
      **Create branch add-docs** highlighted"), not the file name.
- [ ] Decorative images (octocat mascots) use short alt text such as "Mona celebrating", or `alt=""` when purely
      decorative.
- [ ] No instruction depends only on an arrow, a highlight, or a color in a screenshot.
- [ ] Badges have meaningful alt text ("Copilot prompt", "Terminal command").

## Text and structure

- [ ] One `##` heading per step, then `###` sections in order; no skipped levels.
- [ ] Numbered lists for sequences; tables have header rows.
- [ ] Link text describes the destination.
- [ ] Acronyms spelled out on first use; plain words; short sentences.
- [ ] Emoji support meaning but never carry it alone; screen readers read emoji names aloud, so avoid long runs.
- [ ] Pass and fail are shown with words as well as symbols (the toolkit table shows "✅ - Pass" and "❌ - Fail").

## Interaction

- [ ] Every action can be done with a keyboard; name keyboard shortcuts for both platforms
      (`Ctrl + I` on Windows and Linux, `Cmd + I` on macOS).
- [ ] Collapsible `<details>` blocks are used for optional help (they are keyboard operable).
- [ ] Time-limited actions are avoided; waiting for Mona is explained ("about 20 seconds").

## Color and media

- [ ] Diagrams and custom images meet 4.5:1 contrast for text (3:1 for large text).
- [ ] Videos have captions and a transcript, and no step requires audio.

## Requirements disclosure

- [ ] README lists accounts, plans, permissions, tools, and possible costs before the Copy Exercise button.
- [ ] Alternative routes (browser vs. local editor) are offered only when both are supported and graded fairly.
