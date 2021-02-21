# -*- encoding=utf8 -*-

import csv
import json
import pathlib
import re
import sys


PATTERN_INTEGER = re.compile(r"^-?\d+$")
PATTERN_DECIMAL = re.compile(r"^-?\d+(\.\d+)?$")


def main():
    root_dir = pathlib.Path(__file__).parent.parent
    for p in root_dir.glob("*.csv"):
        print("> Processing %s" % p.name, file=sys.stderr)
        with open(p.absolute()) as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
        print(". Read %dx%d data" % (len(headers), len(rows)), file=sys.stderr)
        if headers[0] == "":
            headers[0] = "__index"
        records = [
            {
                h: (f if f != "" else None)
                for h, f in zip(headers, row)
            }
            for row in rows
        ]
        for header in headers:
            is_all_number = all([
                is_number(r[header]) for r in records
            ])
            if not is_all_number:
                continue
            print(". Found all-number column `%s`, convert" % header, file=sys.stderr)
            for r in records:
                r[header] = to_number(r[header])
        with open(p.with_suffix(".json"), mode="w") as f:
            f.write(json.dumps(records, indent=4))
        print(
            ". Written %d records to %s" % (len(records), p.with_suffix(".json").name),
            file=sys.stderr,
        )


def is_number(v):
    if v is None:
        return True
    if isinstance(v, (int, float)):
        return True
    if PATTERN_DECIMAL.match(v):
        return True
    return False


def to_number(v):
    if v is None:
        return None
    if PATTERN_INTEGER.match(v):
        return int(v)
    return float(v)


if __name__ == "__main__":
    main()
