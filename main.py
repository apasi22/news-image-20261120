#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the pre-rendered 20 November 2026 world-news image to the output
directory. The image was drawn fresh for this competition by draw.py
(Pillow, deterministic) and is shipped in this repository as entry.png.
Standard library only; no network; deterministic (a plain file copy).
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
