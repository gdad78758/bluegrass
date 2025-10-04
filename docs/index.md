---
title: Bluegrass Music Collection
description: A collection of bluegrass chord charts, sheet music, and audio files
---

# Bluegrass Music Collection

Welcome to the bluegrass music collection featuring chord charts, sheet music, and audio files for bluegrass musicians and enthusiasts.

## Generated Lists

The following lists are automatically generated during site deployment:

- **Notes List** (`GeneratedNotesList.html`) - Songs both finished and working
- **Songs List** (`GeneratedSongsList.html`) - Miscellaneous songs we've not done  
- **Christmas Songs** (`Christmas.html`) - Holiday music collection
- **Katy Lessons** (`KatyLessons.html`) - Educational materials

*Note: These HTML files are generated during deployment and will be available once the site is published.*

## About This Collection

This collection contains:
- **ChordPro files** (`.chopro`, `.cho`) - Chord charts with lyrics
- **PDF sheet music** - Generated from ChordPro files
- **Audio files** (`.mp3`, `.m4a`, `.aif`) - Reference recordings
- **MuseScore files** (`.mscz`) - Editable sheet music
- **Text files** - Additional notes and resources

## PDF Generation

PDFs are automatically generated using [genpdf-butler](https://github.com/TuesdayUkes/genpdf-butler), a Python package for converting ChordPro files to PDF format.

### Automatic Generation
- PDFs are generated during site deployment when `.chopro` files are newer than their corresponding `.pdf` files
- Uses Git history to determine when files were last modified (not filesystem timestamps)
- Only regenerates PDFs when the source ChordPro file has actually changed

### Manual PDF Control
For better control and faster builds, you can check PDF files directly into the repository:

- **Commit PDFs to Git**: Check in `.pdf` files alongside their `.chopro` counterparts
- **Prevents regeneration**: Committed PDFs won't be regenerated unless the `.chopro` file is modified after the PDF
- **Custom formatting**: Allows manually created or customized PDFs to override automatic generation
- **Faster builds**: Skips ChordPro installation and PDF generation when all PDFs are up to date
- **Mixed approach**: Some PDFs can be committed while others are auto-generated as needed

**Example workflow:**
1. Create or modify a `.chopro` file
2. Generate PDF locally: `genpdf --pagesize a5 mysong.chopro`
3. Customize the PDF if needed (manual edits, different settings)
4. Commit both `.chopro` and `.pdf` files to Git
5. Future deployments will skip regeneration unless you modify the `.chopro` file

## Repository

- **Homepage**: [https://github.com/gdad78758/bluegrass](https://github.com/gdad78758/bluegrass)
- **Issues**: [https://github.com/gdad78758/bluegrass/issues](https://github.com/gdad78758/bluegrass/issues)
