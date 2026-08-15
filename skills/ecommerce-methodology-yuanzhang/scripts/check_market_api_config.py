#!/usr/bin/env python3
"""Check whether the two market API configurations are present.

This script intentionally does not make network requests and never prints
secret values. A real adapter/connector must perform the authenticated calls.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any


def present(name: str) -> bool:
    return bool(os.environ.get(name, "").strip())


def status(platform: str, base: str, auth_groups: list[list[str]]) -> dict[str, Any]:
    missing = []
    if not present(base):
        missing.append(base)
    if not any(all(present(name) for name in group) for group in auth_groups):
        missing.append("one supported authorization set")
    return {
        "platform": platform,
        "configured": not missing,
        "missing": missing,
        "network_test": "not_run",
    }


def main() -> int:
    result = {
        "1688": status(
            "1688",
            "ECOMMERCE_1688_API_BASE_URL",
            [
                ["ECOMMERCE_1688_ACCESS_TOKEN"],
                ["ECOMMERCE_1688_API_KEY"],
                ["ECOMMERCE_1688_APP_KEY", "ECOMMERCE_1688_APP_SECRET"],
            ],
        ),
        "pdd": status(
            "pdd",
            "ECOMMERCE_PDD_API_BASE_URL",
            [
                ["ECOMMERCE_PDD_ACCESS_TOKEN"],
                ["ECOMMERCE_PDD_API_KEY"],
                ["ECOMMERCE_PDD_CLIENT_ID", "ECOMMERCE_PDD_CLIENT_SECRET"],
            ],
        ),
    }
    result["ready_for_api_calls"] = all(item["configured"] for item in result.values())
    result["note"] = "Presence check only; credentials are not displayed and no network request was made."
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready_for_api_calls"] else 2


if __name__ == "__main__":
    sys.exit(main())
