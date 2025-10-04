---
title: GenPDF Butler
description: A Python package for generating PDFs from ChordPro files
---

# GenPDF Butler

A Python package for running ChordPro CLI over a folder to generate PDFs from chord charts and sheet music.

## Features

- **Batch Processing**: Process entire directories of `.chopro` and `.cho` files
- **Configurable Output**: Customize page size, chord display, and formatting
- **Ukulele Optimized**: Pre-configured settings for ukulele chord charts
- **Flexible Input**: Handle single files or entire directory trees

## Installation

```bash
pip install genpdf-butler
```

## Quick Start

```python
from genpdf_butler.GenPDF import createPDFs

# Generate PDFs from all .chopro files in a directory
createPDFs('/path/to/music/folder', 'a4', 'true')

# Process a single file
createPDFs('/path/to/song.chopro', 'letter', 'false')
```

## Parameters

- **musicTarget**: Path to file or directory containing ChordPro files
- **pagesize**: Paper size (`'a4'`, `'letter'`, etc.)
- **showchords**: Chord diagram display (`'true'` or `'false'`)

## Command Line Usage

After installation, you can use the command line interface:

```bash
# Process current directory with default settings (a6 paper, no chords)
genpdf

# Process specific directory with custom settings
genpdf /path/to/music/folder --pagesize a4 --showchords true

# Process single file
genpdf song.chopro --pagesize letter --showchords false
```

### Arguments

- **musictarget** (optional): Path to .chopro file or directory (defaults to current directory)
- **--pagesize**: Paper size (default: 'a6')
- **--showchords**: Show chord diagrams ('true' or 'false', default: 'false')

## Requirements

- Python 3.11+
- ChordPro CLI tool installed and available in PATH

## Repository

- **Homepage**: [https://github.com/gdad78758/bluegrass](https://github.com/gdad78758/bluegrass)
- **Issues**: [https://github.com/gdad78758/bluegrass/issues](https://github.com/gdad78758/bluegrass/issues)

## License

MIT License - see LICENSE file for details.