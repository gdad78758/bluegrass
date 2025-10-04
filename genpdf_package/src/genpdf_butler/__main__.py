from genpdf_butler import PatchTextColor
from genpdf_butler import GenPDF
from git import Repo

from posixpath import basename, splitext
import sys
import os
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("musictarget", nargs='?', default=os.getcwd(), help=".chopro filename or directory containing .chopro files")
  parser.add_argument("--pagesize", type=str, default='a6')
  parser.add_argument("--showchords", type=str, default='false')
  args = parser.parse_args()

  print("Generating Music List (this takes a few seconds)", file=sys.stderr)

  musictarget = args.musictarget
  pagesize = args.pagesize
  showchords = args.showchords

  repo = Repo(path='.', search_parent_directories=True)
  
  # Check if any .chopro or .cho files are modified or untracked
  dirty_chopro_files = [item.a_path for item in repo.index.diff(None) if item.a_path.endswith(('.chopro', '.cho'))]
  untracked_chopro_files = [f for f in repo.untracked_files if f.endswith(('.chopro', '.cho'))]
  
  if dirty_chopro_files or untracked_chopro_files:
    print("Cannot operate on a repo with .chopro/.cho changes -- " +
          "commit, discard, or stash your .chopro/.cho changes and try again")
    if dirty_chopro_files:
      print("Modified .chopro/.cho files:", dirty_chopro_files)
    if untracked_chopro_files:
      print("Untracked .chopro/.cho files:", untracked_chopro_files)
  else:
    PatchTextColor.PatchColors()
    GenPDF.createPDFs(musictarget, pagesize, showchords)
    repo.git.restore('*.chopro')
    repo.git.restore('*.cho')

if __name__ == "__main__":
  main()
