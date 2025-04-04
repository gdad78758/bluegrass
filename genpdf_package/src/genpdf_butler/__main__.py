from genpdf_butler import PatchTextColor
from genpdf_butler import GenPDF
from git import Repo

import subprocess
from pathlib import Path
from posixpath import basename, splitext
import sys
import os
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--musicFolder", type=str, default='.')
  args = parser.parse_args()

  print("Generating Music List (this takes a few seconds)", file=sys.stderr)

  musicFolder = args.musicFolder

  repo = Repo('.')
  if repo.is_dirty():
    print("Cannot operate on a repo with changes -- " +
          "commit, discard, or stash your changes and try again")
  else:
    PatchTextColor.PatchColors()
    createPDFs()
    repo.git.restore('*.chopro')
    repo.git.restore('*.cho')

if __name__ == "__main__":
  main()
