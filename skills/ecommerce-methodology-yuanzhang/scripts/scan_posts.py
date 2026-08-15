#!/usr/bin/env python3
"""Scan a local JSON export of posts for monetization-related themes.

This is a deterministic local pre-analysis. It does not fetch the web or
validate claims about revenue, sales, or case studies.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TERMS = [
    "赚钱", "收入", "月入", "闲鱼", "拼多多", "小红书", "抖音", "私域",
    "学员", "服务", "咨询", "差价", "二道贩子", "AI", "豆包", "飞书",
    "Codex", "WorkBuddy", "选品", "复购", "课程", "自媒体",
]


def load_records(path: Path) -> list[dict[str, Any]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(obj, list):
        rows = obj
    elif isinstance(obj, dict) and isinstance(obj.get("records"), list):
        rows = obj["records"]
    else:
        raise ValueError("JSON must be a list or an object containing records")
    return [row for row in rows if isinstance(row, dict)]


def text_of(row: dict[str, Any]) -> str:
    return str(row.get("text") or row.get("raw_text") or "").strip()


def metric(row: dict[str, Any], key: str) -> int:
    value = (row.get("metrics") or {}).get(key)
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1


def compact(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", text)
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--top", default=20, type=int)
    args = parser.parse_args()

    rows = load_records(args.input)
    counts = Counter()
    selected = []
    missing = Counter()

    for row in rows:
        text = text_of(row)
        lowered = text.lower()
        for term in TERMS:
            if term.lower() in lowered:
                counts[term] += 1
        if any(term.lower() in lowered for term in TERMS):
            selected.append(row)
        for key in ("id", "url", "text"):
            if not row.get(key) and not (key == "text" and row.get("raw_text")):
                missing[key] += 1

    top = []
    for row in sorted(selected, key=lambda item: metric(item, "views"), reverse=True)[: args.top]:
        top.append(
            {
                "views": None if metric(row, "views") < 0 else metric(row, "views"),
                "likes": None if metric(row, "likes") < 0 else metric(row, "likes"),
                "replies": None if metric(row, "replies") < 0 else metric(row, "replies"),
                "bookmarks": None if metric(row, "bookmarks") < 0 else metric(row, "bookmarks"),
                "url": row.get("url"),
                "text": compact(text_of(row)),
            }
        )

    print(json.dumps({
        "records": len(rows),
        "theme_keyword_hits": dict(counts),
        "records_with_monetization_terms": len(selected),
        "missing_fields": dict(missing),
        "top_monetization_samples_by_views": top,
        "interpretation_note": "Keyword hits and interaction metrics are leads for qualitative review, not proof of causation or revenue.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
