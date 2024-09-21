from first import first
from pathlib import Path
from posixpath import basename, splitext
import sys
import os
import argparse
from re import M
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("musicFolder")
parser.add_argument("outputFile")
parser.add_argument("--intro", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()

print("Generating Music List (this takes a few seconds)", file=sys.stderr)

musicFolder = args.musicFolder
outputFile = args.outputFile
intro = args.intro

now = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

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
  formattedS = formattedS.replace('\'','')
  formattedS = formattedS.replace(',','')

  return formattedS.lower()

with open(musicFolder + "/scripts/HTMLheader.txt", "r") as headerText:
  header = headerText.readlines()

introduction = """
<h1>Tuesday Ukes' archive of ukulele songs and chords</h1>

<p>Whether you're a beginner ukulele player looking for easy songs or a longtime
player searching for fun songs, this is the resource for you. Here you will find
ukulele chords and chord diagrams for uke players of all levels.</p>

<p>This collection of the best ukulele songs has been built over time by members
of Austin's Tuesday Ukulele Group. </p>

<h2>Lots of popular songs</h2>
<p>There's a big range: Easy ukulele songs with simple chords for beginner
ukulele players with just 3 chords or 4 chords. You will find great songs  by
Paul McCartney, Neil Diamond, Bob Dylan, John Denver, and Bob Marley turned into
ukulele music. More-advanced ukulele music players can find finger-stretching
chord changes and chord shapes applied to popular ukulele songs. </p>

"""

footer = """
<p>Chord progressions and strum patterns listed are the members' interpretations
of the original recordings, and are presented for educational purposes. Except
as noted (a few of our members are songwriters), we make no copyright claim on
any song.</p>
"""

extensions = [".PDF", ".chopro", ".cho", ".mscz", ".urltxt"]
allFiles = []
for p in Path(musicFolder).rglob('*'):
  if ext(p) in (extension.lower() for extension in extensions):
    allFiles.append(p.as_posix())

# return the first file that matches basename (there should be only zero or one
# matches). Return None if no matches found.
def findMatchingBasename(files, basename):
  return first((f for f in files if dictCompare(f[0]) == dictCompare(l(basename))))

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

downloadExtensions = [".cho", ".chopro"]
sortedTitles = sorted(allTitles, key=(lambda e: dictCompare(e[0]).casefold()))
with open(outputFile, "w") as htmlOutput:
  htmlOutput.writelines(header)
  if intro:
    htmlOutput.writelines(introduction)
  htmlOutput.write("<table>")
  for f in sortedTitles:
    try:
      htmlOutput.write("<tr>")
      # first table column contains the song title (f[0])
      htmlOutput.write(f"  <td>{f[0]}</td>\n<td>")
      # the remainder of f's elements are files that match the title in f[0]
      for i in f[1:]:
        if ext(i) == ".urltxt":
          with open(i, "r") as urlFile:
            label = urlFile.readline().strip()
            address = urlFile.readline().strip()
          htmlOutput.write(f"<a href=\"{address}\">{label}</a><br>\n")
        elif ext(i) in downloadExtensions:
          htmlOutput.write(f" <a href=\"{str(i).replace(' ','%20')}?v={now}\" download=\"{l(i)}{ext(i)}\">{ext(i)}</a><br>\n")
        else:
          htmlOutput.write(f"  <a href=\"{str(i).replace(' ','%20')}?v={now}\">{ext(i)}</a><br>\n")

      # close each table row (and the table data containing file links)
      htmlOutput.write("</td></tr>\n")
    except:
      print(f"failed to write {f[1:]}")

  #close the table etc.
  htmlOutput.write("</table>")
  if intro:
    htmlOutput.write(footer)
  htmlOutput.write("</div>\n")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</body>\n")

print("Done!", file=sys.stderr)
