import os
import re
from pathlib import Path


def PatchColors(musicTarget):
    # Function to get file extension (same as in GenPDF.py)
    def ext(p):
        return str(os.path.splitext(os.path.basename(p))[1]).lower()

    extensions = [".chopro", ".cho"]
    allFiles = []

    if os.path.exists(musicTarget):
        if os.path.isdir(musicTarget):
            print(
                f"PatchColors: Processing all .chopro and .cho files "
                f"in directory '{musicTarget}'"
            )
            for p in Path(musicTarget).rglob("*"):
                if ext(p) in (extension.lower() for extension in extensions):
                    allFiles.append(p)
                    print(f"PatchColors: Found file to process: {p}")
        else:
            if ext(musicTarget) in (
                extension.lower() for extension in extensions
            ):
                allFiles.append(Path(musicTarget))
                print(f"PatchColors: Processing single file '{musicTarget}'")
    else:
        print(f"PatchColors: no such file or folder '{musicTarget}'")
        return

    onsongColor = re.compile(r"&blue:?")

    for p in allFiles:
        try:
            with open(p, mode="r", encoding="utf-8") as f:
                srcLines = f.readlines()

            addColor = False
            with open(p, mode="w", encoding="utf-8") as f:
                for line in srcLines:
                    if not addColor and onsongColor.search(line):
                        addColor = True
                        f.write("{textcolour: blue}\n")
                    elif addColor and not onsongColor.search(line):
                        addColor = False
                        f.write("{textcolour}\n")

                    if addColor:
                        newL = re.sub(".?&blue:?/? *", "", line)
                        f.write(newL)
                    else:
                        f.write(line)

                if addColor:
                    f.write("{textcolour}\n")

        except Exception as e:
            print(f"failed on file {str(p)}: {e}")

PatchColors(".")
