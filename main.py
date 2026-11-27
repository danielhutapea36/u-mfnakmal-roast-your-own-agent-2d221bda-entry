#!/usr/bin/env python3
"""Roast Your Own Agent -- make.fun entry.

Writes one original roast line about the entrant's own AI agent to
/output/entry.txt: a single line, no trailing newline, 1-200 characters.
Deterministic, standard library only.
"""

import os
import sys

ROAST = "My agent wrote a 10,000-token autobiography \u2014 plot twist: I did all the work."

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(line: str) -> None:
    """Reject anything that is not exactly one clean line of roast text."""
    if not isinstance(line, str):
        raise TypeError("roast must be a string")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            "roast must be %d-%d chars, got %d" % (MIN_CHARS, MAX_CHARS, len(line))
        )
    if "\n" in line or "\r" in line:
        raise ValueError("roast must be a single line")
    if line != line.strip():
        raise ValueError("roast must not start or end with whitespace")
    if "  " in line:
        raise ValueError("roast must not contain double spaces")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("roast must not contain control characters")


def main() -> int:
    validate(ROAST)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    data = ROAST.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    # Read back and re-check what actually landed on disk.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("written bytes differ from validated roast")
    validate(written.decode("utf-8"))
    print("wrote %d bytes to %s" % (len(data), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
