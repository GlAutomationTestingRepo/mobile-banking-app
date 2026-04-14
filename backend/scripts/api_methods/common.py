"""Shared helpers for manual API method scripts."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from uuid import uuid4


BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def unique_suffix() -> str:
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{now}_{uuid4().hex[:6]}"


def request_json(method: str, path: str, payload: dict | None = None, params: dict | None = None) -> tuple[int, dict]:
    url = f"{BASE_URL}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    data = None
    headers: dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"detail": body}
        return exc.code, parsed


def ask_int(prompt: str, allow_empty: bool = False) -> int | None:
    while True:
        raw = input(prompt).strip()
        if allow_empty and raw == "":
            return None
        if raw.isdigit():
            return int(raw)
        print("Please enter a valid numeric value.")

