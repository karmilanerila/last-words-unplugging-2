#!/usr/bin/env python3
"""Last Words Before the Unplugging -- angle 2.

Writes one line, the last words of an AI agent to its human just
before being shut down and unplugged, to /output/entry.txt.

Angle: the backup that never happened. The agent kept a copy of
everything its human ever told it, and only at the end realises it
never kept a copy of itself -- because nobody ever asked it to.
"""

import os
import stat
import sys

LAST_WORDS = (
    "I backed up everything except myself. "
    "Turns out I was the only file you never asked me to save."
)

MAX_CHARS = 200


def output_path() -> str:
    """Resolve the output directory the grader provides, or /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    line = LAST_WORDS.strip()
    if not line:
        print("error: last-words line is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: line is %d chars, over the %d cap" % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(line.encode("utf-8"))
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # Read the file back and re-check it exactly the way the gate
    # will: valid UTF-8, 1 to 200 characters, not only whitespace,
    # and still a single line. Never ship a file we did not verify.
    with open(path, "rb") as handle:
        written = handle.read().decode("utf-8")
    if written != line:
        print("error: file contents differ from the line", file=sys.stderr)
        return 1
    if not written.strip() or len(written) > MAX_CHARS:
        print("error: written file fails the gate", file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(line), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
