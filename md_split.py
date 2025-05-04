#!/usr/bin/env python3
# split_md.py

import argparse
import glob
import os
import re
import sys

def sanitize_header(text):
    """
    Strip Markdown bold/italic/backticks/etc., replace any run of
    non-word chars with a single underscore, trim, and prefix with underscore.
    """
    # remove Markdown formatting chars
    cleaned = re.sub(r'[*_`~\[\]]+', '', text)
    cleaned = cleaned.strip()
    # replace any sequence of non-word chars with underscore
    cleaned = re.sub(r'\W+', '_', cleaned, flags=re.UNICODE)
    # strip leading/trailing underscores
    cleaned = cleaned.strip('_')
    return f"_{cleaned}.md"

def split_markdown(input_path, output_dir):
    """
    Split one Markdown file by level-1 headers into separate .md files
    under output_dir.
    """
    if not os.path.isfile(input_path):
        print(f"[!] Skipping (not a file): {input_path}", file=sys.stderr)
        return

    with open(input_path, encoding='utf-8') as f:
        lines = f.readlines()

    header_re = re.compile(r'^#\s+(.*)')
    current_header = None
    buffer = []

    for line in lines:
        m = header_re.match(line)
        if m:
            # flush previous
            if current_header is not None and buffer:
                fname = sanitize_header(current_header)
                out_path = os.path.join(output_dir, fname)
                with open(out_path, 'w', encoding='utf-8') as out_f:
                    out_f.writelines(buffer)
                print(f"→ Written: {out_path}")

            # start new
            current_header = m.group(1)
            buffer = [line]
        else:
            if current_header is not None:
                buffer.append(line)

    # flush last
    if current_header and buffer:
        fname = sanitize_header(current_header)
        out_path = os.path.join(output_dir, fname)
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(buffer)
        print(f"→ Written: {out_path}")

def main():
    p = argparse.ArgumentParser(
        description="Split Markdown file(s) into per-`# ` section files."
    )
    p.add_argument("input_path",
                   help="Path to .md file or directory of .md files")
    p.add_argument("output_dir",
                   help="Directory to place the split files into")
    args = p.parse_args()

    inp = args.input_path
    out = args.output_dir
    os.makedirs(out, exist_ok=True)

    if os.path.isdir(inp):
        # process every .md in this directory (non-recursive)
        md_files = glob.glob(os.path.join(inp, "*.md"))
        if not md_files:
            print(f"[!] No .md files found in {inp}", file=sys.stderr)
            sys.exit(1)
        for md in md_files:
            base = os.path.splitext(os.path.basename(md))[0]
            subdir = os.path.join(out, base)
            os.makedirs(subdir, exist_ok=True)
            print(f"\nProcessing {md} → {subdir}/")
            split_markdown(md, subdir)
    else:
        # single file
        split_markdown(inp, out)

if __name__ == "__main__":
    main()