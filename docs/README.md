# GitHub Pages

This directory holds the rendered site that GitHub Pages serves for `silvergrassband.com`.

## Files

- `index.md` – Main Jekyll entry point that summarizes the generated HTML lists
- `_config.yml` – Minimal Jekyll configuration (layout inheritance handled at the repo root)
- `CNAME` – Declares the custom domain `silvergrassband.com` so GitHub can provision TLS

## Deployment

- Source branch: `main`
- Build workflow: `.github/workflows/deploy-pages.yml`
- Build steps (high level):
	1. Generate PDFs when `.chopro` files change
	2. Regenerate the HTML lists via `scripts/GenList.py`
	3. Copy the repo content (including `CNAME`) into `docs/`
	4. Run the official `jekyll-build-pages` action and upload `_site`
- Pages environment: configured via GitHub UI with **Custom domain** `silvergrassband.com` and **Enforce HTTPS** enabled once DNS verification succeeds

## Local Development

To preview the Jekyll site locally from this folder only:

```bash
gem install bundler jekyll
jekyll serve --source docs
```

Visit `http://localhost:4000` to view the local build (custom-domain HTTPS is handled only on GitHub Pages).
