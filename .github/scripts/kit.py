#!/usr/bin/env python3
"""Render everything the home kit installs besides the rules into one bundle, `home/kit.json`.

WHY THIS EXISTS. The rules are one block, but the modules around them are
many files in three formats: the guard hook, the skills, and the subagents
written three ways. A release ships them as one JSON file, so a consumer
pins one more hash instead of one per file, and the installer writes
strings it never has to convert. The sources stay readable and reviewable,
all under `kit/`:

- `kit/guard.py`, the guard every app's pre-tool hook calls;
- `kit/skills/<name>/`, each a folder in the open Agent Skills format;
- `kit/subagents/<name>.md`, each rendered for Claude Code, Copilot and Codex.

It also holds each source to the strictest rule any target app enforces,
because a skill with a bad name loads nowhere and says nothing. `render.py`
calls it, so `make render` writes the bundle and `make check` fails on a
stale one.

Run it:

    python3 .github/scripts/kit.py            # print the bundle
    python3 .github/scripts/kit.py --check    # list every problem in the sources
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
KIT_FILE = 'home/kit.json'
GUARD_FILE = 'kit/guard.py'
SKILLS_DIR = 'kit/skills'
SUBAGENTS_DIR = 'kit/subagents'

# The line that marks a file or folder as the kit's own. The installer
# replaces what carries it and refuses to touch what does not.
OWNED = "Part of tannergolden/intelligence's home kit, which replaces this file on every install."

SKILL_NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
SKILL_KEYS = ('name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools')
RESERVED = ('synced', 'anthropic-skills')
MAX_DESCRIPTION = 1024
MAX_SKILL_LINES = 500

# The capabilities a subagent may hold, and each app's names for them.
TOOLS = {
    'read': ('Read',),
    'search': ('Grep', 'Glob'),
    'edit': ('Edit', 'Write', 'NotebookEdit'),
    'execute': ('Bash',),
    'web': ('WebFetch', 'WebSearch'),
    'agent': ('Agent',),
}
SUBAGENT_KEYS = ('name', 'description', 'tools')

# Repositories a public file may name: the public ones, and the template the
# standards name by design. Any other tannergolden repository is private.
NAMEABLE = ('intelligence', 'standards', 'dotfiles', 'path', 'knowledge', 'repo', '.github', 'tannergolden')
NAMED = re.compile(r'tannergolden/(\.?[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)')
DASHES = re.compile('[\u2013\u2014\u2015]')


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    """The `key: value` lines between a first-line `---` and the next, and the body after.

    Only flat, one-line values: the formats this kit writes need nothing more,
    and a stricter reader catches a value that would parse differently in YAML.
    """
    if not text.startswith('---\n'):
        raise ValueError('must open with --- on its first line')
    end = text.find('\n---\n', 3)
    if end == -1:
        raise ValueError('has no closing --- for its frontmatter')
    fields: dict[str, str] = {}
    for line in text[4:end].split('\n'):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = re.match(r'^([A-Za-z][A-Za-z0-9-]*):\s*(.*)$', line)
        if not match:
            raise ValueError(f'has a frontmatter line that is not "key: value": {line[:40]}')
        key, value = match.groups()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
            value = value[1:-1]
        fields[key] = value
    return fields, text[end + 5:].lstrip('\n')


def yaml_string(value: str) -> str:
    """A double-quoted YAML scalar; JSON's escapes are YAML's too."""
    return json.dumps(value, ensure_ascii=False)


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def toml_block(value: str) -> str:
    """A multi-line TOML basic string holding `value` exactly."""
    escaped = value.replace('\\', '\\\\').replace('"""', '""\\"')
    return f'"""\n{escaped}"""'


def load_skills(root: pathlib.Path, found: list[str]) -> dict[str, dict[str, str]]:
    """Every skill folder's files, as text by path inside the folder."""
    skills: dict[str, dict[str, str]] = {}
    base = root / SKILLS_DIR
    for folder in sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []:
        where = f'{SKILLS_DIR}/{folder.name}'
        files = {}
        for path in sorted(p for p in folder.rglob('*') if p.is_file()):
            rel = path.relative_to(folder).as_posix()
            if '__pycache__' in rel or rel.endswith('.pyc'):
                continue
            if len(path.relative_to(folder).parts) > 2:
                found.append(f'{where}/{rel}: keep files one level below SKILL.md')
            try:
                files[rel] = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                found.append(f'{where}/{rel}: a skill ships text only')
        if 'SKILL.md' not in files:
            found.append(f'{where}: has no SKILL.md')
            continue
        check_skill(folder.name, files['SKILL.md'], where, found)
        skills[folder.name] = files
    return skills


def check_skill(name: str, text: str, where: str, found: list[str]) -> None:
    if not SKILL_NAME.match(name) or len(name) > 64:
        found.append(f'{where}: the folder name must be lowercase words joined by single hyphens, '
                     'at most 64 characters')
    if 'claude' in name or 'anthropic' in name or name in RESERVED:
        found.append(f'{where}: the name may not contain claude or anthropic, or be {" or ".join(RESERVED)}')
    try:
        fields, body = frontmatter(text)
    except ValueError as error:
        found.append(f'{where}/SKILL.md: {error}')
        return
    extra = sorted(set(fields) - set(SKILL_KEYS))
    if extra:
        found.append(f'{where}/SKILL.md: frontmatter may hold only {", ".join(SKILL_KEYS)}, '
                     f'not {", ".join(extra)}')
    if fields.get('name') != name:
        found.append(f'{where}/SKILL.md: name must equal the folder name, {name}')
    description = fields.get('description', '')
    if not description:
        found.append(f'{where}/SKILL.md: needs a description, which is all that triggers it')
    if len(description) > MAX_DESCRIPTION:
        found.append(f'{where}/SKILL.md: the description is {len(description)} characters '
                     f'(limit {MAX_DESCRIPTION})')
    if '<' in description or '>' in description:
        found.append(f'{where}/SKILL.md: the description may not hold angle brackets')
    if description and 'Use when' not in description:
        found.append(f'{where}/SKILL.md: the description says when to use it, with "Use when"')
    if body.count('\n') > MAX_SKILL_LINES:
        found.append(f'{where}/SKILL.md: the body is over {MAX_SKILL_LINES} lines')
    if '\\' in re.sub(r'`[^`]*`', '', body).replace('\\\n', ''):
        found.append(f'{where}/SKILL.md: paths use forward slashes')


def load_subagents(root: pathlib.Path, found: list[str]) -> dict[str, dict[str, str]]:
    """Every subagent, rendered for each app that reads them."""
    agents: dict[str, dict[str, str]] = {}
    base = root / SUBAGENTS_DIR
    for path in sorted(base.glob('*.md')) if base.is_dir() else []:
        if path.name == 'README.md':
            continue
        where = f'{SUBAGENTS_DIR}/{path.name}'
        try:
            fields, body = frontmatter(path.read_text(encoding='utf-8'))
        except ValueError as error:
            found.append(f'{where}: {error}')
            continue
        name = fields.get('name', '')
        if name != path.stem or not SKILL_NAME.match(name):
            found.append(f'{where}: name must equal the file name, in lowercase words and hyphens')
        if not fields.get('description'):
            found.append(f'{where}: needs a description, which is what delegation reads')
        extra = sorted(set(fields) - set(SUBAGENT_KEYS))
        if extra:
            found.append(f'{where}: frontmatter may hold only {", ".join(SUBAGENT_KEYS)}, not {", ".join(extra)}')
        tools = [tool.strip() for tool in fields.get('tools', '').split(',') if tool.strip()]
        unknown = [tool for tool in tools if tool not in TOOLS]
        if unknown:
            found.append(f'{where}: unknown tools {", ".join(unknown)}; use {", ".join(TOOLS)}')
            continue
        agents[path.stem] = render_subagent(name, fields.get('description', ''), tools, body)
    return agents


def render_subagent(name: str, description: str, tools: list[str], body: str) -> dict[str, str]:
    """One subagent as Claude Code, Copilot and Codex each read it."""
    claude = ['---', f'# {OWNED}', f'name: {name}', f'description: {yaml_string(description)}']
    copilot = ['---', f'# {OWNED}', f'name: {name}', f'description: {yaml_string(description)}']
    if tools:
        claude.append('tools: ' + ', '.join(n for tool in tools for n in TOOLS[tool]))
        copilot.append('tools: ' + json.dumps(tools))
    claude += ['---', '', body]
    copilot += ['---', '', body]
    codex = '\n'.join([f'# {OWNED}', f'name = {toml_string(name)}',
                       f'description = {toml_string(description)}',
                       f'developer_instructions = {toml_block(body)}', ''])
    return {'claude': '\n'.join(claude), 'copilot': '\n'.join(copilot), 'codex': codex}


def bundle(root: pathlib.Path) -> tuple[dict, list[str]]:
    """The bundle, and every problem with its sources."""
    found: list[str] = []
    guard = (root / GUARD_FILE).read_text(encoding='utf-8')
    if OWNED not in guard:
        found.append(f'{GUARD_FILE}: must carry the line "# {OWNED}", which marks the installed copy')
    kit = {
        '//': 'Everything the home kit installs besides the rules, rendered by .github/scripts/kit.py from '
              'kit/guard.py, kit/skills/ and kit/subagents/. Never edit this file by hand.',
        # 2 dropped the knowledge facts (ADR-0023); the installer reads this one format.
        'format': 2,
        'guard': guard,
        'skills': load_skills(root, found),
        'subagents': load_subagents(root, found),
    }
    text = json.dumps(kit, ensure_ascii=False)
    for name in sorted(set(NAMED.findall(text)) - set(NAMEABLE)):
        found.append(f'the kit names tannergolden/{name}, which is not a public repository')
    if DASHES.search(text):
        found.append('the kit holds an en or em dash; use a comma, colon, parentheses or a spaced hyphen')
    return kit, found


def render_kit(root: pathlib.Path) -> str:
    kit, _ = bundle(root)
    return json.dumps(kit, indent=2, ensure_ascii=False) + '\n'


def problems(root: pathlib.Path) -> list[str]:
    return bundle(root)[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--check', action='store_true', help='list every problem in the sources')
    parser.add_argument('--root', type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    found = problems(args.root)
    for line in found:
        print(f'error: {line}', file=sys.stderr)
    if not args.check and not found:
        print(render_kit(args.root), end='')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
