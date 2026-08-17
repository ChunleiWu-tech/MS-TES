from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import shutil
import zipfile
from pathlib import Path


WORKSPACE = Path(r"C:\Users\吴春雷\Desktop\TES\0722")
RUN_ROOT = WORKSPACE / "TES_V10_1_PDF_Run_20260816_021427"
PACKAGE_ROOT = WORKSPACE / "TES_GitHub_Update_V10_1_20260817_232335"
REPO_FILES = PACKAGE_ROOT / "GitHub_Repository_Files"
OVERRIDES = PACKAGE_ROOT / "package_overrides"
RELEASE_ID = "TES-PUB-V10.1.0-MANUSCRIPT-AUDITED-20260816"
FIXED_ZIP_TIME = (2026, 8, 17, 0, 0, 0)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def collect_tree(root: Path, relative_dir: str) -> dict[str, bytes]:
    base = root / relative_dir
    records: dict[str, bytes] = {}
    if not base.exists():
        return records
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        if any(part in {".venv", "__pycache__", ".git"} for part in path.parts):
            continue
        if path.suffix.lower() in {".pyc", ".pyo"}:
            continue
        records[path.relative_to(root).as_posix()] = path.read_bytes()
    return records


def collect_named(root: Path, names: list[str]) -> dict[str, bytes]:
    records: dict[str, bytes] = {}
    for name in names:
        path = root / name
        if path.is_file():
            records[name] = path.read_bytes()
    return records


def manifest_bytes(files: dict[str, bytes]) -> tuple[bytes, bytes]:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["relative_path", "size_bytes", "sha256"])
    checksum_lines = []
    for name in sorted(files):
        checksum = sha256_bytes(files[name])
        writer.writerow([name, len(files[name]), checksum])
        checksum_lines.append(f"{checksum}  {name}")
    return stream.getvalue().encode("utf-8"), ("\n".join(checksum_lines) + "\n").encode("utf-8")


def write_zip(path: Path, top_folder: str, files: dict[str, bytes]) -> dict[str, object]:
    manifest, checksums = manifest_bytes(files)
    files = dict(files)
    files["PACKAGE_MANIFEST_SHA256.csv"] = manifest
    files["PACKAGE_SHA256SUMS.txt"] = checksums
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative_path in sorted(files):
            info = zipfile.ZipInfo(f"{top_folder}/{relative_path}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if relative_path.endswith(".sh") else 0o644
            info.external_attr = mode << 16
            archive.writestr(info, files[relative_path])
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        names = [name for name in archive.namelist() if not name.endswith("/")]
        max_member = max(archive.getinfo(name).file_size for name in names)
    if bad is not None:
        raise RuntimeError(f"Corrupt ZIP member: {bad}")
    return {
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "members": len(names),
        "largest_member_bytes": max_member,
        "zip_integrity": "PASS",
    }


def validate_python(files: dict[str, bytes], package: str) -> int:
    count = 0
    for name, payload in files.items():
        if not name.endswith(".py"):
            continue
        ast.parse(payload.decode("utf-8-sig"), filename=f"{package}/{name}")
        count += 1
    return count


def build_upstream() -> dict[str, object]:
    root = RUN_ROOT / "upstream_reproducible_code"
    top_names = [
        "RELEASE_ID.txt", "RELEASE_NOTES.md", "RUN_FULL_RECOMPUTE.bat",
        "RUN_FULL_RECOMPUTE.sh", "RUN_GUIDE.md", "RUN_SMOKE_TEST.bat",
        "RUN_SMOKE_TEST.sh", "SETUP_ENV.bat", "SETUP_ENV.sh",
        "SOURCE_VALIDATION_REPORT.md", "requirements-lock.txt", "requirements.txt",
    ]
    files = collect_named(root, top_names)
    for folder in ["config", "data", "docs", "src"]:
        files.update(collect_tree(root, folder))
    files["README.md"] = (OVERRIDES / "upstream_README.md").read_bytes()
    files["outputs/README.md"] = (root / "outputs" / "README.md").read_bytes()
    for shared in ["LICENSE", "DATA_LICENSE.md", "THIRD_PARTY_NOTICES.md"]:
        files[shared] = (RUN_ROOT / shared).read_bytes()
    files["SOURCE_PACKAGE_STATUS.json"] = json.dumps(
        {
            "status": "PASS",
            "release_id": RELEASE_ID,
            "package_type": "source_only_upstream",
            "generated_results_bundled": False,
            "registered_inputs_bundled": True,
            "raw_database_archives_bundled": True,
            "registered_mc_iterations": 20000,
            "excluded_generated_output_bytes": 357375394,
            "validation_basis": "Full upstream and post-processing release pipelines passed before source-only packaging.",
        },
        indent=2,
    ).encode("utf-8")
    python_files = validate_python(files, "upstream_reproducible_code")
    result = write_zip(REPO_FILES / "TES_v10.1.0_upstream_source_only.zip", "upstream_reproducible_code", files)
    result["python_files_syntax_checked"] = python_files
    result["contains_generated_tables"] = any(name.startswith("outputs/tables/") for name in files)
    result["contains_generated_qc"] = any(name.startswith("outputs/qc/") for name in files)
    return result


def build_postprocess() -> dict[str, object]:
    root = RUN_ROOT / "postprocess_reproducible_code"
    top_names = [
        "RELEASE_ID.txt", "RELEASE_NOTES.md", "RUN_GUIDE.md", "RUN_POSTPROCESS.bat",
        "RUN_POSTPROCESS.sh", "SETUP_ENV.bat", "SETUP_ENV.sh",
        "SOURCE_VALIDATION_REPORT.md", "SYNC_UPSTREAM_OUTPUTS.bat",
        "SYNC_UPSTREAM_OUTPUTS.sh", "requirements-lock.txt", "requirements.txt",
    ]
    files = collect_named(root, top_names)
    for folder in ["config", "docs", "src"]:
        files.update(collect_tree(root, folder))
    files["README.md"] = (OVERRIDES / "postprocess_README.md").read_bytes()
    files["data/README.md"] = (root / "data" / "README.md").read_bytes()
    files["outputs/README.md"] = (root / "outputs" / "README.md").read_bytes()
    for shared in ["LICENSE", "DATA_LICENSE.md", "THIRD_PARTY_NOTICES.md"]:
        files[shared] = (RUN_ROOT / shared).read_bytes()
    files["SOURCE_PACKAGE_STATUS.json"] = json.dumps(
        {
            "status": "PASS",
            "release_id": RELEASE_ID,
            "package_type": "source_only_postprocess",
            "generated_figures_bundled": False,
            "synced_upstream_results_bundled": False,
            "main_figures": 6,
            "supplementary_figures": 12,
            "postprocess_checks_passed": 42,
            "postprocess_checks_total": 42,
            "validation_basis": "Full pipeline and final PDF rendering passed before source-only packaging.",
        },
        indent=2,
    ).encode("utf-8")
    python_files = validate_python(files, "postprocess_reproducible_code")
    result = write_zip(REPO_FILES / "TES_v10.1.0_postprocess_source_only.zip", "postprocess_reproducible_code", files)
    result["python_files_syntax_checked"] = python_files
    result["contains_virtual_environment"] = any(".venv" in name.split("/") for name in files)
    result["contains_generated_figures"] = any(name.startswith("outputs/main_figures/") or name.startswith("outputs/supplementary_figures/") for name in files)
    return result


def copy_repository_files() -> None:
    shutil.copy2(RUN_ROOT / "upstream_reproducible_code" / "requirements.txt", REPO_FILES / "requirements.txt")
    shutil.copy2(RUN_ROOT / "upstream_reproducible_code" / "requirements-lock.txt", REPO_FILES / "requirements-lock.txt")


def write_outer_checksums() -> None:
    paths = sorted(path for path in REPO_FILES.iterdir() if path.is_file() and path.name != "SHA256SUMS.txt")
    lines = [f"{sha256_file(path)}  {path.name}" for path in paths]
    (REPO_FILES / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPO_FILES.mkdir(parents=True, exist_ok=True)
    copy_repository_files()
    upstream = build_upstream()
    postprocess = build_postprocess()
    write_outer_checksums()
    report = {
        "status": "PASS",
        "release_id": RELEASE_ID,
        "target_repository": "https://github.com/ChunleiWu-tech/MS-TES",
        "upstream": upstream,
        "postprocess": postprocess,
        "all_browser_upload_files_below_25MiB": all(
            path.stat().st_size < 25 * 1024 * 1024 for path in REPO_FILES.iterdir() if path.is_file()
        ),
        "repository_file_count": len([path for path in REPO_FILES.iterdir() if path.is_file()]),
    }
    (PACKAGE_ROOT / "BUILD_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

