#!/usr/bin/env python3
"""Check the links in an assembled Oasis documentation site.

Two different problems, so two checks:

**Internal** — every in-site link resolves to a file that exists in the tree. This is the
one that matters on every build: the orchestrator rewrites cross-component links to
page-relative paths, and a page moving or being renamed in one component silently breaks
links from another. Offline, deterministic, and cheap, so it can gate.

**External** — every ``http(s)`` URL still answers. Needs the network, depends on third
parties, and produces false alarms (rate limits, bot blocking), so by default it reports
without failing; pass ``--fail-on-external`` if you want it to.

Sphinx's own ``linkcheck`` builder works per-project on *source*, so it cannot see the
assembled tree or the rewritten cross-component links. Hence this.

Usage::

    python check_links.py --site build/html              # both checks
    python check_links.py --site build/html --internal-only
    python check_links.py --site build/html --summary $GITHUB_STEP_SUMMARY
"""
import argparse
import collections
import concurrent.futures
import os
import re
import sys
import urllib.error
import urllib.request

# Not checkable, rather than broken:
#   localhost / 127.0.0.1  service UIs in deployment examples (RabbitMQ, Flower)
#   *.example.com          placeholder identity providers in auth docs
#   stackoverflow / *.stackexchange.com   403 to anything that looks automated
DEFAULT_IGNORE = [
    r'^https?://localhost(:\d+)?',
    r'^https?://127\.0\.0\.1(:\d+)?',
    r'^https?://[^/]*\bexample\.com',
    r'^https?://stackoverflow\.com/',
    r'^https?://[^/]*\bstackexchange\.com/',
]

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
UA = 'Mozilla/5.0 (compatible; OasisDocsLinkCheck/1.0)'


def iter_pages(site):
    for root, _dirs, files in os.walk(site):
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(root, f)


def collect(site):
    """Return (internal_links, external_urls).

    internal_links: list of (page, href, resolved_path)
    external_urls:  {url: [pages]}
    """
    internal, external = [], collections.defaultdict(list)
    for page in iter_pages(site):
        try:
            html = open(page, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        base = os.path.dirname(page)
        for href in LINK_RE.findall(html):
            if href.startswith(('http://', 'https://')):
                external[href.split('#')[0].rstrip('/')].append(page)
            elif href.startswith(('mailto:', 'data:', 'javascript:', '#', 'tel:')):
                continue
            else:
                target = href.split('#')[0].split('?')[0]
                if not target:
                    continue
                resolved = os.path.normpath(os.path.join(base, target))
                internal.append((page, href, resolved))
    return internal, external


def check_internal(site, internal):
    """Report in-site links whose target is not in the tree."""
    broken = []
    for page, href, resolved in internal:
        if os.path.exists(resolved):
            continue
        # a directory link is served by its index.html
        if os.path.isdir(resolved) and os.path.exists(os.path.join(resolved, 'index.html')):
            continue
        broken.append((os.path.relpath(page, site), href))
    return broken


def check_one(url, timeout):
    req = urllib.request.Request(url, method='GET', headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return url, r.status, ''
    except urllib.error.HTTPError as e:
        return url, e.code, e.reason or ''
    except Exception as e:                                    # DNS, TLS, timeout, refused
        return url, 0, f'{type(e).__name__}: {e}'


def check_external(external, ignore, timeout, workers):
    """HTTP-check each distinct URL once. Returns (failures, checked, skipped)."""
    pats = [re.compile(p) for p in ignore]
    todo = [u for u in external if not any(p.search(u) for p in pats)]
    skipped = len(external) - len(todo)
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for url, code, reason in pool.map(lambda u: check_one(u, timeout), todo):
            if not (200 <= code < 400):
                failures.append((url, code, reason))
    return failures, len(todo), skipped


def report(lines, summary_path):
    text = "\n".join(lines)
    print(text)
    if summary_path:
        with open(summary_path, 'a', encoding='utf-8') as fh:
            fh.write(text + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--site', default=os.path.join('build', 'html'),
                    help='assembled site root (default build/html)')
    ap.add_argument('--internal-only', action='store_true', help='skip the network checks')
    ap.add_argument('--fail-on-external', action='store_true',
                    help='exit non-zero when an external link fails (off by default: '
                         'third-party outages and bot blocking are not our bugs)')
    ap.add_argument('--timeout', type=int, default=20)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--ignore', action='append', default=[],
                    help='extra regex to skip (repeatable); adds to the built-in list')
    ap.add_argument('--summary', help='also append the report here (e.g. $GITHUB_STEP_SUMMARY)')
    args = ap.parse_args()

    if not os.path.isdir(args.site):
        sys.exit(f"no such site directory: {args.site} — build it first (./build.sh)")

    internal, external = collect(args.site)
    out = [f"## Link check — `{args.site}`", ""]

    broken = check_internal(args.site, internal)
    out.append(f"**Internal:** {len(internal)} link(s), {len(broken)} broken")
    if broken:
        out.append("")
        for page, href in broken[:80]:
            out.append(f"- `{page}` -> `{href}`")
        if len(broken) > 80:
            out.append(f"- … and {len(broken) - 80} more")

    ext_failures = []
    if not args.internal_only:
        ext_failures, checked, skipped = check_external(
            external, DEFAULT_IGNORE + args.ignore, args.timeout, args.workers)
        out += ["", f"**External:** {len(external)} distinct URL(s), {checked} checked, "
                f"{skipped} skipped by the ignore list, {len(ext_failures)} failing"]
        if ext_failures:
            out.append("")
            for url, code, reason in sorted(ext_failures, key=lambda x: str(x[1])):
                where = os.path.relpath(external[url][0], args.site)
                out.append(f"- `{code or 'ERR'}` {url}  (e.g. from `{where}`)")
            out += ["", "_Not every failure is rot: 403 usually means the host blocks "
                        "automated requests, and 000 is a network/DNS error._"]

    report(out, args.summary)

    if broken:
        sys.exit(1)                       # deterministic and always a real defect
    if ext_failures and args.fail_on_external:
        sys.exit(1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
