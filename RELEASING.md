# Publishing the Oasis documentation

A runbook for **publishing a new version** of the aggregated documentation site to
`https://oasislmf.github.io/`. You don't build or deploy from your laptop — CI does it. Your
job is to pin the versions and trigger the deploy.

> Background on *how* the build works is in [README.md](README.md); this page is only the
> release steps.

## What a "documentation release" is

The published site is **versioned**: `oasislmf.github.io/<version>/…`, with a version dropdown
in every page's sidebar and the root redirecting to the latest. Publishing a version means
building each component's docs **at a fixed git tag** and adding that build as a new
`/<version>/` on the site (older versions are kept).

## Before you start

- The components you're publishing have **cut their releases** (git tags exist), e.g.
  `OasisLMF 2.5.7`, `ODS_OpenResultsData 3.0.1`, …
- You can push to `main` on `GenerateDocs` (or open a PR) and run its GitHub Actions.

## Step 1 — pin `modules.json` to the release tags

`modules.json` lists each component and the git `ref` its docs are built from. For a released
site, set every `ref` to the **release tag** (not a branch — a branch moves, a tag is frozen,
so the published `/<version>/` stays reproducible):

```jsonc
{ "name": "oasislmf", "ref": "2.5.7", ... }   // was a branch like "main"
{ "name": "ord",      "ref": "3.0.1", ... }   // components can tag independently
...
```

Commit this to `main` (directly or via PR). This single commit defines the exact source the
next publish will build from.

## Step 2 — trigger the deploy

Either:

- **Cut a GitHub Release** on `GenerateDocs` with the tag = the version label (e.g. `2.5.7`).
  The `Build and Deploy (versioned)` workflow fires; a normal (non-prerelease) release is
  published as the site's **latest**. *(Recommended — the release is the record of the publish.)*
- **Or run it manually:** Actions → **Build and Deploy (versioned)** → **Run workflow**, and
  enter:
  - `version` — the label, e.g. `2.5.7` (becomes the `/2.5.7/` sub-path)
  - `set_latest` — tick to point the site root at this version (leave unticked to publish an
    older/back-version without moving root).

## What CI does (no action needed)

1. Restores the currently-published site (so existing versions are kept).
2. Clones each component at its pinned `ref` and builds its docs.
3. Assembles them into `/<version>/`, refreshes `versions.json`, the root redirect and the
   version dropdown across **all** versions.
4. Deploys the whole tree to the Pages branch.

## Step 3 — verify

Once the workflow is green, open `https://oasislmf.github.io/`:

- it redirects to the new version (if you set it latest);
- the sidebar **Version** dropdown lists the new version and switches correctly;
- switching to a version that lacks a given page falls back to that version's landing.

## Notes & edge cases

- **Publishing a back-version / not moving root:** run manually with `set_latest` unticked.
- **Re-publishing / fixing a version:** just release/dispatch the same version again — it
  rebuilds and overwrites that `/<version>/` in place.
- **First-ever deploy:** there's no site to restore, so add any `CNAME` / `.nojekyll` the Pages
  site needs (later deploys preserve them automatically).
- **Pages source branch:** the deploy targets `gh-pages` (see `PAGES_BRANCH` in
  `.github/workflows/build-deploy.yml`) — confirm GitHub Pages for `OasisLMF.github.io` is set
  to serve that branch.
- **A "latest tracks main" channel** (optional): pin `modules.json` refs to `main` and publish
  with `version: latest` to keep a rolling `/latest/` alongside the tagged versions.
- **Secret:** the deploy uses `BUILD_DEPLOY_TOKEN` (write access to `OasisLMF.github.io`).
