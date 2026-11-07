# Formatting doctrine

How editorial formats prose, subordinate to the repository's own documentation style rules wherever its instructions name them. This file is the fallback when they name none, and, for a page GitHub renders, it defers to standards' [Document Styling guide](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-&-Formatting.md). Read this before any markdown beautification.

This file is the **doctrine** layer: the beauty principle, the precedence,
and the scope by destination. The exhaustive **syntax** lives
in four companions, loaded on demand: `references/markdown-reference.md` (every
markdown element, with the exact syntax, a worked example, and a portability note),
`references/admonitions.md` (callouts: GitHub's five, and Obsidian's full set
for a target that renders it),
`references/plain-text.md` (true plain text: `.txt`, plain-text email, the
no-Markdown-into-raw-text rule, line wrapping, format=flowed, the `-- ` signature),
and `references/messaging-formats.md` (the per-platform chat-dialect matrix for
Slack, Discord, WhatsApp, Telegram, Teams, iMessage, and Reddit). The
machine-readable callout aliases are in `assets/callout-types.json`. Reach for the
syntax references when you need the precise form of an element; this file tells you
when and why to use it.

## Precedence (read first)

> [!WARNING]
> **The repository's rules outrank this file.**
> A file in a repository follows the documentation style its `AGENTS.md` or `CLAUDE.md` sets, and the style guides, frontmatter or note schema, heading and link conventions, and checks those instructions name. When they name a lint or docs check, that check is the **exit gate**: a piece that fails it is not done, no matter how it reads. Where the repository names no style, this file and its companions are the default, and a **page GitHub renders** (a `README.md`, docs pages, the files under `.github/`) follows standards' [Document Styling guide](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-&-Formatting.md).

The order, hardest first: the repository's instructions and the folder's own rules, then the style guide and checks they name, then (where they name none) the Document Styling guide for a page GitHub renders, then this file, then your user's per-document override (which can raise density but never break a hard rule).

## Scope - where the file lives

Three destinations, three rule sets. Do not invent a parallel "portability tier" vocabulary; the destination already draws the line.

- **A file in a repository whose instructions set a documentation style:** follow those rules: their heading rule (some want one H1 that opens with an emoji, some forbid emoji), their frontmatter or note schema, their link convention (some notes use wikilinks, most repositories use relative Markdown links), the callout types they allow, and the check they name. Where a rule here conflicts, theirs wins.
- **A file in a repository that names no style, or a page GitHub renders:** GitHub-Flavored Markdown: CommonMark plus tables, task lists, strikethrough, footnotes, the five alerts, math, and Mermaid. Follow standards' [Document Styling guide](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-&-Formatting.md) for a page GitHub renders. No wikilinks; no em dash.
- **Leaving the repository** (an email, a post, a file handed to someone): follow the **target's own format**. For a markdown target, GitHub-Flavored Markdown is the default; the portable core is CommonMark, so drop everything the target cannot render. A target that renders more, such as Obsidian, may take its own constructs (`references/admonitions.md` has Obsidian's callout set).

> [!CAUTION]
> **Wikilinks stay where they are the convention.**
> A wikilink resolves only in wiki-style tools such as Obsidian; every other renderer shows the raw double brackets as literal text. Use one only in a repository whose instructions say its notes link that way, never on a page GitHub renders. When a piece leaves such a repository, convert each wikilink to a real link or plain text.

## Callouts: the GitHub five

A callout (GitHub calls it an alert) is a blockquote whose first line is a
bracketed bang-type marker, in uppercase and alone on its line. The body is
ordinary markdown on the following `>` lines.

```markdown
> [!NOTE]
> **An optional bold lead-in.**
> The body is ordinary markdown. Keep a blank `>` line before any list or code
> block inside.
```

Unless the repository's rules allow more, use exactly the five types GitHub renders:

- **NOTE** - context worth knowing even when skimming; also the stop-early summary at the top of a long piece.
- **TIP** - advice: a better or faster way to do the thing.
- **IMPORTANT** - the one point the reader needs to succeed.
- **WARNING** - a hazard that needs attention now.
- **CAUTION** - the risk or negative outcome of an action, such as data loss.

The doctrine points to keep in mind:

- **No title after the marker.** GitHub takes none; give a callout a title as a bold lead-in on its first body line.
- **Sparingly, and never nested.** GitHub advises one or two per document; signal-scarcity (below) agrees.
- **No folding.** For optional depth in a long doc, use a collapsible `<details>` block.
- **Obsidian's full set** (abstract, info, todo, success, question, failure, danger, bug, example, quote, the foldable `-` and `+` variants, custom titles) is for a target that renders it. The catalog, with every alias and the degradation behavior, is in `references/admonitions.md`, and the machine-readable list in `assets/callout-types.json`.

## Rich markdown the doctrine reaches for (where it earns its place)

- **Tables** (GFM) for genuinely tabular data; set alignment in the delimiter row; keep them narrow, a wide table loses to a list.
- **Fenced code** with a language tag on every fence; `text` for output, `diff` for diffs.
- **Mermaid** diagrams kept as code (`mermaid` fence), matched to the relationship (`flowchart` for process, `sequenceDiagram` over time, `stateDiagram` for transitions). A Mermaid diagram **inside a file under edit is editorial**; a diagram asked for **as a chat answer is `visualize`**.
- **Math** in LaTeX (`$inline$`, `$$block$$`) where the target renders it.
- **Collapsible `<details>`** for optional depth, the density tool for a long doc (renders on GitHub).
- **Footnotes, task lists, strikethrough** where the target supports them (GFM, not plain CommonMark).

Match the element to the content, never reach for variety. The principle holds: structure before style, whitespace is structural, the right element for the job, restraint with rich content, keep the source readable.

## Other lightweight markup

When the target document is itself written in a non-Markdown lightweight markup, reStructuredText, AsciiDoc, MediaWiki, Org-mode, BBCode, or Textile, match **that target's** native syntax rather than emitting Markdown. These languages reuse Markdown's glyphs with different meanings, so do not pattern-match from habit: a single asterisk is bold in AsciiDoc but italic in reStructuredText, and a leading hash starts an ordered-list item in MediaWiki, not a heading. The glyphs collide, so verify the few constructs you actually need at the target's own primary docs before writing rather than carrying a stale table in your head.

## The beauty principle (default restraint, your user overrides)

> [!TIP]
> **Signal-scarcity, not maximalism.**
> "If every paragraph is important, nothing is." A callout, table, or diagram earns its place **only when it helps the reader understand faster than prose would.** That is the test for every rich element.

**Default:** master every element, deploy each only where it earns its place, with density scaled to the piece's length and stakes. A two-line note is a two-line note, not a callout with a table. A long technical document carries a `<details>` block or two, a table, and a diagram where the structure is genuinely spatial.

This is a **default, not a ceiling.** Your user overrides per document: "make this note rich," "go heavy on the formatting," "plain text only" all win over the default. State the default when you apply it, then follow your user's instruction when it differs. A collapsible `<details>` block lets a long doc stay rich without becoming a wall, putting depth one click away.

## The exit gate

For a file in a repository: after formatting, run the check its instructions name (a docs lint, a link check, a format check) and clear every error. With no named check, confirm by reading: one H1, zero em dashes (DOC-002), only the five callout types, and frontmatter in the shape the repository's other files use. The piece is done when it reads clear, sounds true, and passes the repository's check.
