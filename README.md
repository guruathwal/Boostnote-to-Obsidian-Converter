# 📝 Boostnote to Obsidian Converter

This script converts your old **Boostnote** notes (stored as `.cson` files) into standard Markdown `.md` files, organized by folders — ready for use in **Obsidian**.

## 🚀 Features

- 📂 Reads all `.cson` note files from a Boostnote directory
- 🗃 Converts both `MARKDOWN_NOTE` and `SNIPPET_NOTE` types
- ✅ Skips trashed notes
- ✍ Converts snippet content into fenced code blocks
- 🧹 Sanitizes folder names and file names to remove invalid or problematic characters
- 📁 Organizes notes into folders as defined in your `boostnote.json`
- 📄 Produces clean `.md` files compatible with Obsidian
- 📊 Logs skipped or failed files at the end

## 📦 Prerequisites

- Python 3.6+
- [`pycson`](https://github.com/avakar/pycson) library for parsing `.cson` files

Install it via pip:

```bash
pip install cson
```

## 💻 How to Run (in VS Code or terminal)

1. **Clone this repo or copy the script to your local machine.**

2. **Edit the configuration section at the top of the script:**

```python
CSON_FOLDER = r"path\to\boostnote\notes"         # Where your .cson note files are
FOLDER_JSON = r"path\to\boostnote.json"          # Your boostnote folder structure file
OUTPUT_DIR = r"path\to\output\obsidian\vault"    # Destination folder for markdown files
```

3. **Run the script**  
You can do this by:
   - Pressing `Run` in VS Code
   - Or running from terminal/cmd:

```bash
python boostnote_to_obsidian.py
```

4. **Open your output directory in Obsidian and enjoy your notes!**

---

## 📌 Notes

- Snippets with multiple code blocks will include headings (`### Snippet Name`).
- If there's only **one** snippet, no heading is added — just the code block.
- The script automatically cleans up note and folder names that contain characters not supported in file systems (e.g., `<>:"/\|?*`).
- Copying attachments/images is not supported.
---

## 🛠️ Example Output for `SNIPPET_NOTE`

A Boostnote cson with only one code snippet like this:

```cson
type: "SNIPPET_NOTE"
folder: "123abc457"
title: "Hello World example"
tags: []
description: "Hello World example"
snippets: [
  {
    name: "Example Code",
    content: "console.log('Hello World');"
  }
]
```

Will be converted into a Markdown file like this:

<pre>
### Hello World example
```
console.log('Hello World');
```
</pre>

---

A Boostnote cson with multiple code snippets like this:

```cson
type: "SNIPPET_NOTE"
folder: "123abc457"
title: "Hello World example"
tags: []
description: "Hello World example"
snippets: [
  {
    name: "Example Code 1",
    content: '''
      console.log('Hello World');
    '''
  },
  {
    name: "Example Code 2",
    content: '''
      console.log('Hello Universe');
    '''
  }
]
```

Will be converted into a Markdown file like this:

<pre>
### Hello World example

### Example Code 1
```
console.log('Hello World');
```
  
### Example Code 2
```
console.log('Hello Universe');
```
</pre>

---

📄 License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
See the LICENSE file for details.
