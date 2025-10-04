import subprocess
from pathlib import Path
from posixpath import basename, splitext
import os

def createPDFs(musicTarget, pagesize, showchords):
  chordproSettings=[
  	"chordpro",
          "--config=ukulele",
          "--config=ukulele-ly",
          "--define=pdf:diagrams:show=" + showchords,
          "--define=settings:inline-chords=true",
          "--define=pdf:even-odd-pages=0",
          "--define=pdf:margintop=70",
          "--define=pdf:marginbottom=0",
          "--define=pdf:marginleft=10",
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
  if os.path.exists(musicTarget):
    if os.path.isdir(musicTarget):
      for p in Path(musicTarget).rglob('*'):
        if ext(p) in (extension.lower() for extension in extensions):
          pdf_output = str(p).replace(ext(p), '.pdf')
          subprocess.run(chordproSettings + [f"--output={pdf_output}", str(p)])
    else:
      if ext(musicTarget) in (extension.lower() for extension in extensions):
        pdf_output = musicTarget.replace(ext(musicTarget), '.pdf')
        subprocess.run(chordproSettings + [f"--output={pdf_output}", musicTarget])
  else:
    print(f"no such file or folder '{musicTarget}'")
