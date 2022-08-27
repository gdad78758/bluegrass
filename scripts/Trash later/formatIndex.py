from pathlib import Path
from posixpath import basename, splitext
import os
import argparse

import re

parser = argparse.ArgumentParser()
parser.add_argument("inputFilename")
parser.add_argument("youtubeLink")
args = parser.parse_args()

inputFilename = args.inputFilename
youtubeLink = args.youtubeLink
JsFilename = "VideoIndex.js"
HtmlFilename = "VideoIndex.html"

with open(inputFilename, "r") as sourceText:
  sourceLines = sourceText.readlines()

with open(HtmlFilename, "w") as HtmlFile:
  with open(JsFilename, "w") as JsFile:
    JsFile.write("document.write('\\")
    JsFile.write("\n")
    HtmlFile.write("<table>\n")
    JsFile.write("<table>\\\n")
    for l in sourceLines:
      HtmlFile.write("<tr>")
      JsFile.write("<tr>")

      newL = l

      # For timestamps greater than an hour, look for three numbers separated by 2 colons
      newL = re.sub("^(\d+):(\d+):(\d+)", f"<td><a href=\"{youtubeLink}?t=\\1h\\2m\\3s\">\\1:\\2:\\3</a></td>",newL)

      # For timestamps less than an hour, there are only two time fields (minutes : seconds)
      newL = re.sub("^(\d+):(\d+)", f"<td><a href=\"{youtubeLink}?t=\\1m\\2s\">\\1:\\2</a></td>",newL)

      # reshape URL for sheet music into an HTML tag using the song title as the
      # visible text
      newL = re.sub("\((.*)\) (https?:.*)", r"<td><a href=\2>\1</a></td>",newL)

      # Add <td></td> around player's name
      newL = re.sub("(?:</td> *)(.*)(?: *<td|$)", r"<td>\1</td>", newL)

      # If song title wasn't used with a link, split it from the player name here:
      newL = re.sub("\((.*)\)", r"</td><td>\1", newL)

      HtmlFile.write(newL.rstrip())

      # Add escape backslashes in front of single quotes (also used as apostrophe)
      # for the sake of the .js document.write string
      newL = re.sub(r"'", r"\\'",newL)

      JsFile.write(newL.rstrip())

      HtmlFile.write("</tr>\n")
      JsFile.write("</tr>\\\n")

    HtmlFile.write("</table>")
    JsFile.write("</table>")
    JsFile.write(r"')")
