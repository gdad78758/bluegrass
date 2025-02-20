import PatchTextColor
from git import Repo

import subprocess
from pathlib import Path
from posixpath import basename, splitext
import sys
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--musicFolder", type=str, default='.')
args = parser.parse_args()

print("Generating Music List (this takes a few seconds)", file=sys.stderr)

musicFolder = args.musicFolder

def createPDFs():
  chordproSettings=[
  	"chordpro",
          "--config=Ukulele",
          "--config=Ukulele-ly",
          "--define=pdf:diagrams:show=none",
          "--define=settings:inline-chords=true",
          "--define=pdf:margintop=70",
          "--define=pdf:marginbottom=0",
          "--define=pdf:marginleft=20",
          "--define=pdf:marginright=20",
          "--define=pdf:headspace=50",
          "--define=pdf:footspace=10",
          "--define=pdf:head-first-only=true",
          "--define=pdf:fonts:chord:color=red",
          "--text-font=helvetica",
          "--chord-font=helvetica"
  ]

  # lambda ext is like lambda l, except it returns the file extension
  ext = lambda p: str(os.path.splitext(os.path.basename(p))[1]).lower()

  extensions = [".chopro", ".cho"]
  for p in Path(musicFolder).rglob('*'):
    if ext(p) in (extension.lower() for extension in extensions):
      subprocess.run(chordproSettings + [str(p)])

repo = Repo('.')
if repo.is_dirty():
  print("Cannot operate on a repo with changes -- " +
        "commit, discard, or stash your changes and try again")
else:
  PatchTextColor.PatchColors()
  createPDFs()
  repo.git.restore('*.chopro')
  repo.git.restore('*.cho')

