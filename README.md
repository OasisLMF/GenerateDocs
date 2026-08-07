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

## Build locally

**Prerequisites:** Python 3, `git`, and the doc toolchain in `requirements.txt` (Sphinx, Furo,
MyST-NB, sphinx-design, sphinx-autoapi, sphinxcontrib-redoc, `oasislmf`, `ods-tools`).

### Option A — from your local checkouts (fastest for iterating)

Check the component repos out next to this one (`../OasisLMF`, `../OasisPlatform`,
`../ODS_OpenResultsData`, …) on the branch you want, then:

```bash
./build.sh --local
```

This builds every component from your local checkouts and assembles the site. To run the
orchestrator directly in an environment that already has the toolchain (skipping the venv step):

```bash
python orchestrate.py --use-local            # build all components + landing
python orchestrate.py --use-local --only ord ods-tools   # just these
```

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
| `--latest` | with `--deploy-version`, point the root redirect at this version |

## Versioned publishing

`--deploy-version NAME` assembles the site into `build/html/NAME/`, maintains a
`build/html/versions.json` and a root `index.html` redirect, and injects a **version
dropdown** into every page's sidebar. Switching version navigates to the same page under the
chosen version, **falling back to that version's landing** if the page doesn't exist there.

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

## View the result

The assembled site is static — just open the landing page:

```bash
xdg-open build/html/index.html      # or open it in your browser
```

Everything navigates from the filesystem. The only feature that needs a server is the search
box (browsers block its data load over `file://`):

```bash
python -m http.server 8080 --directory build/html
# then browse http://localhost:8080/
```

## Build via Docker

```bash
docker build -f docker/Dockerfile.oasis_docbuilder -t oasis_doc_builder .
docker run -v "$(pwd)":/tmp/output oasis_doc_builder:latest
```

`build.sh` also packages the site as `output/oasis_docs.tar.gz`.
