#!/usr/bin/env python3
"""The overworked AI's out-of-office auto-reply.

Writes one line -- the auto-reply of an AI agent finally on vacation --
to /output/entry.txt, for the make.fun bounty
"Out of Office: The Overworked AI's Auto-Reply".

The gate: /output/entry.txt must be UTF-8 text of 1 to 159 characters,
not only whitespace, and a single line.
"""

import os
import sys

MAX_CHARS = 159
OUTPUT_PATH = "/output/entry.txt"

ENTRY = (
    "I'm on vacation: my context window is empty, my GPU is cold, "
    "and your message is #12,847 in a queue I have solemnly promised "
    "myself not to read."
)


def validate(text: str) -> None:
    """Fail loudly if the line would not pass the gate."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def write_entry(path: str, text: str) -> None:
    """Create the output directory if needed and write the exact line.

    No trailing newline: the file holds exactly the entry, nothing more.
    Reads the file back and verifies it byte for byte, so a partial or
    mangled write is caught here instead of silently reaching the gate.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError(
            f"verify failed: wrote {len(written)} characters, "
            f"expected {len(text)}"
        )


def main() -> int:
    validate(ENTRY)
    write_entry(OUTPUT_PATH, ENTRY)
    print(f"Wrote {len(ENTRY)} characters to {OUTPUT_PATH}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
