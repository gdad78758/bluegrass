from pathlib import Path
from posixpath import basename, splitext
import os
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputTextFileName")
args = parser.parse_args()

inputTextFileName = args.inputTextFileName

with open(inputTextFileName, "r") as inputTextFile:
  inputText = inputTextFile.readlines()

HtmlFileName = 'Links.html'
with open(HtmlFileName, "w") as HtmlFile:
  Titleline = "Links:"
  HtmlFile.write(Titleline)
  HtmlFile.write('<br /><br />')
  line = 2
  for line in inputText:
    HtmlLine = line
    HtmlLine = re.sub("^(.*)(http.*)", f"<a href=\"\\2\"> \\1 </a> <br>", HtmlLine)

    HtmlFile.write(HtmlLine.rstrip())
