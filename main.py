#!/usr/bin/env python3
"""The One-Line Laugh entry.

Writes one original funny line (<=200 chars) to /output/entry.txt,
deterministically: same bytes on every run.
"""
import os
import sys

LINE = (
    "My toaster has two settings: lightly golden, and a full "
    "smoke-alarm audition."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(line):
    """Check the line against the sealed scorer's gate, without asserts.

    Asserts vanish under python -O, so the gate is enforced with explicit
    checks that always run, and failures name the broken rule.
    """
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line is {len(line)} chars, gate needs 1-200")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main():
    try:
        validate(LINE)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        raise SystemExit(1)
    # Deterministic by construction: fixed constant, no randomness, no
    # timestamps, explicit UTF-8 encoding, no trailing newline added.
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read back what landed on disk and prove it is exactly the line the
    # judge will read: same bytes, still one line, still within the gate.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("entry.txt on disk differs from LINE", file=sys.stderr)
        raise SystemExit(1)
    if raw.count(b"\n") != 0:
        print("entry.txt must hold exactly one line", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
