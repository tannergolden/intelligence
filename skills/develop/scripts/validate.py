#!/usr/bin/env python3
"""Check a skill, an agent, a team roster or an agent library against the format every app accepts.

Gate 1 of the develop skill: what is true of a skill or an agent in every
repository. A repository's own rules (its frontmatter schema, its tag
vocabulary, its layout) stay with that repository's own checks, which its
AGENTS.md names; run those too.

Run it:

    python3 scripts/validate.py skill <skill folder> [--agents <agent home>]...
    python3 scripts/validate.py agent <agent file>
    python3 scripts/validate.py team <roster file> [--agents <agent home>]...
    python3 scripts/validate.py library <agent home>...

An agent home is a folder of agent specs, with a roster for each team: a
file whose frontmatter lists `members`. Add --json for one JSON object on
stdout, and --allow-em-dash in a repository whose rules allow the
character. It exits 1 on any error, 2 on bad usage, and 0 otherwise;
warnings never fail it. It reads files and writes nothing.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import pathlib
import re
import sys

SKILL_KEYS = ('name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools')
NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
RESERVED = ('synced', 'anthropic-skills')
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_BODY_LINES = 500
SKILL_FILES = ('License.txt', 'Changelog.md')
SKILL_FOLDERS = ('assets', 'references', 'templates')
SKIPPED = ('__pycache__',)
DASHES = re.compile('[\u2013\u2014\u2015]')
STAR = '\u2605 '
CAPABILITIES = ('read', 'search', 'edit', 'execute', 'web', 'agent')
APP_TOOLS = ('Read', 'Write', 'Edit', 'MultiEdit', 'NotebookEdit', 'Bash', 'Grep', 'Glob', 'WebFetch', 'WebSearch',
             'Agent', 'Task')
PRE_APPROVES_WRITES = re.compile(r'\b(Write|Edit|MultiEdit|NotebookEdit|Bash|edit|execute)\b')
AGENT_SECTIONS = ('Identity', 'Role & Objective', 'Inputs', 'Method', 'Output contract', 'Examples', 'Boundaries',
                  'Recovery', 'Non-negotiables')
IDENTITY_LINES = ('Name', 'Persona', 'Voice')
CURRENT_VERSION = re.compile(r'^## Current Version[ \t]*\n\s*\*\*`(?P<version>[^`]+)`\*\*', re.M)
FENCE = re.compile(r'^\s*(?:```|~~~)')
KEY = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*)|[ \t]*)$')
SUB_KEY = re.compile(r'^[ \t]+([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*)|[ \t]*)$')


class FrontmatterError(ValueError):
    """Frontmatter that no YAML reader would read the way it looks."""


# --- reading frontmatter: the subset of YAML skill and agent files use -------


def split_frontmatter(text: str) -> tuple[str, str]:
    """The frontmatter between a first-line `---` and the next `---` line, and the body after it."""
    text = text.replace('\r\n', '\n')
    if not text.startswith('---\n'):
        raise FrontmatterError('must open with --- on its first line')
    lines = text.split('\n')
    for index in range(1, len(lines)):
        if lines[index] in ('---', '...'):
            return '\n'.join(lines[1:index]), '\n'.join(lines[index + 1:])
    raise FrontmatterError('has no closing --- line for its frontmatter')


def split_outside_quotes(text: str, separator: str) -> list[str]:
    """`text` cut at each `separator` that is outside quotes and brackets."""
    parts, current, quote, depth = [], [], '', 0
    for char in text:
        if quote:
            current.append(char)
            if char == quote:
                quote = ''
        elif char in '"\'':
            quote = char
            current.append(char)
        elif char in '[{':
            depth += 1
            current.append(char)
        elif char in ']}':
            depth -= 1
            current.append(char)
        elif char == separator and depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(char)
    parts.append(''.join(current))
    return parts


def scalar(value: str) -> object:
    """One YAML value written on one line: a quoted or plain string, or a flow list or map."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except ValueError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if value.startswith('['):
        if not value.endswith(']'):
            raise FrontmatterError(f'has an unclosed list: {value[:40]}')
        return [scalar(item) for item in split_outside_quotes(value[1:-1], ',') if item.strip()]
    if value.startswith('{'):
        if not value.endswith('}'):
            raise FrontmatterError(f'has an unclosed map: {value[:40]}')
        out: dict[str, object] = {}
        for item in split_outside_quotes(value[1:-1], ','):
            if not item.strip():
                continue
            key, *rest = split_outside_quotes(item, ':')
            if not rest:
                raise FrontmatterError(f'has a map entry with no value: {item.strip()[:40]}')
            out[str(scalar(key))] = scalar(':'.join(rest))
        return out
    if ' #' in value:
        value = value.split(' #', 1)[0].rstrip()
    return value


def parse_frontmatter(block: str) -> dict[str, object]:
    """The keys of a frontmatter block, with folded and literal scalars, lists and one level of maps."""
    fields: dict[str, object] = {}
    lines = block.split('\n')
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line[:1] in (' ', '\t'):
            raise FrontmatterError(f'has an indented line with no key above it: {line.strip()[:40]}')
        match = KEY.match(line)
        if not match:
            raise FrontmatterError(f'has a line that is not "key: value": {line[:40]}')
        key, value = match.group(1), (match.group(2) or '').strip()
        if key in fields:
            raise FrontmatterError(f'sets {key} twice')
        nested = []
        while index < len(lines) and (lines[index][:1] in (' ', '\t') or not lines[index].strip()):
            nested.append(lines[index])
            index += 1
        content = [entry for entry in nested if entry.strip()]
        if value in ('>', '>-', '>+'):
            fields[key] = ' '.join(entry.strip() for entry in content)
        elif value in ('|', '|-', '|+'):
            fields[key] = '\n'.join(entry.strip() for entry in content)
        elif value:
            words = [value] + [entry.strip() for entry in content]
            fields[key] = scalar(' '.join(words)) if content else scalar(value)
        elif not content:
            fields[key] = ''
        elif content[0].strip()[:1] in ('[', '{'):
            # A flow list or map laid out over several lines, as Prettier writes a long one.
            fields[key] = scalar(' '.join(entry.strip() for entry in content))
        elif all(entry.strip() == '-' or entry.strip().startswith('- ') for entry in content):
            fields[key] = [scalar(entry.strip()[2:]) for entry in content]
        else:
            sub: dict[str, object] = {}
            for entry in content:
                found = SUB_KEY.match(entry)
                if not found:
                    raise FrontmatterError(f'has a line under {key} that is not "key: value": {entry.strip()[:40]}')
                sub[found.group(1)] = scalar(found.group(2) or '')
            fields[key] = sub
    return fields


def read_frontmatter(path: pathlib.Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding='utf-8')
    block, body = split_frontmatter(text)
    return parse_frontmatter(block), body


# --- the report ---------------------------------------------------------------------


@dataclasses.dataclass
class Report:
    errors: list[str] = dataclasses.field(default_factory=list)
    warnings: list[str] = dataclasses.field(default_factory=list)
    checked: int = 0

    def error(self, where: object, message: str) -> None:
        self.errors.append(f'{where}: {message}')

    def warn(self, where: object, message: str) -> None:
        self.warnings.append(f'{where}: {message}')


def text_of(path: pathlib.Path) -> str | None:
    """A file's text, or None when it is not UTF-8 text."""
    raw = path.read_bytes()
    if b'\0' in raw:
        return None
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return None


def check_dashes(path: pathlib.Path, text: str, report: Report, allow_dash: bool) -> None:
    if allow_dash:
        return
    for number, line in enumerate(text.splitlines(), 1):
        if DASHES.search(line):
            report.error(f'{path}:{number}', 'holds an em dash, en dash or horizontal bar; use a comma, colon, '
                                             'parentheses or a spaced hyphen, or pass --allow-em-dash')
            return


def headings(body: str) -> list[str]:
    """Every `## ` heading outside code fences."""
    found, fenced = [], False
    for line in body.split('\n'):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith('## '):
            found.append(line[3:].strip())
    return found


# --- agents, teams and libraries --------------------------------------------------------


def slug(title: str) -> str:
    title = title[len(STAR):] if title.startswith(STAR) else title
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


@dataclasses.dataclass
class Spec:
    path: pathlib.Path
    fields: dict[str, object]

    @property
    def title(self) -> str:
        return str(self.fields.get('title', ''))


def collect(homes: list[pathlib.Path], report: Report) -> tuple[list[Spec], list[Spec]]:
    """The agents and the rosters in every home: a roster lists `members`, an agent has a title and a name."""
    agents, rosters = [], []
    for home in homes:
        if not home.is_dir():
            report.error(home, 'is not a folder of agent specs')
            continue
        for path in sorted(home.rglob('*.md')):
            if any(part.startswith('.') or part in SKIPPED for part in path.relative_to(home).parts):
                continue
            try:
                fields, _ = read_frontmatter(path)
            except (FrontmatterError, UnicodeDecodeError):
                continue  # not an agent spec; the agent check reports a broken one it is pointed at
            if 'members' in fields:
                rosters.append(Spec(path, fields))
            elif 'title' in fields and 'name' in fields:
                agents.append(Spec(path, fields))
    return agents, rosters


def check_agent(path: pathlib.Path, report: Report, allow_dash: bool = False) -> None:
    report.checked += 1
    text = text_of(path)
    if text is None:
        report.error(path, 'is not UTF-8 text')
        return
    try:
        block, body = split_frontmatter(text)
        fields = parse_frontmatter(block)
    except FrontmatterError as error:
        report.error(path, f'frontmatter {error}')
        return
    for key in ('title', 'name', 'description'):
        if not str(fields.get(key, '')).strip():
            report.error(path, f'needs a {key} in its frontmatter')
    title = str(fields.get('title', ''))
    if title and path.stem not in (title, slug(title)):
        report.error(path, f'the file is named for its title: {slug(title)}.md, or "{title}.md" where the '
                           "repository's rules name files that way")
    description = str(fields.get('description', ''))
    if description and not description.startswith('Dispatch this agent'):
        report.warn(path, 'a routing description starts "Dispatch this agent when ..." or "Dispatch this agent to ..."')
    tools = fields.get('tools', '')
    names = tools if isinstance(tools, list) else [tool.strip() for tool in str(tools).split(',')]
    unknown = [str(tool) for tool in names if str(tool).strip() and tool not in CAPABILITIES and tool not in APP_TOOLS]
    if unknown:
        report.warn(path, f'unknown tools {", ".join(unknown)}; use {", ".join(CAPABILITIES)}')
    present = headings(body)
    missing = [section for section in AGENT_SECTIONS if section not in present]
    if missing:
        report.error(path, f'is missing its {", ".join(missing)} section' + ('s' if len(missing) > 1 else ''))
    if 'Identity' in present:
        identity = body.split('## Identity', 1)[1].split('\n## ', 1)[0]
        for label in IDENTITY_LINES:
            if f'**{label}:**' not in identity:
                report.warn(path, f'its Identity block has no **{label}:** line')
    check_dashes(path, text, report, allow_dash)


def check_team(roster: Spec, agents: list[Spec], report: Report, allow_dash: bool = False) -> None:
    report.checked += 1
    path, fields = roster.path, roster.fields
    for key in ('title', 'description', 'lead'):
        if not str(fields.get(key, '')).strip():
            report.error(path, f'a roster needs a {key} in its frontmatter')
    members = fields.get('members')
    if not isinstance(members, list) or not members:
        report.error(path, 'a roster lists its members, as a list of agent titles')
        members = []
    members = [str(member) for member in members]
    lead = str(fields.get('lead', ''))
    if lead and lead not in members:
        report.error(path, f'its lead, {lead}, is not among its members')
    if lead and not lead.startswith(STAR):
        report.error(path, f'its lead, {lead}, is marked with a star: "{STAR}{lead}"')
    starred = [member for member in members if member.startswith(STAR)]
    if len(starred) > 1:
        report.error(path, f'stars {len(starred)} members; only the lead carries the star')
    nearby = {agent.title for agent in agents if agent.path.parent == path.parent}
    known = {agent.title for agent in agents}
    for member in members:
        if member not in nearby and member not in known:
            report.error(path, f'lists {member}, which no agent file in the agent homes is titled')
    text = text_of(path)
    if text is not None:
        check_dashes(path, text, report, allow_dash)


def check_library(homes: list[pathlib.Path], report: Report, allow_dash: bool = False) -> None:
    agents, rosters = collect(homes, report)
    for agent in agents:
        check_agent(agent.path, report, allow_dash)
    for roster in rosters:
        check_team(roster, agents, report, allow_dash)
    titles: dict[str, list[pathlib.Path]] = {}
    names: dict[str, list[pathlib.Path]] = {}
    for agent in agents:
        titles.setdefault(agent.title, []).append(agent.path)
        names.setdefault(str(agent.fields.get('name', '')).lower(), []).append(agent.path)
    for title, paths in sorted(titles.items()):
        if title and len(paths) > 1:
            report.error(paths[1], f'shares its title, {title}, with {paths[0]}; a role is unique across the homes')
    for name, paths in sorted(names.items()):
        if name and len(paths) > 1:
            report.error(paths[1], f'shares its spoken name with {paths[0]}; a name is unique across the homes')


def find_team(team: str, homes: list[pathlib.Path], report: Report) -> tuple[Spec | None, list[Spec]]:
    """The roster titled `team` in the homes, and the agents it names."""
    agents, rosters = collect(homes, Report())
    for roster in rosters:
        if roster.title == team or roster.path.stem == team or slug(roster.title) == slug(team):
            members = [str(member) for member in roster.fields.get('members') or []]
            nearby = [agent for agent in agents if agent.path.parent == roster.path.parent]
            chosen = []
            for member in members:
                match = next((a for a in nearby if a.title == member), None) or next(
                    (a for a in agents if a.title == member), None)
                if match is not None:
                    chosen.append(match)
            return roster, chosen
    return None, []


# --- skills ---------------------------------------------------------------------------


def check_skill(folder: pathlib.Path, homes: list[pathlib.Path], report: Report, allow_dash: bool = False) -> None:
    report.checked += 1
    if not folder.is_dir():
        report.error(folder, 'is not a folder')
        return
    manifest = folder / 'SKILL.md'
    files = sorted(path for path in folder.rglob('*')
                   if path.is_file() and not any(part in SKIPPED for part in path.relative_to(folder).parts)
                   and path.suffix not in ('.pyc', '.pyo'))
    for path in files:
        if path.name.lower() == 'skill.md' and path != manifest:
            report.error(path, 'is a second SKILL.md; a skill has one, at its root, and a template manifest is '
                               'named t-SKILL.md')
    if not manifest.is_file():
        report.error(folder, 'has no SKILL.md at its root')
        return
    text = text_of(manifest)
    if text is None:
        report.error(manifest, 'is not UTF-8 text')
        return
    try:
        block, body = split_frontmatter(text)
        fields = parse_frontmatter(block)
    except FrontmatterError as error:
        report.error(manifest, f'frontmatter {error}')
        return

    extra = sorted(set(fields) - set(SKILL_KEYS))
    if extra:
        report.error(manifest, f'frontmatter may hold only {", ".join(SKILL_KEYS)}, not {", ".join(extra)}')
    name = str(fields.get('name', ''))
    if not name:
        report.error(manifest, 'needs a name')
    elif not NAME.match(name) or len(name) > MAX_NAME:
        report.error(manifest, f'the name is lowercase words joined by single hyphens, at most {MAX_NAME} characters')
    if name and name != folder.name:
        report.error(manifest, f'the name, {name}, equals the folder name, {folder.name}')
    if 'claude' in name or 'anthropic' in name or name in RESERVED:
        report.error(manifest, f'the name may not contain claude or anthropic, or be {" or ".join(RESERVED)}')
    description = fields.get('description', '')
    if not isinstance(description, str) or not description.strip():
        report.error(manifest, 'needs a description, which is all that decides whether it triggers')
        description = ''
    if len(description) > MAX_DESCRIPTION:
        report.error(manifest, f'the description is {len(description)} characters (limit {MAX_DESCRIPTION})')
    if '<' in description or '>' in description:
        report.error(manifest, 'the description may not hold angle brackets')
    if description and 'Use when' not in description:
        report.error(manifest, 'the description says when to use the skill, with "Use when"')
    if not str(fields.get('license', '')).strip():
        report.error(manifest, 'needs a license, matching License.txt')
    compatibility = fields.get('compatibility', '')
    if compatibility and len(str(compatibility)) > MAX_COMPATIBILITY:
        report.error(manifest, f'compatibility is at most {MAX_COMPATIBILITY} characters')
    metadata = fields.get('metadata')
    version = ''
    if not isinstance(metadata, dict):
        report.error(manifest, 'needs a metadata map with its version, such as metadata: {"version": "01.00.00"}')
    else:
        version = str(metadata.get('version', ''))
        if not version:
            report.error(manifest, 'metadata carries the version, which equals the Changelog\'s Current Version')
    tools = fields.get('allowed-tools', '')
    tools_text = ', '.join(map(str, tools)) if isinstance(tools, list) else str(tools)
    if PRE_APPROVES_WRITES.search(tools_text):
        report.warn(manifest, 'allowed-tools pre-approves a tool that writes or runs commands; list read-only tools '
                              'at most')

    if body.count('\n') > MAX_BODY_LINES:
        report.error(manifest, f'the body is over {MAX_BODY_LINES} lines; move detail into references/')
    if '\\' in re.sub(r'`[^`]*`', '', body).replace('\\\n', ''):
        report.error(manifest, 'paths use forward slashes')
    sections = headings(body)
    if 'Boundaries' not in sections:
        report.error(manifest, 'the body needs a ## Boundaries section')
    if 'Bootstrap' in sections and name != 'develop':
        report.error(manifest, 'a ## Bootstrap section belongs to develop alone')

    for required in SKILL_FILES:
        if not (folder / required).is_file():
            report.error(folder, f'needs {required}')
    for wanted in SKILL_FOLDERS:
        if not (folder / wanted).is_dir():
            report.warn(folder, f'has no {wanted}/ folder')
    changelog = folder / 'Changelog.md'
    if changelog.is_file() and version:
        found = CURRENT_VERSION.search(text_of(changelog) or '')
        if found is None:
            report.error(changelog, 'needs a "## Current Version" line with the version in bold code, as **`01.00.00`**')
        elif found.group('version') != version:
            report.error(changelog, f'its Current Version, {found.group("version")}, differs from metadata.version, '
                                    f'{version}; one version, every site')

    for path in files:
        relative = path.relative_to(folder)
        if len(relative.parts) > 2:
            report.error(path, 'keep files at most one folder below SKILL.md')
        content = text_of(path)
        if content is None:
            report.warn(path, 'is not UTF-8 text, which some apps refuse in a skill')
        else:
            check_dashes(path, content, report, allow_dash)

    vendored = folder / 'agents'
    if vendored.is_dir():
        check_library([vendored], report, allow_dash)
    team = metadata.get('team', '') if isinstance(metadata, dict) else ''
    if team:
        search = ([vendored] if vendored.is_dir() else []) + homes
        roster, _ = find_team(str(team), search, report) if search else (None, [])
        if roster is None:
            report.error(manifest, f'metadata.team names {team}, which no roster in agents/ or in an agent home '
                                   'given with --agents defines')
        elif not roster.fields.get('members'):
            report.error(roster.path, f'the roster for {team} lists no members, so the team is not staffed')


# --- command line ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('kind', choices=('skill', 'agent', 'team', 'library'), help='what to check')
    parser.add_argument('paths', nargs='+', type=pathlib.Path, help='the skill folder, agent file, roster or homes')
    parser.add_argument('--agents', action='append', default=[], type=pathlib.Path, metavar='HOME',
                        help='an agent home to resolve teams and members in; repeat for more')
    parser.add_argument('--allow-em-dash', action='store_true', help='for repositories whose rules allow the character')
    parser.add_argument('--json', action='store_true', help='print one JSON object instead of lines')
    args = parser.parse_args(argv)
    report = Report()
    try:
        if args.kind == 'skill':
            for folder in args.paths:
                check_skill(folder, args.agents, report, args.allow_em_dash)
        elif args.kind == 'agent':
            for path in args.paths:
                check_agent(path, report, args.allow_em_dash)
        elif args.kind == 'team':
            for path in args.paths:
                fields, _ = read_frontmatter(path)
                agents, _ = collect([path.parent, *args.agents], report)
                check_team(Spec(path, fields), agents, report, args.allow_em_dash)
        else:
            check_library(args.paths, report, args.allow_em_dash)
    except (OSError, FrontmatterError, UnicodeDecodeError) as error:
        report.error(getattr(error, 'filename', None) or args.paths[0], str(error))
    if args.json:
        print(json.dumps({'errors': report.errors, 'warnings': report.warnings, 'checked': report.checked}, indent=2))
    else:
        for line in report.errors:
            print(f'error: {line}')
        for line in report.warnings:
            print(f'warning: {line}')
        print(f'{len(report.errors)} errors, {len(report.warnings)} warnings, {report.checked} checked')
    return 1 if report.errors else 0


if __name__ == '__main__':
    sys.exit(main())
