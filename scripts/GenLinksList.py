# invoke with: 
# python3 path/GenLinksList.py Path/Links.txt
#
from pathlib import Path
from posixpath import basename, splitext
import os
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputLinksFileName")
args = parser.parse_args()

inputLinksFileName = args.inputLinksFileName

#added these 2 lines
with open("HTMLheader.txt", "r") as headerText:
  header = headerText.readlines()


with open(inputLinksFileName, "r") as inputLinksFile:
  inputText = inputLinksFile.readlines()

HtmlFileName = 'GeneratedLinksList.html'
with open(HtmlFileName, "w") as HtmlFile:

# added this line
  HtmlFile.writelines(header)
  
  Titleline = "Links:"
  HtmlFile.write(Titleline)
  HtmlFile.write('<br /><br />')
  line = 2
  for line in inputText:
    HtmlLine = line
    HtmlLine = re.sub("^(.*)(http.*)", f"<a href=\"\\2\"> \\1 </a> <br>", HtmlLine)
   
    HtmlFile.write(HtmlLine.rstrip())
