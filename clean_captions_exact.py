#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Clean CSV:
- Remove entire sentences in the caption (or specified column) that contain an exact whole-word match of 'lighting' / 'illumination' / 'light'
- Optionally keep a backup of the original column
- Optionally drop rows that become empty after cleaning
- By default, replace internal newlines in all string columns with spaces to ensure “one record per line” on export
"""

import argparse
import csv
import re
import sys
from typing import Optional
import pandas as pd

# Match **whole words** only; no letters/digits/underscore/hyphen on either side
# (avoid matching light-colored / highlight / daylight / lights / back-lighting)
# WORD_REGEX = re.compile(r'(?i)(?<![A-Za-z0-9_-])(lighting|illumination|light)(?![A-Za-z0-9_-])')
WORD_REGEX = re.compile(r'(?i)(?<![A-Za-z0-9_-])(648746456465465465456)(?![A-Za-z0-9_-])')

# Sentence splitting (by .?!, keep the ending punctuation); we first turn internal newlines into spaces, then split
SENT_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')

def flatten_newlines(value: Optional[str]) -> Optional[str]:
    """Replace \r\n / \n / \r with spaces and collapse extra whitespace."""
    if isinstance(value, str):
        text = value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        text = re.sub(r"\s+", " ", text).strip()
        return text
    return value

def clean_caption(text: Optional[str]) -> Optional[str]:
    """Remove entire sentences containing target words; match whole words only."""
    if not isinstance(text, str) or not text.strip():
        return text
    text = flatten_newlines(text)
    sentences = SENT_SPLIT_REGEX.split(text) if text else []
    kept = [s for s in sentences if not WORD_REGEX.search(s)]
    cleaned = " ".join(kept).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def main():
    parser = argparse.ArgumentParser(
        description="Remove entire sentences in the caption column that contain whole-word matches of 'lighting' / 'illumination' / 'light', and ensure exported CSV has one record per line."
    )
    parser.add_argument("-i", "--input", required=True, help="Input CSV path")
    parser.add_argument("-o", "--output", required=True, help="Output CSV path")
    parser.add_argument("-c", "--column", default="caption", help="Column name to process (default: caption)")
    parser.add_argument("--keep-original", action="store_true",
                        help="Keep the original column as <column>_orig, and overwrite the original column with the cleaned result")
    parser.add_argument("--drop-empty", action="store_true",
                        help="Drop rows where the target column becomes empty after cleaning")
    parser.add_argument("--encoding", default="utf-8", help="CSV encoding (default: utf-8)")
    parser.add_argument("--sep", default=",", help="CSV delimiter (default: ,)")
    parser.add_argument("--no-flatten-all", dest="no_flatten_all", action="store_true",
                        help="By default, replace newlines with spaces in ALL string columns; set this flag to disable that behavior")
    args = parser.parse_args()

    # Read
    try:
        df = pd.read_csv(
            args.input,
            encoding=args.encoding,
            sep=args.sep,
            dtype=str,                    # Read all columns as strings to avoid numeric casting changing output format
            quoting=csv.QUOTE_MINIMAL,    # Compatible with commas/quotes/newlines (we’ll remove internal newlines later)
            keep_default_na=False         # Prevent empty strings from turning into NaN
        )
    except Exception as e:
        print(f"[Read failed] {e}", file=sys.stderr)
        sys.exit(1)

    if args.column not in df.columns:
        print(f"[Error] Column not found: {args.column}. Available columns: {list(df.columns)}", file=sys.stderr)
        sys.exit(2)

    # Optional backup
    if args.keep_original:
        backup_col = f"{args.column}_orig"
        if backup_col in df.columns:
            print(f"[Note] Backup column {backup_col} already exists and will be overwritten.", file=sys.stderr)
        df[backup_col] = df[args.column]

    # Process target column
    df[args.column] = df[args.column].apply(clean_caption)

    # Optionally: drop rows that became empty after cleaning
    if args.drop_empty:
        before = len(df)
        df = df[~(df[args.column].isna() | (df[args.column].str.strip() == ""))]
        print(f"[Info] Removed rows with empty {args.column}: {before - len(df)}", file=sys.stderr)

    # Ensure one record per line on export: remove internal newlines from **all string columns**
    if not args.no_flatten_all:
        str_cols = [col for col in df.columns]  # Treat all columns as strings for cleaning (dtype=str above ensures this)
        for col in str_cols:
            df[col] = df[col].apply(flatten_newlines)

    # Write: explicitly set line terminator to '\n'
    try:
        df.to_csv(
            args.output,
            index=False,
            encoding=args.encoding,
            sep=args.sep,
            quoting=csv.QUOTE_MINIMAL,
            line_terminator="\n"
        )
        print(f"[Done] Wrote: {args.output}")
    except TypeError:
        # Compatibility for some older pandas versions that use the 'lineterminator' parameter name
        df.to_csv(
            args.output,
            index=False,
            encoding=args.encoding,
            sep=args.sep,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n"
        )
        print(f"[Done] Wrote (compat with older pandas parameter name): {args.output}")
    except Exception as e:
        print(f"[Write failed] {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
