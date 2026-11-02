# Bluegrass Music Collection

This repository contains the band's ChordPro charts, PDFs, recordings, sheet music, and generated song lists. The `.chopro` file is the editable source of truth for a song; generated HTML lists and PDFs should not be edited as substitutes for that source.

## Adding or updating a song

1. Add the song's `<Title>.chopro` file to the appropriate collection folder. Songs in the main notes/set-list collection belong in `notes/set_list/`; other collections, such as `Christmas/`, have their own folders.
2. Put a `{title:...}` directive near the top of the ChordPro file. Include a version in the title when useful, for example `{title:Home Sweet Home v2}`.
3. If the song is still being worked on, add its filename stem (the title without `.chopro`) on its own line in `notes/set_list/workingsetlist.txt`. This controls the generated **Working Songs** collection.
4. When the song is ready for the finished set list, also add its title on its own line in `notes/set_list/setlist.txt`. The order of titles in this file is the order in the finished set list. A song can remain in the working list if it is useful there.
5. Commit the `.chopro` and list-file changes. Do not edit the generated `Working Songs` or `Finished Set List` files by hand.

The notes site's `songs.html` list is generated from files in `notes/set_list/`, so a new song in that folder appears there on deployment without a separate list entry. Other collection pages are generated from their corresponding folders.

## Generating set lists locally

Run these commands from the repository root. The finished list reads titles from `notes/set_list/setlist.txt`; the working list reads `notes/set_list/workingsetlist.txt`. Titles are matched to `.chopro` file names in `notes/set_list/` (including subfolders).

```shell
python GenSetList.py --list notes/set_list/setlist.txt -o "notes/set_list/Finished Set List.chopro"
python GenSetList.py --list notes/set_list/workingsetlist.txt -o "notes/set_list/Working Songs.chopro"
```

To generate or refresh the corresponding PDFs locally, use ChordPro's `genpdf` command:

```shell
genpdf --force --pagesize a5 "notes/set_list/Finished Set List.chopro"
genpdf --force --pagesize a5 "notes/set_list/Working Songs.chopro"
```

## PDFs and deployment

The GitHub Pages workflow (`.github/workflows/deploy-pages.yml`) regenerates the finished and working set-list `.chopro` files on deployment. It generates PDFs for `.chopro` files that are missing a PDF or have a newer committed source file, and commits generated PDFs back to the repository. The generated HTML lists and the site content are also rebuilt for deployment.

For manual PDF generation, install ChordPro and `genpdf-butler`, then run `genpdf --pagesize a5 "<file>.chopro"` from the repository root. For set-list PDFs, use the `--force` commands above so the generated PDFs reflect the latest set-list contents.

## Random weekly set list

The workflow can also generate a random selection of two songs from `Christmas/` and five from `notes/set_list/Finished/`. It runs on the weekly schedule in `.github/workflows/deploy-pages.yml` or can be started manually from the GitHub Actions tab with **Generate random set list** enabled. The selection is recorded in `random_log.html`; temporary generated set-list files are removed by the workflow.

## Git hook setup

To automatically update the `main.css` cache-busting query before commits, install the hook:

- Git Bash: `scripts/install-hooks.sh`
- PowerShell: `scripts/install-hooks.ps1`
