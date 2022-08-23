from pathlib import Path
from posixpath import basename, splitext
import re
import os

# lambda l accepts a path and returns just the filename without an extension
l = lambda p: str(os.path.splitext(os.path.basename(p))[0])

# lambda ext is like lambda l, except it returns the file extension
ext = lambda p: str(os.path.splitext(os.path.basename(p))[1])

articles = ['a', 'an', 'the']
def dictCompare(s):
  sWords = s.split()
  if sWords[0].lower() in articles:
    return ' '.join(sWords[1:])
  else:
    return s

with open("scripts/HTMLheader.txt", "r") as headerText:
  header = headerText.readlines()

allFiles = []
for p in Path("./").rglob('*.chopro'):
  allFiles.append(p)
for p in Path("./").rglob('*.cho'):
  allFiles.append(p)

startColor = re.compile('textcolour: *\w+')
endColor = re.compile('textcolour *}')
for p in allFiles:
  try:
    with open(p, mode="r", encoding="utf-8") as f:
      srcLines = f.readlines()

    addColor = False
    with open(p, mode="w", encoding="utf-8") as f:
      for l in srcLines:
        if startColor.search(l):
          addColor = True
        elif endColor.search(l):
          addColor = False
        elif addColor:
          f.write("&blue: " + l)
        else:
          f.write(l)
  except:
    print(f"failed on file {str(p)}")

