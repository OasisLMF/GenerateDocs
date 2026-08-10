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
    """Real version dirs = immediate subdirs (with an index.html) other than the ``latest`` alias,
    newest-first (version-aware). ``latest`` is a redirect, not a version, so it never appears."""
    vers = [d for d in os.listdir(root)
            if d != "latest" and os.path.isdir(os.path.join(root, d))
            and os.path.exists(os.path.join(root, d, "index.html"))]
    return sorted(vers, key=_version_key, reverse=True)


def _write_redirect(path, target):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('<!doctype html><meta charset="utf-8">'
                 f'<meta http-equiv="refresh" content="0; url={target}">'
                 '<title>Oasis documentation</title>'
                 f'<a href="{target}">Continue to the Oasis documentation</a>')


def write_versions_index(root, latest_version=None):
    """Write versions.json and the redirects. ``latest`` is an alias (a redirect), never a copy:
    the site root and ``/latest/`` both redirect to ``latest_version`` (or, if not given, the
    newest version by number). Returns the real version list."""
    vers = _list_versions(root)
    with open(os.path.join(root, "versions.json"), "w", encoding="utf-8") as fh:
        json.dump([{"label": v.lstrip("v"), "path": v} for v in vers], fh, indent=2)
    target = latest_version if (latest_version in vers) else (vers[0] if vers else None)
    if target:
        _write_redirect(os.path.join(root, "index.html"), f"{target}/index.html")
        # /latest/ is a stable bookmarkable URL implemented as a redirect stub (not a duplicate site)
        latest_dir = os.path.join(root, "latest")
        if os.path.isdir(latest_dir):
            shutil.rmtree(latest_dir)
        os.makedirs(latest_dir, exist_ok=True)
        _write_redirect(os.path.join(latest_dir, "index.html"), f"../{target}/index.html")
    return vers, target


def inject_version_switcher(root, latest=None):
    """(Re)inject the sidebar version dropdown into every page of every version dir.

    Idempotent: strips any previously-injected switcher first, so re-running after a new version
    is added refreshes every version's dropdown with the full list. Options are baked from the
    current version list; the option for ``latest`` (default: the newest version) is marked
    "(latest)". The shared version-switch.js (written at ``root``) wires up navigation with the
    404 fallback.
    """
    vers = _list_versions(root)
    if latest not in vers:
        latest = vers[0] if vers else None
    with open(os.path.join(root, "version-switch.js"), "w", encoding="utf-8") as fh:
        fh.write(SWITCHER_JS)
    # inject right before Furo's sidebar search form (present regardless of the brand markup,
    # so this also works on the legacy site's older template)
    anchor = '<form class="sidebar-search-container"'
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
                    f'{v.lstrip("v")}{" (latest)" if v == latest else ""}</option>' for v in vers)
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
                    s = s.replace(anchor, widget + anchor, 1)
                    open(fp, "w", encoding="utf-8").write(s)
                    injected += 1
    return vers, injected


# -- Federated search -------------------------------------------------------
# Each component is its own Sphinx build with its own searchindex.js, so the aggregated site
# has no single index. This makes the top-level search page federate: it fetches every
# component's index, searches them together, and lists results grouped by component. Every
# page's sidebar search box is repointed here so search from anywhere covers the whole site.
# (Fetching indexes needs the site served, like Sphinx's own search — no worse than before.)
SEARCH_ALL_JS = """\
// Federated search across all component Sphinx indexes of this site version.
(function () {
  var AREAS = __AREAS__;                       // [{label, path}]  path "" = the landing
  var params = new URLSearchParams(location.search);
  var q = (params.get("q") || "").trim();
  var box = document.querySelector('input[name="q"]');
  if (box) box.value = q;
  var out = document.getElementById("search-results");
  if (!out) return;
  if (!q) { out.innerHTML = "<p>Type a query above to search all Oasis documentation.</p>"; return; }
  out.innerHTML = "<p>Searching\\u2026</p>";
  var words = q.toLowerCase().split(/\\s+/).filter(Boolean);

  function parseIndex(txt) {
    var s = txt.trim();
    return JSON.parse(s.slice(s.indexOf("(") + 1, s.lastIndexOf(")")));
  }
  function matchTerms(terms, w, weight, scores) {
    for (var t in terms) {
      if (t.indexOf(w) === 0 || w.indexOf(t) === 0) {          // approx-stem: either is a prefix
        var v = terms[t]; v = Array.isArray(v) ? v : [v];
        for (var i = 0; i < v.length; i++) scores[v[i]] = (scores[v[i]] || 0) + weight;
      }
    }
  }
  function searchArea(area, idx) {
    var scores = {}, dn = idx.docnames || [], ti = idx.titles || [], fn = idx.filenames || [];
    words.forEach(function (w) {
      for (var i = 0; i < dn.length; i++) {
        if (dn[i].toLowerCase().indexOf(w) >= 0 || (ti[i] || "").toLowerCase().indexOf(w) >= 0)
          scores[i] = (scores[i] || 0) + 8;                    // title / path hit
      }
      matchTerms(idx.titleterms || {}, w, 5, scores);
      matchTerms(idx.terms || {}, w, 2, scores);
    });
    var pre = area.path ? area.path + "/" : "";
    return Object.keys(scores).map(function (i) {
      return { area: area.label, score: scores[i],
               title: ti[i] || dn[i], url: pre + dn[i] + ".html",
               // Sphinx ships the page source under _sources/<filename>.txt — used for the snippet
               src: fn[i] ? pre + "_sources/" + fn[i] + ".txt" : null };
    });
  }

  // strip the noisiest reST/MyST markup so the excerpt reads as prose
  function clean(t) {
    return t
      .replace(/:[a-z]+:`([^`]+)`/gi, "$1")      // :ref:`text` -> text
      .replace(/^\\s*\\.\\.[ \\t].*$/gm, " ")       // directive lines (.. figure:: …)
      .replace(/^[=~^#*_-]{2,}\\s*$/gm, " ")       // section underline rows
      .replace(/[`*]/g, "")                       // stray backticks / emphasis stars
      .replace(/\\s+/g, " ").trim();
  }
  // a short context excerpt around the first matched word, with the terms highlighted
  function snippet(raw) {
    var text = clean(raw), low = text.toLowerCase(), pos = -1;
    words.forEach(function (w) { var p = low.indexOf(w); if (p >= 0 && (pos < 0 || p < pos)) pos = p; });
    if (pos < 0) return "";
    var start = Math.max(0, pos - 80);
    var ex = text.slice(start, pos + 160).replace(/\\s+/g, " ").trim();
    words.forEach(function (w) {
      var hw = w.replace(/[^a-z0-9]/gi, "");                    // alnum-only → safe in RegExp
      if (hw) ex = ex.replace(new RegExp("(" + hw + ")", "ig"), '<span class="highlighted">$1</span>');
    });
    return (start > 0 ? "\\u2026" : "") + ex + "\\u2026";
  }

  Promise.all(AREAS.map(function (a) {
    var url = (a.path ? a.path + "/" : "") + "searchindex.js";
    return fetch(url).then(function (r) { return r.text(); })
      .then(function (t) { return searchArea(a, parseIndex(t)); })
      .catch(function () { return []; });
  })).then(function (lists) {
    var all = [].concat.apply([], lists).sort(function (a, b) { return b.score - a.score; }).slice(0, 80);
    if (!all.length) { out.innerHTML = "<p>No results found for <strong>" + q + "</strong>.</p>"; return; }
    var html = '<p>' + all.length + ' result(s) for <strong>' + q + '</strong>:</p><ul class="search">';
    all.forEach(function (r, i) {
      html += '<li><a href="' + r.url + '">' + r.title + '</a>' +
              ' <span style="opacity:.6;font-size:.85em">\\u2014 ' + r.area + '</span>' +
              '<div class="context" id="oasis-ctx-' + i + '" style="margin:.15rem 0 .5rem;opacity:.85"></div></li>';
    });
    out.innerHTML = html + "</ul>";
    // fill the excerpts lazily from each page's source
    all.forEach(function (r, i) {
      if (!r.src) return;
      fetch(r.src).then(function (res) { return res.ok ? res.text() : ""; }).then(function (txt) {
        var s = txt && snippet(txt);
        if (s) { var el = document.getElementById("oasis-ctx-" + i); if (el) el.innerHTML = s; }
      }).catch(function () {});
    });
  });
})();
"""


def build_federated_search(site_out, modules):
    """Make the top-level search federate over all component indexes, and repoint every page's
    search box at it. Returns (areas, pages_repointed)."""
    areas = [{"label": "Home", "path": ""}] + \
            [{"label": m.get("title", m["path"]), "path": m["path"]} for m in modules]
    with open(os.path.join(site_out, "search-all.js"), "w", encoding="utf-8") as fh:
        fh.write(SEARCH_ALL_JS.replace("__AREAS__", json.dumps(areas)))

    # rewrite the landing search page to use the federated script instead of Sphinx's per-build one
    sp = os.path.join(site_out, "search.html")
    if os.path.exists(sp):
        s = open(sp, encoding="utf-8").read()
        s = s.replace('<script src="_static/searchtools.js"></script>',
                      '<script src="search-all.js" defer></script>')
        open(sp, "w", encoding="utf-8").write(s)

    # point every page's sidebar search box at the site-root federated search page
    action_re = re.compile(r'(<form class="sidebar-search-container"[^>]*\baction=")[^"]*search\.html(")')
    repointed = 0
    for dirpath, _dirs, files in os.walk(site_out):
        for f in files:
            if not f.endswith(".html"):
                continue
            fp = os.path.join(dirpath, f)
            page_path = os.path.relpath(fp, site_out).replace(os.sep, "/")
            relroot = "../" * page_path.count("/")
            s = open(fp, encoding="utf-8").read()
            s2, n = action_re.subn(rf'\g<1>{relroot}search.html\g<2>', s)
            if n:
                open(fp, "w", encoding="utf-8").write(s2)
                repointed += 1
    return areas, repointed


_NB_MARKER = "oasis-run-yourself"          # idempotency guard for the injected block
_NB_FRONTMATTER = re.compile(r"file_format:\s*mystnb|kernelspec:")


def _nb_run_block(name, org, repo):
    """The 'Run this tutorial yourself' admonition + notebook download link (HTML)."""
    return (
        f'<div class="admonition tip {_NB_MARKER}">\n'
        f'<p class="admonition-title">Run this tutorial yourself</p>\n'
        f'<p>This page is a Jupyter notebook, executed when the docs are built. '
        f'<a class="reference download internal" download href="{name}.ipynb">'
        f'<code class="xref download docutils literal notranslate">'
        f'<span class="pre">Download&nbsp;{name}.ipynb</span></code></a></p>\n'
        f'<p>Set up an environment and open it in Jupyter:</p>\n'
        f'<div class="highlight"><pre>'
        f'python -m venv venv &amp;&amp; source venv/bin/activate\n'
        f'pip install oasislmf jupyterlab matplotlib\n'
        f'jupyter lab {name}.ipynb</pre></div>\n'
        f'<p>The example data ships in the '
        f'<a class="reference external" href="https://github.com/{org}/{repo}">{repo}</a> '
        f'repository (under <code class="docutils literal notranslate">'
        f'<span class="pre">docs/source/tutorials/</span></code>); tutorials that run a model '
        f'need that model’s data and the loss engine — follow the prerequisites '
        f'described on this page.</p>\n'
        f'</div>\n'
    )


def add_notebook_downloads(built, org):
    """For each executable tutorial notebook, publish a downloadable ``.ipynb`` next to its page
    and inject a 'Run this tutorial yourself' block with the download link.

    Notebooks are authored as MyST-Markdown (``file_format: mystnb``); we convert the source with
    jupytext into a clean, runnable ``.ipynb`` (no build outputs) and drop it beside the rendered
    HTML. Returns the number of notebooks published."""
    try:
        import jupytext
    except ImportError:
        print("  !! jupytext not installed — skipping notebook downloads "
              "(add jupytext to requirements.txt)")
        return 0

    published = 0
    for m, src_dir, out_dir, _ref in built:
        tut_src = os.path.join(src_dir, "tutorials")
        tut_out = os.path.join(out_dir, "tutorials")
        if not os.path.isdir(tut_src) or not os.path.isdir(tut_out):
            continue
        for fn in sorted(os.listdir(tut_src)):
            if not fn.endswith(".md"):
                continue
            md = os.path.join(tut_src, fn)
            head = "".join(open(md, encoding="utf-8").readlines()[:12])
            if not _NB_FRONTMATTER.search(head):     # not an executable notebook (e.g. index.md)
                continue
            name = fn[:-3]
            html = os.path.join(tut_out, name + ".html")
            if not os.path.exists(html):
                continue
            # convert MyST source -> a clean runnable notebook (drop jupytext/myst metadata)
            try:
                nb = jupytext.read(md)
            except Exception as e:                   # noqa: BLE001 - report and carry on
                print(f"  !! could not convert {m['name']}/tutorials/{fn}: {e}")
                continue
            for k in ("jupytext", "file_format"):
                nb.metadata.pop(k, None)
            jupytext.write(nb, os.path.join(tut_out, name + ".ipynb"), fmt="ipynb")
            # inject the download/run block right after the page's <h1> (idempotent)
            s = open(html, encoding="utf-8").read()
            if _NB_MARKER in s:
                published += 1
                continue
            block = _nb_run_block(name, org, m["repo"])
            s2, n = re.subn(r"(</h1>)", r"\1\n" + block, s, count=1)
            if n:
                open(html, "w", encoding="utf-8").write(s2)
            published += 1
    return published


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

    # federate search over all component indexes + repoint every search box at the top-level page
    areas, repointed = build_federated_search(site_out, modules)
    print(f"federated search: {len(areas)} area(s); repointed search box on {repointed} pages")

    # publish a downloadable .ipynb for each executable tutorial + a 'run it yourself' block
    nbs = add_notebook_downloads(built, org)
    print(f"tutorial notebooks: published {nbs} downloadable .ipynb")

    # versioned publishing: write versions.json + root redirect, then (re)inject the sidebar
    # version selector across every version so each dropdown lists the full set
    if args.deploy_version:
        vers, target = write_versions_index(args.output, args.deploy_version if args.latest else None)
        _, n = inject_version_switcher(args.output, latest=target)
        print(f"version selector: {vers} (latest={target}) — injected into {n} pages; "
              f"root and /latest/ redirect to {target}")

    print("\n===== summary =====")
    for name, status, warns, ref in results:
        print(f"  {name:12} {status:8} warnings={warns if warns is not None else '-':<4} ref={ref}")
    failed = [r for r in results if r[1] != "OK"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
