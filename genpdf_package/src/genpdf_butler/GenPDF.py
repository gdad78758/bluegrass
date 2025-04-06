import subprocess
from pathlib import Path
from posixpath import basename, splitext
import os

def createPDFs(musicFolder, pagesize):
  chordproSettings=[
  	"chordpro",
          "--config=Ukulele",
          "--config=Ukulele-ly",
          "--define=pdf:diagrams:show=none",
          "--define=settings:inline-chords=true",
          "--define=pdf:even-odd-pages=0",
          "--define=pdf:margintop=70",
          "--define=pdf:marginbottom=0",
          "--define=pdf:marginleft=0",
          "--define=pdf:marginright=50",
          "--define=pdf:headspace=50",
          "--define=pdf:footspace=10",
          "--define=pdf:head-first-only=true",
          "--define=pdf:fonts:chord:color=red",
          "--define=pdf:papersize=" + pagesize,
          "--text-font=helvetica",
          "--chord-font=helvetica"
  ]

  # lambda ext is like lambda l, except it returns the file extension
  ext = lambda p: str(os.path.splitext(os.path.basename(p))[1]).lower()

  extensions = [".chopro", ".cho"]
  for p in Path(musicFolder).rglob('*'):
    if ext(p) in (extension.lower() for extension in extensions):
      subprocess.run(chordproSettings + [str(p)])
