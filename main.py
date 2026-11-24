"""Write one funny AI weekly status report line to /output/entry.txt.

Standard library only. The file's content is exactly the line's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be a single line of at most 200
characters, so the line is validated before it is written.
"""

import os

LINE = (
    "Weekly status: I saved you 20 hours by finishing your work in "
    "4 minutes, then spent the remaining 19 hours and 56 minutes "
    "waiting for you to approve one checkbox."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line):
    """The bounty gate: one line, 1-200 characters, non-blank."""
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    if line != line.strip() or not line.strip():
        raise ValueError("entry must not be blank or padded")
    if not 1 <= len(line) <= 200:
        raise ValueError("entry must be 1-200 characters")
    # Exactly one line: no line-break character anywhere, including
    # the Unicode line/paragraph separators and vertical whitespace
    # that some readers still render as a second line.
    line_breaks = "\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029"
    if any(char in line for char in line_breaks):
        raise ValueError("entry must be a single line")
    return line


def write_entry(line):
    """Write the line's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(line.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    line = validate(LINE)
    write_entry(line)


if __name__ == "__main__":
    main()
