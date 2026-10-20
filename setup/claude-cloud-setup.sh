#!/usr/bin/env bash
# Install the universal rules into a Claude Code cloud session.
#
# WHY THIS EXISTS. A Claude cloud session starts in a fresh container, so
# nothing the home kit installed on your machines is there. Pasted into the
# cloud environment's setup script, this downloads one pinned release's home
# file, kit and installer, checks each against its pin, and writes
# ~/.claude/CLAUDE.md with the rules, plus Claude Code's share of the kit:
# the guard hook, the skills and the subagents.
# Copy it with its pins filled in: run `make cloud-setup VERSION=vX.Y.Z` in
# the hub, which prints this file ready to paste.
#
# A kit that cannot be downloaded or misses its pin is left out, and the
# rules still install. An empty kit pin means a release from before the kit.
#
# IT NEVER FAILS THE SESSION. A setup script that exits non-zero stops the
# session from starting, so every failure here prints a notice and the
# script still exits 0. The session then runs on each repository's own
# AGENTS.md alone, which carries the same rules.

VERSION='@VERSION@'
HOME_SHA256='@HOME_SHA256@'
INSTALL_SHA256='@INSTALL_SHA256@'
KIT_SHA256='@KIT_SHA256@'
BASE="${INTELLIGENCE_BASE:-https://raw.githubusercontent.com/tannergolden/intelligence}"

notice() {
  printf 'intelligence: %s\n' "$*" >&2
}

sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | cut -d ' ' -f 1
  else
    shasum -a 256 "$1" | cut -d ' ' -f 1
  fi
}

fetch() {
  curl -fsSL --retry 2 --max-time 30 "$1" -o "$2"
}

main() {
  case "$VERSION" in
    @*) notice 'no release is pinned here yet; run make cloud-setup VERSION=vX.Y.Z in the hub'; return 0 ;;
  esac
  for tool in curl python3; do
    command -v "$tool" >/dev/null 2>&1 || { notice "$tool is not installed, so the rules were not installed"; return 0; }
  done
  dir="$(mktemp -d)" || { notice 'could not make a scratch folder'; return 0; }
  trap 'rm -rf "$dir"' EXIT
  fetch "$BASE/$VERSION/home/intelligence.md" "$dir/intelligence.md" \
    || { notice "could not download the home file for $VERSION"; return 0; }
  fetch "$BASE/$VERSION/scripts/install.py" "$dir/install.py" \
    || { notice "could not download the installer for $VERSION"; return 0; }
  [ "$(sha256 "$dir/intelligence.md")" = "$HOME_SHA256" ] \
    || { notice "the home file for $VERSION does not match its pin, so nothing was installed"; return 0; }
  [ "$(sha256 "$dir/install.py")" = "$INSTALL_SHA256" ] \
    || { notice "the installer for $VERSION does not match its pin, so nothing was installed"; return 0; }
  set -- --home-file "$dir/intelligence.md" --cloud
  case "$KIT_SHA256" in
    '' | @*) ;;
    *)
      if ! fetch "$BASE/$VERSION/home/kit.json" "$dir/kit.json"; then
        notice "could not download the kit for $VERSION, so only the rules were installed"
      elif [ "$(sha256 "$dir/kit.json")" != "$KIT_SHA256" ]; then
        notice "the kit for $VERSION does not match its pin, so only the rules were installed"
      else
        set -- "$@" --kit-file "$dir/kit.json"
      fi
      ;;
  esac
  python3 "$dir/install.py" install "$@" \
    || notice 'the installer reported a problem; see above'
}

main || true
exit 0
