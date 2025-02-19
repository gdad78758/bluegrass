from pathlib import Path
from posixpath import basename, splitext
import re
import os

allFiles = []
for p in Path("./").rglob('*.chopro'):
  allFiles.append(p)
for p in Path("./").rglob('*.cho'):
  allFiles.append(p)

startColor = re.compile('textcolour: *\w+')
endColor = re.compile('textcolour *}')
onsongColor = re.compile('&blue:')

for p in allFiles:
  try:
    with open(p, mode="r", encoding="utf-8") as f:
      srcLines = f.readlines()

    addColor = False
    with open(p, mode="w", encoding="utf-8") as f:
      for l in srcLines:
        if not addColor and onsongColor.search(l):
          addColor = True
          f.write("{textcolour: blue}\n")
        elif addColor and not onsongColor.search(l):
          addColor = False
          f.write("{textcolour}\n")

        if addColor:
          newL = l.replace('&blue:','')
          f.write(newL)
        else:
          f.write(l)

      if addColor:
        f.write("{textcolour}\n")


  except:
    print(f"failed on file {str(p)}")

