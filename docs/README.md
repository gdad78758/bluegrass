# GitHub Pages

This directory contains the documentation and configuration for GitHub Pages deployment.

## Files

- `index.md` - Main documentation page
- `_config.yml` - Jekyll configuration for GitHub Pages

## Deployment

The site is automatically deployed via GitHub Actions when changes are pushed to the `butler-gh-pages` branch.

## Local Development

To test locally:

```bash
gem install bundler jekyll
jekyll serve --source docs
```

Visit `http://localhost:4000` to view the site.