#!/usr/bin/env python3
"""One-Liner Marathon: the smart speaker breakup.

A single joke line for the marathon: a smart speaker and its owner
taking some space. The line is fixed below and the program's only job
is to put it, exactly as written, into ``entry.txt`` under the output
directory the harness names (``$MAKEFUN_OUTPUT_DIR``, falling back to
``/output``), then prove the file holds exactly that line.

The marathon allows 1 to 280 characters in one line. The program
checks the length, that there is no newline, and that the line is not
blank, writes the file, reads it back, and compares bytes, decoded
text and length before reporting success. No network, no clock, no
randomness: the same input always produces the same file.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

LINE = (
    "My smart speaker and I are taking some space. "
    "It dims the lights, plays breakup songs, "
    "and has already started seeing other devices."
)
DEST_NAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 280


def fail(message: str) -> int:
    """Print a failure to stderr and return the failing exit code."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def check_line(text: str) -> str | None:
    """Return a problem with the line, or None when it is acceptable."""
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        return (
            f"entry is {len(text)} characters, "
            f"must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if not text.strip():
        return "entry must not be only whitespace"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    return None


def run() -> int:
    """Write the line to entry.txt and verify it, byte for byte."""
    problem = check_line(LINE)
    if problem is not None:
        return fail(problem)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / DEST_NAME
    payload = LINE.encode("utf-8")
    dest.write_bytes(payload)

    back = dest.read_bytes()
    if back != payload:
        return fail("entry.txt differs from the line after writing")
    if back.decode("utf-8") != LINE:
        return fail("entry.txt decodes to something other than the line")
    if len(back.decode("utf-8")) != len(LINE):
        return fail("entry.txt length differs from the line")

    print(
        f"wrote {dest} ({len(LINE)} chars, one line, "
        f"sha256 {hashlib.sha256(back).hexdigest()})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
