# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

Single-page lab website for Dr. Tinyi Chu (UVA Genome Sciences), deployed via GitHub Pages at `chulab-uva.github.io`. The entire site is one file: `index.html`.

## Stack

- **No build step.** Edit `index.html` directly and push — GitHub Pages serves it as-is.
- **Tailwind CSS** loaded from CDN (no `node_modules`, no `npm`).
- **AOS** (Animate On Scroll) loaded from CDN for scroll animations.
- **Google Fonts**: Inter (body) + Space Grotesk (display/headings).
- **Google Analytics**: tag `G-XXG4WJ5CNJ` at top of `<head>`.

## Figures

All figures are pre-rendered PNGs/JPGs in `figures/`. There is no build pipeline that regenerates them automatically. Figure generator scripts live at the workspace root (`/workspace/gen_dynamics*.js`) and use Node.js + ImageMagick CLI — run them manually when regenerating a figure, then copy the output into `figures/`.

Key figures and their content:
- `fig_bayesprism.png` — BayesPrism deconvolution algorithm diagram
- `fig_dynamics_render.png` — Cell state transition dynamics (sourced from `materials/dynamics.png`)
- `fig_cfrna_vessel.png` — cfRNA vessel illustration (sourced from `materials/cfRNA.png`)
- `fig_prismspot.png` — PrismSpot spatial deconvolution
- `fig_spacefold.png` / `fig_spacefold_lower.jpg` — SpaceFold 3D tissue folding

## Page structure (`index.html`)

Sections in order, each with a matching `id` anchor:
1. `#home` — Hero with PI name, title, stats card (total citations auto-updated)
2. `#research` — Four research cards: Bayesian Deconvolution, cfRNA, SpaceFold, Cell State Dynamics
3. `#publications` — Paper list with journal badges
4. `#software` — Software tools (BayesPrism, PrismSpot, SpaceFold)
5. `#team` — Current members
6. `#join` — Postdoc/grad recruiting, how-to-apply checklist
7. `#contact` — Contact info and funding acknowledgements

CSS utility classes defined in `<style>`:
- `.grad-border` / `.grad-border-subtle` — gradient border cards
- `.badge-nature` / `.badge-cell` / `.badge-science` / `.badge-other` / `.badge-preprint` — journal badge colors
- `.card-hover` — lift-on-hover transition
- `.shimmer-text` — animated gradient text

## Auto-updating citations

`.github/workflows/sync-citations.yml` runs every Monday 06:00 UTC. It calls `.github/scripts/update_citations.py`, which uses the `scholarly` library to fetch:
1. **Total author citations** → updates the `<div class="font-display text-2xl font-bold text-indigo-400">` stat card in the hero.
2. **BayesPrism per-paper citations** → updates `<span class="bayesprism-citations">` in the research card.

If either regex pattern fails to match (e.g. after an HTML restructure), the script prints a warning and exits 0 (no CI failure).

## Git workflow notes

GitHub Pages occasionally pushes `Create CNAME` / `Delete CNAME` commits to `origin/main` directly. This causes push rejections. Standard fix:

```bash
git reset --soft HEAD~1   # un-commit local change (keep edits staged)
git stash
git pull --ff-only origin main
git stash pop
git add <files>
git commit -m "..."
git push origin main
```
