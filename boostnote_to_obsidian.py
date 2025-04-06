# boostnote_to_obsidian.py
# 
# Copyright (C) 2025 guruathwal https://github.com/guruathwal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
import cson
from pathlib import Path
import re

#  CONFIGURATION
# Path to the Boostnote note files (.cson format)
CSON_FOLDER = r"path\to\boostnote\folder"

# Path to the Boostnote folder list file (boostnote.json)
FOLDER_JSON = r"path\to\Boostnote\boostnote.json"

# Destination folder where converted markdown files will be saved (Obsidian vault)
OUTPUT_DIR = r"path\to\obsidian"

#  FUNCTION TO SANITIZE FILE/FOLDER NAMES
def sanitize(name):
    # Remove characters not allowed in file/folder names on most systems
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '', name).strip()

#  STEP 1: Load folder mapping from Boostnote
# This maps internal folder keys to folder names for organizing notes
with open(FOLDER_JSON, 'r', encoding='utf-8') as f:
    folders_json = json.load(f)

folder_map = {f['key']: sanitize(f['name']) for f in folders_json.get('folders', [])}

#  STEP 2: Get all Boostnote .cson files
cson_files = [f for f in os.listdir(CSON_FOLDER) if f.endswith('.cson')]
total_files = len(cson_files)
print(f"Total notes to process: {total_files}\n")

#  STEP 3: Process and convert each note

failed_files = []   # To keep track of files that fail to parse
skipped_files = []  # To keep track of trashed notes

for i, file in enumerate(cson_files, start=1):
    full_path = os.path.join(CSON_FOLDER, file)

    # Try to load the CSON file using the cson module
    with open(full_path, 'rb') as f:
        try:
            note = cson.load(f)
        except Exception as e:
            print(f"[{i}/{total_files}] Failed to parse {file}: {e}")
            failed_files.append(file)
            continue

    # Skip notes that were marked as trashed in Boostnote
    if note.get("isTrashed"):
        skipped_files.append(file)
        continue

    # Resolve the folder path based on the folder key
    folder_key = note.get("folder")
    folder_name = sanitize(folder_map.get(folder_key, "Uncategorized"))
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    # Determine note title and markdown file name
    title = sanitize(note.get("title", "Untitled"))
    md_filename = os.path.join(folder_path, f"{title}.md")

    #  PRINT PROGRESS
    print(f"[{i}/{total_files}] Writing: {md_filename}")
    print(f"   - Title : {title}")
    print(f"   - Type  : {note.get('type')}")
    print(f"   - Folder: {folder_name}\n")

    #  WRITE THE MARKDOWN FILE
    try:
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            if note.get("type") == "MARKDOWN_NOTE":
                # Directly write the content of markdown notes
                md_file.write(note.get("content", ""))
            elif note.get("type") == "SNIPPET_NOTE":
                # For snippet notes, wrap each snippet in fenced code blocks
                snippets = note.get("snippets", [])
                show_titles = len(snippets) > 1

                for snippet in snippets:
                    name = snippet.get("name", "Snippet")
                    content = snippet.get("content", "")
                    if show_titles:
                        # Add snippet title if there are multiple snippets
                        md_file.write(f"### {name}\n\n")
                    md_file.write("```\n")
                    md_file.write(content)
                    md_file.write("\n```\n\n")
    except Exception as e:
        print(f"   !! Failed to write {md_filename}: {e}")

#  REPORT SKIPPED FILES
if skipped_files:
    print("\n Some files marked as trashed were skipped ")
    print(f"{len(skipped_files)} file(s) were marked as trashed:\n")
    for f in skipped_files:
        print(f"- {f}")

#  FINAL REPORT
if failed_files:
    print("\n Conversion completed with errors ")
    print(f"{len(failed_files)} file(s) failed to convert:\n")
    for f in failed_files:
        print(f"- {f}")
else:
    print("\n Conversion completed successfully! All files processed. ")
