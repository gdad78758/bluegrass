from genpdf_butler import PatchTextColor
from genpdf_butler import GenPDF
from git import Repo

from posixpath import basename, splitext
import sys
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--musicFolder", type=str, default='.')
  parser.add_argument("--pagesize", type=str, default='a6')
  parser.add_argument("--showchords", type=str, default='false')
  args = parser.parse_args()

  print("Generating Music List (this takes a few seconds)", file=sys.stderr)

  musicFolder = args.musicFolder
  pagesize = args.pagesize
  showchords = args.showchords

  repo = Repo(path='.', search_parent_directories=True)
  if repo.is_dirty():
    print("Cannot operate on a repo with changes -- " +
          "commit, discard, or stash your changes and try again")
  else:
    PatchTextColor.PatchColors()
    GenPDF.createPDFs(musicFolder, pagesize, showchords)
    repo.git.restore('*.chopro')
    repo.git.restore('*.cho')

if __name__ == "__main__":
  main()
