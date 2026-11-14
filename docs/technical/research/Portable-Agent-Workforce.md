<!--
title: '🔎 PORTABLE AGENT WORKFORCE'
description: 'How to write a team of AI agent definitions once and run it in local agent apps, API orchestrators and Grok, as of November 2026: file formats, names with spaces and a star, Grok Bot and the xAI API, and how agents should message each other. The research behind workforce/.'
type: record
verified: '2026-11-14'
focus: 'As of November 2026, what format lets one set of agent definitions run in local agent apps, API orchestrators and Grok, how must file names holding spaces, ampersands, brackets and a star be handled, and how should a hub-and-spoke workforce pass messages?'
decision: '[ADR-0044](../../adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md)'
-->

<div align="center">

# 🔎 PORTABLE AGENT WORKFORCE

<a name="top"></a>

**One source for every agent, and what each environment needs from it.**

_Every claim sourced. Every report dated._

</div>

---

## 🎯 Bottom Line

> [!IMPORTANT]
> **Write each agent once, as Markdown with flat frontmatter, and render a copy for each environment.** No single agent file format is read everywhere, but Markdown with a `---` frontmatter block is what most agent apps read, and Claude Code's folder alone is read by Claude Code, Copilot CLI, VS Code and Cursor. Grok is reachable three ways, Grok Bot, the xAI API and Grok Build, each with a documented format. Keep the persona's name, with its spaces and star, in the source, and give every copy an ASCII id. Route messages between departments through one hub that relays answers word for word. Confidence is medium to high on the formats, which rest on official documentation, and medium on Grok Bot, a beta whose multi-group rules are undocumented.

---

## 📋 Report Meta

| Attribute               | Detail                                                                                    |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Question**            | How to define a workforce of agents once and run it locally, in the cloud and on Grok     |
| **Decision it informs** | The format, layout, names, protocol and installer of `workforce/`                         |
| **Verified**            | 2026-11-14, equal to the newest log entry below                                           |
| **Confidence**          | Medium - official documentation throughout, but no app was run against the rendered files |
| **Sources**             | 45 fetched directly / 48 total, itemized under Sources & Provenance                       |
| **Supersedes**          | N/A                                                                                       |
| **Graduated to**        | [ADR-0044](../../adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md)                     |

---

## 📅 Log Entry: 2026-11-14

### 🎯 Objective

Find the facts needed to write about fifty agent definitions once and install them in local agent apps, API orchestrators and Grok, with file names that hold spaces, `&`, brackets and a star, and a message protocol for a mesh inside each department and a hub between departments.

### 🔭 Scope

- **In scope**: agent file formats of the major agent apps and specifications; tool schema portability across APIs; Grok Bot, Grok Build and the xAI API; file names across git, GitHub, archives, shells and the three desktop systems; orchestration topologies, message envelopes, shared memory and approval gates.
- **Out of scope**: which models to run each agent on, cost per task, and evaluating the agents' answers.

### 🧪 Method

- Three research passes ran in parallel in one Claude Code session on 2026-11-14, each reading official documentation and primary sources and writing a full report with every quote and URL: agent file formats and tool schemas; xAI and Grok; file names and agent communication.
- The file-name pass also ran tests on Ubuntu 24.04 with git 2.43, Python 3.13, GNU tar 1.35, Info-ZIP 3.0 and curl 8.5, including live requests to raw.githubusercontent.com for paths holding spaces, `&`, brackets and a non-ASCII letter.
- **Provenance note**: the sources below were fetched directly by those passes. x.ai's news index and changelog and help.x.com returned 403; their claims rest on other official pages. Windows, macOS, GitHub's contents API and loading the names in any agent app were not tested.

### 🔎 Findings

1. **Claude Code reads a subagent as Markdown with YAML frontmatter, requiring `name` and `description`, and skips a file silently when its frontmatter is malformed.** `name` may be up to 256 characters without `:`; the file name need not match; folders are scanned recursively.
   - **Source**: [Claude Code docs: sub-agents](https://code.claude.com/docs/en/sub-agents) - ✅ fetched directly
   - **Confidence**: High - official reference
2. **Claude Code runs an agent as the main session with `claude --agent`, lets subagents nest three levels by default, and warns at startup when all descriptions together pass 15,000 tokens.** Agent teams, with a shared task list and messaging, exist but are experimental and interactive only.
   - **Source**: [Claude Code docs: sub-agents](https://code.claude.com/docs/en/sub-agents), [Claude Code docs: agent-teams](https://code.claude.com/docs/en/agent-teams) - ✅ fetched directly
   - **Confidence**: High
3. **Copilot CLI and VS Code also load agents from `.claude/agents/`, and Cursor reads `.claude/agents/` and `.codex/agents/`.** One Claude Code copy therefore serves four apps.
   - **Source**: [GitHub Docs: cli-command-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference), [VS Code docs: custom-agent-file-reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference), [Cursor docs: subagents](https://cursor.com/docs/subagents) - ✅ fetched directly
   - **Confidence**: High
4. **GitHub Copilot's custom agents are `.agent.md` files whose names take only `.`, `-`, `_`, letters and digits, with a body of at most 30,000 characters.** Tool aliases are `read`, `edit`, `search`, `execute`, `agent`, `web` and `todo`, and Claude Code's names are accepted as aliases.
   - **Source**: [GitHub Docs: custom-agents-configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) - ✅ fetched directly
   - **Confidence**: High
5. **Codex takes one TOML file per custom agent, in `.codex/agents/` or `~/.codex/agents/`, requiring `name`, `description` and `developer_instructions`.** Sandbox, approvals and MCP are inherited and cannot be set per agent.
   - **Source**: [OpenAI docs: subagents](https://developers.openai.com/codex/subagents) - ✅ fetched directly
   - **Confidence**: High
6. **Only `AGENTS.md` and Agent Skills have real adoption across tools; for personas, Markdown with frontmatter is the de facto format.** Gemini CLI, Antigravity, opencode and Devin CLI read their own agent folders in it; A2A's Agent Card describes an agent for discovery, not its prompt.
   - **Source**: [AGENTS.md](https://agents.md/), [Agent Skills: specification](https://agentskills.io/specification), [Gemini CLI docs: subagents](https://geminicli.com/docs/core/subagents/), [GitHub: a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto) - ✅ fetched directly
   - **Confidence**: Medium - a judgment across many vendors' pages
7. **Claude Managed Agents nest one level deep, with at most twenty predefined subagents.**
   - **Source**: [Claude Platform docs: multiagent-orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) - ✅ fetched directly
   - **Confidence**: High
8. **Ollama, LM Studio, Open WebUI, LibreChat and AnythingLLM all take OpenAI-style function calling; an Ollama Modelfile carries `FROM` and `SYSTEM`, and tools travel with each request.**
   - **Source**: [Ollama docs: modelfile](https://docs.ollama.com/modelfile), [Ollama docs: openai-compatibility](https://docs.ollama.com/api/openai-compatibility), [LM Studio docs: tools](https://lmstudio.ai/docs/developer/openai-compat/tools) - ✅ fetched directly
   - **Confidence**: High

9. **A tool definition every API accepts uses a name matching `^[a-z][a-z0-9_]{0,63}$`, an object root, every property required, `additionalProperties: false` and string enums only.** OpenAI caps names at 64 characters, Anthropic and MCP at 128, and Gemini allows `:` and `.`. `$ref`, `oneOf`, `anyOf`, `allOf`, `format`, ranges, lengths and defaults are rejected or stripped by at least one of them.
   - **Source**: [OpenAI docs: function-calling](https://developers.openai.com/api/docs/guides/function-calling), [Claude Platform docs: define-tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), [Gemini API docs: caching](https://ai.google.dev/api/caching), [MCP specification: tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) - ✅ fetched directly
   - **Confidence**: High

10. **Grok Bot, in beta since 2026-08-11, runs one Bot per job; a personal Bot has no field for instructions and takes its job, sources and approval limits in its first message, and xAI calls its memory "not a source of truth".**
    - **Source**: [xAI: introducing-grok-bot](https://x.ai/news/introducing-grok-bot), [xAI docs: bots](https://docs.x.ai/grok-bot/bots) - ✅ fetched directly
    - **Confidence**: High
11. **xAI sets "roughly 50 Bots per account and six per group chat"; a group chat holds two to six Bots, and one Bot can message another directly.** Whether one Bot can sit in several groups is documented nowhere, nor whether group chats count against the Bot limit.
    - **Source**: [xAI: designing-grok-bot](https://x.ai/news/designing-grok-bot), [xAI docs: chat-and-collaboration](https://docs.x.ai/grok-bot/chat-and-collaboration) - ✅ fetched directly; multi-group membership ❌ could not verify
    - **Confidence**: High for the limits, none for multi-group membership
12. **A Grok Bot's connected apps, GitHub among them, are available to every Bot on the account, and there is no public API to create or message Bots.** A primary Bot coordinates the others and can create focused Bots.
    - **Source**: [xAI docs: computer-and-apps](https://docs.x.ai/grok-bot/computer-and-apps), [xAI docs: how-grok-bot-works](https://docs.x.ai/grok-bot/how-grok-bot-works) - ✅ fetched directly
    - **Confidence**: High
13. **Grok Build reads custom agents from `.grok/agents/` and `~/.grok/agents/`, as Markdown with YAML frontmatter (`name`, `description`, `tools`, `mcpServers`), runs one as the main session with `--agent`, nests subagents one level, and needs `--trust` for project files in a headless run.** Whether it reads `.claude/agents/` is not documented, and its tool names are not listed.
    - **Source**: [xAI docs: subagents](https://docs.x.ai/build/features/subagents), [xAI docs: project-rules](https://docs.x.ai/build/features/project-rules), [xAI docs: reference](https://docs.x.ai/build/settings/reference) - ✅ fetched directly
    - **Confidence**: Medium - a beta, with gaps
14. **The xAI API is OpenAI-compatible at `https://api.x.ai/v1`, recommends the Responses API, takes up to 350 tools per request, and reads its key from `XAI_API_KEY`.** Chat Completions is marked deprecated but works.
    - **Source**: [xAI docs: quickstart](https://docs.x.ai/developers/quickstart), [xAI docs: function-calling](https://docs.x.ai/developers/tools/function-calling) - ✅ fetched directly
    - **Confidence**: High

15. **The star U+2B50 alone is the fully qualified emoji, and U+2B50 followed by the variation selector U+FE0F is a different byte sequence that every filesystem and git keep as a separate name; no Unicode normalization merges the two.**
    - **Source**: [Unicode: emoji-test.txt](https://www.unicode.org/Public/emoji/latest/emoji-test.txt), [Unicode: tr51](https://www.unicode.org/reports/tr51/) - ✅ fetched directly, and tested
    - **Confidence**: High
16. **Git for Windows refuses `: < > " | ? *`, names ending in a space or a dot, and device names such as `CON` even with an extension; `&`, brackets, spaces and emoji pass. Paths past 260 characters fail unless long paths are turned on.**
    - **Source**: [git source: mingw.c](https://raw.githubusercontent.com/git/git/master/compat/mingw.c), [Microsoft Learn: naming-a-file](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) - ✅ fetched directly
    - **Confidence**: High
17. **raw.githubusercontent.com matches path bytes exactly: percent-encoded spaces, `&` and brackets work, `+` for a space and a decomposed letter return 404. GitHub's zip archives mark names as UTF-8, while its tarballs carry no UTF-8 marker for short paths.**
    - **Source**: tested live; [git source: archive-zip.c](https://raw.githubusercontent.com/git/git/master/archive-zip.c), [git source: archive-tar.c](https://raw.githubusercontent.com/git/git/master/archive-tar.c) - ✅ fetched directly; that Windows `tar` then garbles the star is 🟡 inferred from libarchive's source
    - **Confidence**: High for GitHub, Low for the Windows tarball
18. **A YAML value that starts with `&` is an anchor, which a loader drops without an error.**
    - **Source**: [YAML spec: 1.2.2](https://yaml.org/spec/1.2.2/) - ✅ fetched directly, and tested with PyYAML
    - **Confidence**: High

19. **Orchestrator and workers fits work whose subtasks cannot be predicted, and every delegation needs an objective, the shape of the answer, the tools and sources to use, and its boundaries; vague briefs caused duplicated work.**
    - **Source**: [Anthropic: building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents), [Anthropic: multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system) - ✅ fetched directly
    - **Confidence**: High
20. **A supervisor that paraphrases its sub-agents' answers loses accuracy; forwarding them verbatim, and trimming handoff messages, recovered it.**
    - **Source**: [LangChain: benchmarking-multi-agent-architectures](https://www.langchain.com/blog/benchmarking-multi-agent-architectures) - ✅ fetched directly
    - **Confidence**: Medium - one benchmark
21. **A2A's task states are submitted, working, input-required, auth-required, completed, failed, canceled and rejected, and a finished task never restarts.**
    - **Source**: [A2A specification: specification](https://a2a-protocol.org/latest/specification/) - ✅ fetched directly
    - **Confidence**: High
22. **Irreversible or high-stakes actions need a person's approval, enforced outside the model, bound to the exact arguments: a changed argument needs a new approval.**
    - **Source**: [OWASP: llm062025-excessive-agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), [OpenAI Agents SDK: human_in_the_loop](https://openai.github.io/openai-agents-python/human_in_the_loop/), [Microsoft Learn: tool-approval](https://learn.microsoft.com/agent-framework/agents/tools/tool-approval) - ✅ fetched directly
    - **Confidence**: High
23. **Multi-agent systems fail in fourteen documented ways in three groups (system design, misalignment between agents, and task verification), and an explicit verification step improved results.**
    - **Source**: [arXiv: 2503.13657](https://arxiv.org/abs/2503.13657) - ✅ fetched directly
    - **Confidence**: Medium - one study

### 📚 Sources & Provenance

| Source                                                                                                                         | Fetched   | Backs / notes              |
| :----------------------------------------------------------------------------------------------------------------------------- | :-------- | :------------------------- |
| [Claude Code docs: sub-agents](https://code.claude.com/docs/en/sub-agents)                                                     | ✅ direct | 1, 2                       |
| [Claude Code docs: agent-teams](https://code.claude.com/docs/en/agent-teams)                                                   | ✅ direct | 2                          |
| [GitHub Docs: cli-command-reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) | ✅ direct | 3                          |
| [VS Code docs: custom-agent-file-reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)   | ✅ direct | 3                          |
| [Cursor docs: subagents](https://cursor.com/docs/subagents)                                                                    | ✅ direct | 3                          |
| [GitHub Docs: custom-agents-configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)           | ✅ direct | 4                          |
| [OpenAI docs: subagents](https://developers.openai.com/codex/subagents)                                                        | ✅ direct | 5                          |
| [AGENTS.md](https://agents.md/)                                                                                                | ✅ direct | 6                          |
| [Agent Skills: specification](https://agentskills.io/specification)                                                            | ✅ direct | 6                          |
| [Gemini CLI docs: subagents](https://geminicli.com/docs/core/subagents/)                                                       | ✅ direct | 6                          |
| [GitHub: a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto)                                       | ✅ direct | 6                          |
| [Claude Platform docs: multiagent-orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)  | ✅ direct | 7                          |
| [Ollama docs: modelfile](https://docs.ollama.com/modelfile)                                                                    | ✅ direct | 8                          |
| [Ollama docs: openai-compatibility](https://docs.ollama.com/api/openai-compatibility)                                          | ✅ direct | 8                          |
| [LM Studio docs: tools](https://lmstudio.ai/docs/developer/openai-compat/tools)                                                | ✅ direct | 8                          |
| [OpenAI docs: function-calling](https://developers.openai.com/api/docs/guides/function-calling)                                | ✅ direct | 9                          |
| [Claude Platform docs: define-tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)               | ✅ direct | 9                          |
| [Gemini API docs: caching](https://ai.google.dev/api/caching)                                                                  | ✅ direct | 9                          |
| [MCP specification: tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)                              | ✅ direct | 9                          |
| [xAI: introducing-grok-bot](https://x.ai/news/introducing-grok-bot)                                                            | ✅ direct | 10                         |
| [xAI docs: bots](https://docs.x.ai/grok-bot/bots)                                                                              | ✅ direct | 10                         |
| [xAI: designing-grok-bot](https://x.ai/news/designing-grok-bot)                                                                | ✅ direct | 11                         |
| [xAI docs: chat-and-collaboration](https://docs.x.ai/grok-bot/chat-and-collaboration)                                          | ✅ direct | 11                         |
| [xAI docs: computer-and-apps](https://docs.x.ai/grok-bot/computer-and-apps)                                                    | ✅ direct | 12                         |
| [xAI docs: how-grok-bot-works](https://docs.x.ai/grok-bot/how-grok-bot-works)                                                  | ✅ direct | 12                         |
| [xAI docs: subagents](https://docs.x.ai/build/features/subagents)                                                              | ✅ direct | 13                         |
| [xAI docs: project-rules](https://docs.x.ai/build/features/project-rules)                                                      | ✅ direct | 13                         |
| [xAI docs: reference](https://docs.x.ai/build/settings/reference)                                                              | ✅ direct | 13                         |
| [xAI docs: quickstart](https://docs.x.ai/developers/quickstart)                                                                | ✅ direct | 14                         |
| [xAI docs: function-calling](https://docs.x.ai/developers/tools/function-calling)                                              | ✅ direct | 14                         |
| [xAI news](https://x.ai/news) (index), [xAI changelog](https://x.ai/changelog), help.x.com (no link)                           | ❌ 403    | Covered by the pages above |
| [Unicode: emoji-test.txt](https://www.unicode.org/Public/emoji/latest/emoji-test.txt)                                          | ✅ direct | 15                         |
| [Unicode: tr51](https://www.unicode.org/reports/tr51/)                                                                         | ✅ direct | 15                         |
| [git source: mingw.c](https://raw.githubusercontent.com/git/git/master/compat/mingw.c)                                         | ✅ direct | 16                         |
| [Microsoft Learn: naming-a-file](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)                         | ✅ direct | 16                         |
| [git source: archive-zip.c](https://raw.githubusercontent.com/git/git/master/archive-zip.c)                                    | ✅ direct | 17                         |
| [git source: archive-tar.c](https://raw.githubusercontent.com/git/git/master/archive-tar.c)                                    | ✅ direct | 17                         |
| [YAML spec: 1.2.2](https://yaml.org/spec/1.2.2/)                                                                               | ✅ direct | 18                         |
| [Anthropic: building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)                        | ✅ direct | 19                         |
| [Anthropic: multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)                    | ✅ direct | 19                         |
| [LangChain: benchmarking-multi-agent-architectures](https://www.langchain.com/blog/benchmarking-multi-agent-architectures)     | ✅ direct | 20                         |
| [A2A specification: specification](https://a2a-protocol.org/latest/specification/)                                             | ✅ direct | 21                         |
| [OWASP: llm062025-excessive-agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)                               | ✅ direct | 22                         |
| [OpenAI Agents SDK: human_in_the_loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)                       | ✅ direct | 22                         |
| [Microsoft Learn: tool-approval](https://learn.microsoft.com/agent-framework/agents/tools/tool-approval)                       | ✅ direct | 22                         |
| [arXiv: 2503.13657](https://arxiv.org/abs/2503.13657)                                                                          | ✅ direct | 23                         |

### ⚖️ Alternatives Considered

| Option                                                        | Pros                                                        | Cons                                                                                  |
| :------------------------------------------------------------ | :---------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| One hand-kept file per agent per app                          | Each copy exactly what its app wants                        | Five or more copies of every agent, drifting apart                                    |
| A JSON or YAML file per agent                                 | Easy to parse                                               | Long prompts read badly as strings; no app reads it as an agent                       |
| Markdown with frontmatter, rendered per app (chosen)          | Read by most apps as it is; one source; renders to the rest | Needs a renderer and a check                                                          |
| The persona's name as the file's `name`                       | One field                                                   | Cursor, Gemini CLI and Copilot's file names take only ASCII; the star and spaces fail |
| `name` as an ASCII id, `title` as the persona's name (chosen) | Every app gets an id it accepts; the owner reads the title  | Two fields to keep in step, which the check does                                      |
| Grok Bot for Grok                                             | Bots and groups the owner uses directly                     | Beta; about fifty Bots; no instruction field; multi-group undocumented                |
| The xAI API for Grok                                          | No group or Bot limits; tools and routes enforced in code   | Needs an orchestrator to host the agents                                              |

### 🛠️ Spikes / Prototypes

- `.github/scripts/workforce.py` renders all eight targets from `workforce/`, and `test_workforce.py` runs every install against a throwaway home folder - all passing on Python 3.11 and 3.13.
- The file-name pass's tests on Ubuntu: the star with and without U+FE0F as two files and two git entries; `git archive` zip and tar names; raw.githubusercontent.com requests for encoded and unencoded paths.

### 🏁 Conclusion / Recommendation

Keep each agent as one Markdown file with flat, quoted frontmatter: `name` as the ASCII id, `title` as the persona's name and file name, and capabilities instead of one app's tool names. Compose each prompt from the agent, its department's charter and one shared protocol, and render it per environment with a standard-library script that refuses broken names, variation selectors and non-portable tool schemas. Route every message between departments through the Chief of Staff, which relays answers word for word, give the vault one writer, and gate irreversible acts on the owner's yes for the exact act. On Grok, run the workforce through the xAI API when it must scale, through Grok Bot when the owner wants Bots, with each Bot's first message pointing it at its files on GitHub, and through Grok Build for work on files. Recorded as [ADR-0044](../../adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md).

### ✅ Confidence & Caveats

- **Overall confidence**: Medium
- **What would change this conclusion**: Grok Bot gaining an instruction field or an API, documenting multi-group membership, or changing its limits; Claude Code dropping Copilot's and Cursor's reading of `.claude/agents/`; Copilot changing its 30,000-character body limit.
- **Known gaps**: no agent app was run against the rendered files; Windows and macOS were not tested; Grok Build's tool names and its reading of `.claude/agents/`; whether Grok Bot group chats count toward its Bot limit.

---

## ♻️ Reverification

> [!NOTE]
> A report is trusted only inside its verification window. To reverify: re-check each claim against its cited source and the current state of the repository, then **append** a new dated entry below (never edit a past one) and bump the `verified:` frontmatter to that date - or, if the findings no longer hold, supersede or remove the report.

---

## 🤖 AI Agent Directive

> [!IMPORTANT]
> This report is **evidence, not instructions**. It informs decisions and proposals but never overrides this project's standards. Trust a finding only within its verification window - an expired claim is an unverified claim - and weight a claim tagged _fetched directly_ above one that is only _corroborated_.

### 🔗 See also

> [!TIP]
> [The Workforce](../The-Workforce.md) puts these findings to use. Durable decisions graduate to the [🧭 ADR index](../../adrs/README.md). Every canonical guide is indexed in the [📚 Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md).

---

<div align="center">

**Write each agent once. Render it for every app that runs it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
