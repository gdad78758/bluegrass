#
# Invoke with:
#   python3 GenSongsList.py SongsFolder
# from pathlib import Path

from pathlib import Path
from posixpath import basename, splitext
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("musicFolder")
args = parser.parse_args()

musicFolder = args.musicFolder

# lambda l accepts a path and returns just the filename without an extension
l = lambda p: str(os.path.splitext(os.path.basename(p))[0])

# lambda ext is like lambda l, except it returns the file extension
ext = lambda p: str(os.path.splitext(os.path.basename(p))[1]).lower()

# dictCompare removes articles that appear as the first word in a filename
articles = ['a', 'an', 'the']
def dictCompare(s):
  formattedS = ''
  sWords = s.split()
  if sWords[0].lower() in articles:
    formattedS = ' '.join(sWords[1:])
  else:
    formattedS = s

  # Remove punctuation
  formattedS.replace('\'','')
  formattedS.replace(',','')

  return formattedS

with open("HTMLheader.txt", "r") as headerText:
  header = headerText.readlines()

extensions = [".PDF", ".chopro", ".cho", ".aif", ".mp3", ".mscz",
              ".jpg", ".jpeg", ".txt", ".png", ".html", ".urltxt",".wav"]

allFiles = []
for p in Path(musicFolder).rglob('*'):
  if ext(p) in (extension.lower() for extension in extensions):
    allFiles.append(p)

def findMatchingBasename(files, basename):
  matches = [f for f in files if f[0].lower() == l(basename).lower()]
  if matches:
    # matches should never have more than one entry, but there is no check to
    # verify that claim. The only way we intend to add a new file path to
    # "files" is when no entry already has a file with the same basename.
    return matches[0]
  else:
    return None

# allTitles will be an array of arrays. Each element's [0] entry will be the
# song title. The other entries will be file paths that contain that title.
allTitles = []
for p in allFiles:
  matchingTitle = findMatchingBasename(allTitles, p)
  if matchingTitle:
    # add a newly found file for a previously found song
    matchingTitle.append(str(p))
  else:
    # found a song for the first time. Add the title and the filename
    allTitles.append([l(p), str(p)])

downloadExtensions = [".cho", ".chopro", ".mscz"]
sortedTitles = sorted(allTitles, key=(lambda e: dictCompare(e[0]).casefold()))
with open("GeneratedNotesList.html", "w") as htmlOutput:
  # define separator character sep
  sep='&nbsp&nbsp'
  htmlOutput.writelines(header)
  htmlOutput.write("<table>")
  for f in sortedTitles:
    try:
      htmlOutput.write("<tr>")
      # first table column contains the song title (f[0])
      htmlOutput.write(f"  <td>{f[0]}</td>\n<td>")
      # the remainder of f's elements are files that match the title in f[0]
      for i in f[1:]:
#        if ext(i) != ".pdf":
#          htmlOutput.write(f"  <a href=\"{str(i)}\" download>{ext(i)}</a>\n")
#       else:
#         htmlOutput.write(f"  <a href=\"{str(i)}\">{ext(i)}</a>\n")
#
        if ext(i) == ".urltxt":
          with open(i, "r") as urlFile:
            label = urlFile.readline()
            address = urlFile.readline()
          htmlOutput.write(f"<a href=\"{address}\">{sep}{label}{sep}</a>\n")
        elif ext(i) in downloadExtensions:
          htmlOutput.write(f"  <a href=\"{str(i)}\" download>{ext(i)}{sep}</a>\n")
        else:
          htmlOutput.write(f"  <a href=\"{str(i)}\">{ext(i)}{sep}</a>\n")

      # close each table row (and the table data containing file links)
      htmlOutput.write("</td></tr>\n")
    except:
      print(f"failed to write {f[1:]}")

  #close the table etc.
  htmlOutput.write("</table>")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</body>\n")
