#!/usr/bin/env python3
"""Version-pinned documentation orchestrator for the aggregated Oasis site.

GenerateDocs no longer holds documentation content — each repository owns and builds its own
Sphinx docs. This script reads ``modules.json`` (the pinned manifest), builds each module's
docs from its own repo at the pinned ``ref``, and assembles them under one output tree:

    build/html/                  <- top-level landing (built from ./src)
    build/html/<path>/           <- each module's own docs (e.g. /oasislmf, /platform, /oed)

Two source modes:
  --clone            clone/checkout each repo at its pinned ``ref`` into ./modules/<repo>
                     (the CI / release path — reproducible, version-pinned).
  --use-local BASE   build from existing checkouts at BASE/<repo> (local dev; default BASE is
                     the parent directory of this repo). Uses whatever ref is checked out.

Each module builds in place (inside its cloned repo) so per-repo relative paths and build-time
generators (autoapi, gen_*_reference) resolve correctly.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/{org}/{repo}.git"


def load_manifest():
    with open(os.path.join(HERE, "modules.json"), encoding="utf-8") as fh:
        return json.load(fh)


def sh(cmd, **kw):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def clone_or_update(org, repo, ref, dest):
    """Clone repo at a pinned ref (shallow) into dest, or fetch+checkout if present."""
    url = GH.format(org=org, repo=repo)
    if not os.path.isdir(os.path.join(dest, ".git")):
        sh(["git", "clone", "--depth", "1", "--branch", ref, url, dest])
    else:
        sh(["git", "-C", dest, "fetch", "--depth", "1", "origin", ref])
        sh(["git", "-C", dest, "checkout", "-f", ref])
        sh(["git", "-C", dest, "reset", "--hard", f"origin/{ref}"])
    return dest


def pip_install_editable(repo_dir):
    """Install a module's package editable from its checkout, without touching dependencies.

    For modules marked ``"editable": true`` in the manifest (the org's own packages, e.g.
    oasislmf), the docs must document the *source being built at the pinned ref* — not the
    last PyPI release. Sphinx/autoapi imports the package to resolve version info and inherited
    docstrings, so an ``pip install -e`` from the checkout points those imports at this source.
    ``--no-deps`` links only the package (its dependency tree is already satisfied by
    requirements.txt), keeping it fast and avoiding accidental upgrades.
    """
    print(f"  == editable install: {repo_dir} ==")
    # editable_mode=compat puts the repo on sys.path (like the old develop install) so ALL
    # submodules resolve — the default "strict" finder can miss submodules and clashes with a
    # pre-existing wheel install of the same package.
    proc = subprocess.run([sys.executable, "-m", "pip", "install", "-e", repo_dir, "--no-deps", "-q",
                           "--config-settings", "editable_mode=compat"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout[-2000:] + proc.stderr[-2000:])
        print(f"  !! editable install failed for {repo_dir} (continuing with installed package)")


def build(src_dir, out_dir, keep_going, env_extra=None):
    """Run sphinx-build; return the number of warnings (or None on failure).

    Runs with CWD set to the repo's docs directory (the parent of the Sphinx source dir), so
    per-repo conf.py hooks that write generated pages with paths relative to ``docs/`` (e.g.
    OasisLMF's ``./source/generated_options.rst``) resolve correctly. ``env_extra`` adds
    environment variables (used to pass OASIS_INTERSPHINX_MAP on the second pass).
    """
    src_dir = os.path.abspath(src_dir)
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    cwd = os.path.dirname(src_dir)
    cmd = [sys.executable, "-m", "sphinx", "-b", "html", src_dir, out_dir]
    if keep_going:
        cmd.append("--keep-going")
    env = dict(os.environ, **(env_extra or {}))
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)
    warnings = proc.stderr.count("WARNING") + proc.stdout.count("WARNING")
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout[-3000:] + proc.stderr[-3000:])
        return None
    return warnings


def rewrite_cross_links(site_dir, base_url, module_paths):
    """Rewrite in-site links to page-relative paths, and point the sidebar logo at the landing.

    Two rewrites, applied per HTML file relative to its depth below the site root:

    - Intersphinx emits cross-references as absolute URLs (``base_url`` + ``<path>/…``); rewriting
      them relative to each file makes the assembled tree fully relocatable — cross-links resolve
      when opened as local files (``file://``), from any server, and under a project sub-path.
      Only links whose path starts with a known module path (or the landing ``index.html``) are
      touched.
    - Furo links its sidebar-brand logo to each component's own index; repoint it at the
      aggregated landing (the site-root ``index.html``) so the logo always returns there.
    """
    prefix = base_url
    mods = tuple(module_paths)
    pat = re.compile(r'(href|src)="' + re.escape(prefix) + r'([^"]*)"')
    brand_pat = re.compile(r'(<a\b[^>]*\bclass="sidebar-brand[^"]*"[^>]*\bhref=")[^"]*(")')
    count = 0
    for root, _dirs, files in os.walk(site_dir):
        depth = 0 if os.path.relpath(root, site_dir) == "." else os.path.relpath(root, site_dir).count(os.sep) + 1
        relroot = "../" * depth
        for f in files:
            if not f.endswith(".html"):
                continue
            fp = os.path.join(root, f)
            hits = [0]

            def repl(m):
                path = m.group(2)
                # component cross-links (…/<module>/…) and the landing "home" link (index.html)
                if path.startswith(mods) or path in ("", "index.html"):
                    hits[0] += 1
                    rel = path or "index.html"
                    return f'{m.group(1)}="{relroot}{rel}"'
                return m.group(0)

            with open(fp, encoding="utf-8") as fh:
                s = fh.read()
            s2 = pat.sub(repl, s)
            # point the sidebar logo at the aggregated landing (site-root index)
            s2, n_brand = brand_pat.subn(rf'\g<1>{relroot}index.html\g<2>', s2)
            hits[0] += n_brand
            if hits[0]:
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(s2)
                count += hits[0]
    return count


# -- Versioned publishing ---------------------------------------------------
# A versioned site lives under <root>/<version>/… with a versions.json + a root redirect at
# <root>. Every page carries a sidebar version dropdown; switching navigates to the same page
# under the chosen version, falling back to that version's landing if the page doesn't exist
# there (the 404 fallback). The dropdown options are baked at build time (so the list shows even
# under file://); the fallback needs a served site (a HEAD request), degrading to a direct jump
# under file://.
SWITCHER_JS = """\
(function () {
  document.querySelectorAll('.oasis-version-switch select').forEach(function (sel) {
    var w = sel.closest('.oasis-version-switch');
    var root = w.dataset.root, page = w.dataset.page, cur = w.dataset.version;
    sel.addEventListener('change', function () {
      var v = sel.value;
      if (v === cur) return;
      var target = root + v + '/' + page, landing = root + v + '/index.html';
      // 404 fallback: if the same page is missing in the target version, go to its landing
      fetch(target, { method: 'HEAD' })
        .then(function (r) { location.href = r.ok ? target : landing; })
        .catch(function () { location.href = target; });  // file:// blocks HEAD -> best effort
    });
  });
})();
"""

_SWITCH_BLOCK_RE = re.compile(
    r'<div class="oasis-version-switch".*?</div>\s*<script src="[^"]*version-switch\.js"[^>]*></script>',
    re.S)


def _version_key(name):
    """Natural sort key for a version dir: numeric components descending, ignoring a 'v' prefix
    (so 2.5.10 > 2.5.6 > v2.4.0). Non-numeric tails compare as text."""
    parts = re.split(r"[.\-_]", name.lstrip("vV"))
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parts]


def _list_versions(root):
    """Version dirs = immediate subdirs of root containing an index.html. 'latest' sorts first,
    then the rest newest-first (version-aware)."""
    vers = [d for d in os.listdir(root)
            if os.path.isdir(os.path.join(root, d)) and os.path.exists(os.path.join(root, d, "index.html"))]
    rest = sorted((v for v in vers if v != "latest"), key=_version_key, reverse=True)
    return (["latest"] if "latest" in vers else []) + rest


def write_versions_index(root, default_version):
    """Write versions.json and the root index.html redirect from the version dirs present."""
    vers = _list_versions(root)
    label = lambda v: v if v == "latest" else v.lstrip("v")
    with open(os.path.join(root, "versions.json"), "w", encoding="utf-8") as fh:
        json.dump([{"label": label(v), "path": v} for v in vers], fh, indent=2)
    dflt = default_version if default_version in vers else (vers[0] if vers else default_version)
    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as fh:
        fh.write('<!doctype html><meta charset="utf-8">'
                 f'<meta http-equiv="refresh" content="0; url={dflt}/index.html">'
                 '<title>Oasis documentation</title>'
                 f'<a href="{dflt}/index.html">Continue to the Oasis documentation</a>')
    return vers


def inject_version_switcher(root):
    """(Re)inject the sidebar version dropdown into every page of every version dir.

    Idempotent: strips any previously-injected switcher first, so re-running after a new version
    is added refreshes every version's dropdown with the full list. Options are baked from the
    current version list; the shared version-switch.js (written at ``root``) wires up navigation
    with the 404 fallback.
    """
    vers = _list_versions(root)
    with open(os.path.join(root, "version-switch.js"), "w", encoding="utf-8") as fh:
        fh.write(SWITCHER_JS)
    anchor = '</a><form class="sidebar-search-container"'
    injected = 0
    for ver in vers:
        vdir = os.path.join(root, ver)
        for dirpath, _dirs, files in os.walk(vdir):
            for f in files:
                if not f.endswith(".html"):
                    continue
                fp = os.path.join(dirpath, f)
                page_path = os.path.relpath(fp, vdir).replace(os.sep, "/")
                rel_root = "../" * (page_path.count("/") + 1)          # page -> versioned root
                opts = "".join(
                    f'<option value="{v}"{" selected" if v == ver else ""}>'
                    f'{v if v == "latest" else v.lstrip("v")}</option>' for v in vers)
                widget = (
                    f'<div class="oasis-version-switch" data-version="{ver}" data-page="{page_path}" '
                    f'data-root="{rel_root}" style="padding:.5rem 1rem .25rem">'
                    '<label style="display:block;font-size:.7rem;letter-spacing:.08em;'
                    'text-transform:uppercase;opacity:.7;margin-bottom:.25rem">Version</label>'
                    '<select style="width:100%;padding:.3rem .4rem;border-radius:6px;'
                    'border:1px solid var(--color-background-border);'
                    'background:var(--color-background-primary);'
                    'color:var(--color-foreground-primary);font:inherit">'
                    f'{opts}</select></div>'
                    f'<script src="{rel_root}version-switch.js" defer></script>')
                s = open(fp, encoding="utf-8").read()
                s = _SWITCH_BLOCK_RE.sub("", s)          # strip any previous injection
                if anchor in s:
                    s = s.replace(anchor, "</a>" + widget + '<form class="sidebar-search-container"', 1)
                    open(fp, "w", encoding="utf-8").write(s)
                    injected += 1
    return vers, injected


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--clone", action="store_true",
                     help="clone each repo at its pinned ref into ./modules/<repo>")
    src.add_argument("--use-local", metavar="BASE", nargs="?", const="",
                     help="build from BASE/<repo> checkouts (default: parent of this repo)")
    ap.add_argument("--output", default=os.path.join(HERE, "build", "html"),
                    help="output site directory (default: build/html — the path the deploy CI publishes)")
    ap.add_argument("--keep-going", action="store_true",
                    help="pass --keep-going to sphinx-build and continue past a failing module")
    ap.add_argument("--only", nargs="*", help="build only these module names")
    ap.add_argument("--single-pass", action="store_true",
                    help="skip the second (cross-reference) pass — faster, but intersphinx "
                         "links between components will not resolve")
    ap.add_argument("--absolute-links", action="store_true",
                    help="keep cross-component links as absolute site_base_url URLs instead of "
                         "rewriting them to page-relative (relative is the default, so the site "
                         "is relocatable and works under file://)")
    ap.add_argument("--deploy-version", metavar="NAME",
                    help="assemble into <output>/NAME/ and add a sidebar version selector; "
                         "maintains <output>/versions.json and a root redirect. Run once per "
                         "version (against an <output> that already holds the others) to accumulate.")
    ap.add_argument("--latest", action="store_true",
                    help="with --deploy-version, make the root redirect point at this version")
    args = ap.parse_args()

    manifest = load_manifest()
    org = manifest.get("org", "OasisLMF")
    modules = manifest["modules"]
    if args.only:
        modules = [m for m in modules if m["name"] in args.only]

    # default source mode: use-local from the parent directory
    use_local_base = None
    if not args.clone:
        use_local_base = args.use_local or os.path.abspath(os.path.join(HERE, os.pardir))

    site_base = manifest.get("site_base_url", "").rstrip("/") + "/" if manifest.get("site_base_url") else ""

    # with --deploy-version the aggregated site is assembled into <output>/<version>/, with
    # versions.json + the root redirect living at <output>; otherwise the site is <output> itself.
    site_out = os.path.join(args.output, args.deploy_version) if args.deploy_version else args.output

    # resolve each module's source + output dirs
    built = []            # [(module, src_dir, out_dir, shown_ref)]
    results = []
    for m in modules:
        name, repo, ref = m["name"], m["repo"], m["ref"]
        if args.clone:
            repo_dir = clone_or_update(org, repo, ref, os.path.join(HERE, "modules", repo))
            shown_ref = ref
        else:
            repo_dir = os.path.join(use_local_base, repo)
            shown_ref = "(local checkout)"
        if not os.path.isdir(repo_dir):
            print(f"  !! repo not found: {repo_dir}")
            results.append((name, "MISSING", None, shown_ref))
            continue
        # the org's own packages are installed editable so autoapi/notebooks document THIS source
        if m.get("editable"):
            pip_install_editable(repo_dir)
        built.append((m, os.path.join(repo_dir, m["docs_source"]),
                      os.path.join(site_out, m["path"]), shown_ref))

    # -- pass 1: build every module (produces each objects.inv) --------------
    for m, src_dir, out_dir, shown_ref in built:
        print(f"\n== [pass 1] {m['name']} ==")
        warns = build(src_dir, out_dir, args.keep_going)
        results.append([m["name"], "OK" if warns is not None else "FAILED", warns, shown_ref])
        if warns is None and not args.keep_going:
            print(f"  !! {m['name']} failed; stopping (use --keep-going to continue)")
            break

    # inventory registry of successfully-built modules (for cross-references)
    registry = {}
    for m, _src, out_dir, _ref in built:
        inv = os.path.join(out_dir, "objects.inv")
        if os.path.exists(inv):
            registry[m["name"]] = (f"{site_base}{m['path']}/", os.path.abspath(inv))

    # -- pass 2: rebuild each module with links to the others' inventories ---
    if not args.single_pass and len(registry) > 1:
        for m, src_dir, out_dir, shown_ref in built:
            cross = {k: [v[0], v[1]] for k, v in registry.items() if k != m["name"]}
            if not cross:
                continue
            print(f"\n== [pass 2 · xref] {m['name']} ==")
            warns = build(src_dir, out_dir, args.keep_going,
                          env_extra={"OASIS_INTERSPHINX_MAP": json.dumps(cross)})
            # update the recorded warning count from the resolved build
            for row in results:
                if row[0] == m["name"] and warns is not None:
                    row[1], row[2] = "OK", warns

    # top-level landing page (this repo's slim ./src) — no cross-refs needed
    print("\n== landing (./src) ==")
    landing_warns = build(os.path.join(HERE, "src"), site_out, args.keep_going)
    results.append(["landing", "OK" if landing_warns is not None else "FAILED", landing_warns, "-"])

    # publish the manifest alongside the site
    shutil.copy(os.path.join(HERE, "modules.json"), os.path.join(site_out, "modules.json"))

    # make cross-component links page-relative so the assembled site is relocatable
    if not args.absolute_links and site_base:
        n = rewrite_cross_links(site_out, site_base, [m["path"] + "/" for m in modules])
        print(f"\nrewrote {n} cross-component link(s) to page-relative")

    # versioned publishing: write versions.json + root redirect, then (re)inject the sidebar
    # version selector across every version so each dropdown lists the full set
    if args.deploy_version:
        write_versions_index(args.output, args.deploy_version if args.latest else "latest")
        vers, n = inject_version_switcher(args.output)
        print(f"version selector: {vers} — injected into {n} pages; root redirects to "
              f"{args.deploy_version if args.latest else 'latest'}")

    print("\n===== summary =====")
    for name, status, warns, ref in results:
        print(f"  {name:12} {status:8} warnings={warns if warns is not None else '-':<4} ref={ref}")
    failed = [r for r in results if r[1] != "OK"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
