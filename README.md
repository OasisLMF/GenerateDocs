# GenerateDocs

**Version-pinned orchestrator for the aggregated Oasis documentation site.**

GenerateDocs holds no documentation content. Each Oasis component owns and builds its own
Sphinx docs; this repo pins the version of each and assembles them into one site:

```
build/html/            landing page (built from ./src)
build/html/<path>/     each component's own docs (e.g. /oasislmf, /platform, /oed, /ord …)
```

Cross-component links resolve via intersphinx and are rewritten to page-relative paths, so the
assembled tree is relocatable — it works opened as local files, from any server, or under a
GitHub Pages sub-path.

## Quick start (local dev)

Build the whole site from local checkouts and preview it in a browser.

**1. Clone GenerateDocs and the component repos side by side** (the `--local` build expects
them next to each other):

```bash
mkdir oasis-docs && cd oasis-docs
for repo in GenerateDocs OasisLMF OasisPlatform ODS_Tools \
            ODS_OpenExposureData ODS_OpenResultsData OasisModels; do
  git clone https://github.com/OasisLMF/$repo.git
done
```

**2. Set up a Python environment and install the doc toolchain** (Python 3.10+):

```bash
cd GenerateDocs
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**3. Build the aggregated site from your local checkouts:**

```bash
python orchestrate.py --use-local        # builds all components + landing into build/html/
```

(Or `./build.sh --local`, which creates its own venv and installs `requirements.txt` for you —
handy for a clean one-shot build.)

**4. Preview it in a local server** (recommended — search and the version selector's 404
fallback need a served site, not `file://`):

```bash
python -m http.server 8080 --directory build/html
# then open http://localhost:8080/
```

Iterating on one component is faster with `--only`:

```bash
python orchestrate.py --use-local --only ord ods-tools
```

## What gets built

The manifest [`modules.json`](modules.json) lists every component and the ref to build it from:

```jsonc
{
  "name": "ord", "repo": "ODS_OpenResultsData",
  "ref": "docs/migration",     // pin to a release tag for a released site
  "docs_source": "docs/source",
  "path": "ord",               // published under /ord/
  "title": "Open Results Data (ORD)"
}
```

Edit `modules.json` to add a component or change a pinned version.

Modules that are the org's own importable packages (e.g. `oasislmf`, `ods-tools`) carry
`"editable": true`. Before building such a module the orchestrator runs
`pip install -e <checkout> --no-deps` so Sphinx/autoapi and the executable notebooks document
**the source at the pinned ref**, not the last PyPI release. Their dependencies still come from
`requirements.txt`.

## Runnable tutorial notebooks

Tutorials authored as executable MyST notebooks (`file_format: mystnb`) are rendered with their
outputs, and the orchestrator also publishes a clean, runnable **`.ipynb`** beside each one and
injects a *"Run this tutorial yourself"* block (download link + how to set up an environment).
This uses `jupytext` to convert the MyST source — no build outputs are baked into the download.
No per-component configuration is needed; any `tutorials/*.md` notebook is picked up
automatically.

## Build modes

**Prerequisites:** Python 3.10+, `git`, and the doc toolchain in `requirements.txt` (Sphinx,
Furo, MyST-NB, sphinx-design, sphinx-copybutton, sphinx-autoapi, `oasislmf`, `ods-tools`). The
Platform REST API is rendered by a **vendored Redoc bundle** (in `OasisPlatform/docs`), so no
Sphinx redoc extension is needed.

### Option A — from your local checkouts (see [Quick start](#quick-start-local-dev))

`./build.sh --local` (own venv) or `python orchestrate.py --use-local` (existing env), building
each component from the sibling checkouts.

### Option B — pinned clone (CI / release)

Clone each component at the `ref` pinned in `modules.json` and build:

```bash
./build.sh                     # == orchestrate.py --clone
```

### Useful flags (`orchestrate.py`)

| Flag | Effect |
| --- | --- |
| `--use-local [BASE]` | build from `BASE/<repo>` checkouts (default: parent dir) |
| `--clone` | clone each repo at its pinned `ref` into `./modules/` |
| `--only NAME …` | build a subset of components |
| `--keep-going` | continue past a failing component (and pass `--keep-going` to Sphinx) |
| `--single-pass` | skip the cross-reference pass (faster; intersphinx links won't resolve) |
| `--absolute-links` | keep cross-links as absolute URLs instead of page-relative |
| `--output DIR` | output directory (default `build/html`) |
| `--deploy-version NAME` | assemble into `build/html/NAME/` and add a sidebar version selector |
| `--latest` | with `--deploy-version`, make the site root and `/latest/` redirect to this version |

## Versioned publishing

`--deploy-version NAME` assembles the site into `build/html/NAME/`, maintains a
`build/html/versions.json` and a root `index.html` redirect, and injects a **version
dropdown** into every page's sidebar. Switching version navigates to the same page under the
chosen version, **falling back to that version's landing** if the page doesn't exist there.

`latest` is **not a version** — it's a redirect. The site root and `/latest/` both forward to
the newest version (or the one built with `--latest`); there's no duplicate `latest/` site and
it never appears in the dropdown.

Each release is one run against an output tree that already holds the other versions, so they
accumulate:

```bash
# in CI: restore the existing published site into build/html first, then add the new version
python orchestrate.py --clone --deploy-version 2.5.7 --latest   # newest → root redirect
```

The version list is scanned from the sub-directories present, so `versions.json`, the redirect
and every dropdown stay consistent. The dropdown list works offline (`file://`); the 404
fallback needs the site served (it does a `HEAD` request), degrading to a direct jump under
`file://`.

**Publishing a release** is done by CI, not by hand — see **[RELEASING.md](RELEASING.md)** for
the step-by-step (pin `modules.json` to the release tags → cut a GitHub release or run the
deploy workflow).

## View the result

The assembled site is static. For a quick look you can open it straight from disk:

```bash
xdg-open build/html/index.html      # navigation, cross-links and logo all work over file://
```

But **prefer a local server** — the search box and the version selector's 404 fallback make
XHR/`HEAD` requests that browsers block over `file://`:

```bash
python -m http.server 8080 --directory build/html
# then browse http://localhost:8080/   (Ctrl-C to stop)
```

## Build via Docker

```bash
docker build -f docker/Dockerfile.oasis_docbuilder -t oasis_doc_builder .
docker run -v "$(pwd)":/tmp/output oasis_doc_builder:latest
```

`build.sh` also packages the site as `output/oasis_docs.tar.gz`.
