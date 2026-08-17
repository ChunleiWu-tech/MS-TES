from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(r"C:\Users\吴春雷\Desktop\TES\0722\TES_GitHub_Update_V10_1_20260817_232335")
REPO = ROOT / "GitHub_Repository_Files"
ARCHIVES = [
    REPO / "TES_v10.1.0_upstream_source_only.zip",
    REPO / "TES_v10.1.0_postprocess_source_only.zip",
]

FORBIDDEN = {
    "personal_windows_path": re.compile(r"(?i)[a-z]:[\\/](?:users|documents and settings)[\\/]"),
    "workspace_drive_path": re.compile(r"(?i)\b[ce]:[\\/](?:桌面1|users)[\\/]"),
    "local_file_uri": re.compile(r"(?i)file://"),
    "github_token": re.compile(r"(?i)\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "openai_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "assigned_secret": re.compile(r"(?i)\b(?:password|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
}


def scan_text(label: str, payload: bytes, hits: list[dict[str, str]]) -> None:
    text = payload.decode("utf-8", errors="ignore")
    for kind, pattern in FORBIDDEN.items():
        match = pattern.search(text)
        if match:
            hits.append({"entry": label, "kind": kind, "match": match.group(0)[:120]})


def scan_nested_zip(label: str, payload: bytes, hits: list[dict[str, str]]) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as nested:
            for name in nested.namelist():
                if name.endswith("/"):
                    continue
                info = nested.getinfo(name)
                if info.file_size > 12 * 1024 * 1024:
                    continue
                nested_payload = nested.read(name)
                scan_text(f"{label}!{name}", nested_payload, hits)
    except zipfile.BadZipFile:
        return


def audit_archive(path: Path) -> dict[str, object]:
    forbidden_hits: list[dict[str, str]] = []
    manifest_missing: list[str] = []
    manifest_mismatch: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        casefold_unique = len({name.casefold() for name in names}) == len(names)
        manifest_name = next(name for name in names if name.endswith("/PACKAGE_MANIFEST_SHA256.csv"))
        prefix = manifest_name[: -len("PACKAGE_MANIFEST_SHA256.csv")]
        manifest = list(csv.DictReader(io.StringIO(archive.read(manifest_name).decode("utf-8-sig"))))
        name_map = {name[len(prefix) :]: name for name in names if name.startswith(prefix)}
        for row in manifest:
            relative = row["relative_path"]
            member = name_map.get(relative)
            if member is None:
                manifest_missing.append(relative)
                continue
            payload = archive.read(member)
            if len(payload) != int(row["size_bytes"]) or hashlib.sha256(payload).hexdigest() != row["sha256"]:
                manifest_mismatch.append(relative)
        for name in names:
            info = archive.getinfo(name)
            if info.file_size > 12 * 1024 * 1024:
                continue
            payload = archive.read(name)
            scan_text(name, payload, forbidden_hits)
            if name.lower().endswith((".zip", ".xlsx", ".xlsm")):
                scan_nested_zip(name, payload, forbidden_hits)
        forbidden_generated = [
            name for name in names
            if re.search(r"/outputs/(?:tables|qc|main_figures|supplementary_figures)/.+", name)
        ]
        forbidden_runtime = [name for name in names if "/.venv/" in name or "/__pycache__/" in name]
        bad_member = archive.testzip()
    passed = not any([
        forbidden_hits,
        manifest_missing,
        manifest_mismatch,
        forbidden_generated,
        forbidden_runtime,
        bad_member,
        not casefold_unique,
    ])
    return {
        "archive": path.name,
        "status": "PASS" if passed else "FAIL",
        "members": len(names),
        "casefold_unique": casefold_unique,
        "zip_test": "PASS" if bad_member is None else bad_member,
        "manifest_rows": len(manifest),
        "manifest_missing": manifest_missing,
        "manifest_mismatch": manifest_mismatch,
        "forbidden_generated_entries": forbidden_generated,
        "forbidden_runtime_entries": forbidden_runtime,
        "personal_path_or_secret_hits": forbidden_hits,
    }


def main() -> None:
    records = [audit_archive(path) for path in ARCHIVES]
    report = {
        "status": "PASS" if all(record["status"] == "PASS" for record in records) else "FAIL",
        "target": "public GitHub repository and versioned DOI archive",
        "archives": records,
    }
    (ROOT / "PUBLIC_ARCHIVE_AUDIT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()

