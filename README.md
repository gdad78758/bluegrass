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
  