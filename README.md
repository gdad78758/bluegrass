# bluegrass - Repository for bluegrass music

Notes:
1. We consider the filetype 'chopro' to be the master of our songs list
2. Try to put the version number of our song in the title.  For example
   within the chopro file include a line like {title:Home Sweet Home v2}
3. Once we're happy with the chopro file then from the main bluegrass folder
   1. commit any changes made to the chopro files
   2. generate pdfs from the master chopro files by invoking this from the bluegrass root folder:
        python GenPDF.py (must be from Windows Cli)
      This will take awhile, but when it's done you'll have a bunch of pdf files that have been changed.
   3. When ii. is done, commit the pdf file changes

   Note:  the python GenPDF.py step will not work if you haven't committed all previous changes to the repo.

   Set list PDF:
   1. The set list master file is generated from numbered ChordPro files in notes/set_list.
   2. From the notes/set_list folder, run:
      python ../../GenSetList.py
      This writes notes/set_list/00 - Set List.chopro by concatenating 00-99 prefixed .chopro files in order.
   3. The PDF (notes/set_list/00 - Set List.pdf) is generated from that .chopro via:
      genpdf --force --pagesize a5 "notes/set_list/00 - Set List.chopro"
   4. In GitHub Actions (see .github/workflows/deploy-pages.yml), the set list .chopro is regenerated
      on every deploy, and the PDF is generated only if it is missing. The set list PDF is not committed
      back to the repo by the workflow.

   Random set list:
   1. The workflow can generate a random set list (7 songs) from notes/set_list and Christmas.
   2. It runs weekly on Thursday at 03:00 Central (see schedule in .github/workflows/deploy-pages.yml).
   3. You can also run it manually via Actions and enable the "Generate random set list" input.
   4. The random selection is appended to random.log and committed back to the repo.
   5. The generated notes/set_list/00 - Random.chopro and PDF are published to GitHub Pages only,
      and are not committed to the repo.

Hook setup:
1. To auto-update the main.css cache-busting query before commits, install the hook:
   - Git Bash: scripts/install-hooks.sh
   - PowerShell: scripts/install-hooks.ps1
  