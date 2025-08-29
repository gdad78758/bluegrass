#! python
import subprocess
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
parser.add_argument("--genPDF", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--forcePDF", action=argparse.BooleanOptionalAction, default=False)
args = parser.parse_args()

print("Generating Music List (this takes a few seconds)", file=sys.stderr)

musicFolder = args.musicFolder
outputFile = args.outputFile
intro = args.intro
forceNewPDF = args.forcePDF
genPDF = args.genPDF

now = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

# lambda l accepts a path and returns just the filename without an extension
l = lambda p: str(os.path.splitext(os.path.basename(p))[0])

# lambda ext is like lambda l, except it returns the file extension
ext = lambda p: str(os.path.splitext(os.path.basename(p))[1]).lower()

def createPDFs():
  linuxpath = ["perl",
               "/home/paul/chordpro/script/chordpro.pl",
               "--config=/home/paul/chordpro/lib/ChordPro/res/config/ukulele.json",
               "--config=/home/paul/chordpro/lib/ChordPro/res/config/ukulele-ly.json"
               ]

  winpath = ["chordpro",
            "--config=Ukulele",
            "--config=Ukulele-ly"
            ]

  chordproSettings=[
    "--define=pdf:diagrams:show=top",
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

  if os.name == "nt":
    chordproSettings = winpath + chordproSettings
  else:
    chordproSettings = linuxpath + chordproSettings

  extensions = [".chopro", ".cho"]
  for p in Path(musicFolder).rglob('*'):
    if ext(p) in (extension.lower() for extension in extensions):
      pdfFile = str(os.path.splitext(str(p))[0]) + ".pdf"
      if not os.path.exists(pdfFile) or forceNewPDF:
        print("Generating " + pdfFile)
        subprocess.run(chordproSettings + [str(p)])

# A file with the extension ".hide" will prevent other files within the same
# folder with the same name (but all extensions) from being adding to the
# archive table. This is a way to conceal older versions of a song, without
# breaking old links to the older versions (the files still exist, but there
# will be no HTML links to them in the new archive table).
def removeHiddenFiles(allFiles):
  hideFiles = []
  for f in allFiles:
    if ext(f).lower() == ".hide":
      # Add full path name without extension as lowercase string
      # WARNING! This call to "lower()" (together with the call when
      # constructing "basename" below) will cause files that differ only in case
      # to match, even on Linux
      hideFiles.append(str(os.path.splitext(f)[0]).lower())

  visibleFiles = []
  for f in allFiles:
    # WARNING! This call to "lower()" together with the same call above when
    # appending to "hideFiles" will cause files that differ only in case to
    # match, even on Linux.
    basename = str(os.path.splitext(f)[0]).lower()
    if not (basename in hideFiles):
      visibleFiles.append(f)

  return visibleFiles

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

with open("HTMLheader.txt", "r") as headerText:
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

script = """
    <script>
        const searchInput = document.getElementById('searchInput');
        const table = document.getElementById('dataTable');
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            for (let i = 0; i < rows.length; i++) {
                let rowText = rows[i].textContent.toLowerCase();
                rows[i].style.display = rowText.includes(filter) ? '' : 'none';
            }
        });
    </script>
"""

footer = """
<p>Chord progressions and strum patterns listed are the members' interpretations
of the original recordings, and are presented for educational purposes. Except
as noted (a few of our members are songwriters), we make no copyright claim on
any song.</p>
"""

extensions = [".PDF", ".chopro", ".cho", ".mscz", ".urltxt", ".aif",
              ".txt", ".mp3", ".html", ".jpg", ".jpeg", ".png", ".m4a"]
allFiles = []
for p in Path(musicFolder).rglob('*'):
  if ext(p) in (extension.lower() for extension in extensions):
    allFiles.append(p.as_posix())

visibleFiles = removeHiddenFiles(allFiles)

# return the first file that matches basename (there should be only zero or one
# matches). Return None if no matches found.
def findMatchingBasename(files, basename):
  return first((f for f in files if dictCompare(f[0]) == dictCompare(l(basename))))

# allTitles will be an array of arrays. Each element's [0] entry will be the
# song title. The other entries will be file paths that contain that title.
allTitles = []
for p in visibleFiles:
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

  htmlOutput.write("<h2>Searchable Table</h2>")
  htmlOutput.write('<input type="text" id="searchInput" placeholder="Search table...">')

  htmlOutput.write('<table id="dataTable">')
  htmlOutput.write("<tbody>\n")
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
          htmlOutput.write(f"<a href=\"{address}\" target=\"_blank\">{label}</a><br>\n")
        elif ext(i) in downloadExtensions:
          htmlOutput.write(f" <a href=\"{str(i).replace(' ','%20')}?v={now}\" download=\"{l(i)}{ext(i)}\" target=\"_blank\">{ext(i)}</a><br>\n")
        else:
          htmlOutput.write(f"  <a href=\"{str(i).replace(' ','%20')}?v={now}\" target=\"_blank\">{ext(i)}</a><br>\n")

      # close each table row (and the table data containing file links)
      htmlOutput.write("</td></tr>\n")
    except:
      print(f"failed to write {f[1:]}")

  #close the table etc.
  htmlOutput.write("</tbody>")
  htmlOutput.write("</table>")
  htmlOutput.write(script)
  if intro:
    htmlOutput.write(footer)
  htmlOutput.write("</div>\n")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</body>\n")

print("Done!", file=sys.stderr)
