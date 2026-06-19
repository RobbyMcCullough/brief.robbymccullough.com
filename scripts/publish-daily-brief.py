#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GENERATOR = (
    Path.home()
    / "Library/CloudStorage/Dropbox/AI/personal-brand/daily-brief-site"
)


def dated_briefs(generator: Path) -> list[str]:
    content_dir = generator / "content" / "briefs"
    dates = sorted(path.stem for path in content_dir.glob("*.md"))
    if not dates:
        raise SystemExit(f"No Markdown briefs found in {content_dir}")
    return dates


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise SystemExit(f"Missing expected build output: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def publish(generator: Path, include_latest_archive: bool) -> None:
    generator = generator.expanduser().resolve()
    subprocess.run(["python3", "scripts/build.py"], cwd=generator, check=True)

    dates = dated_briefs(generator)
    latest = dates[-1]
    public = generator / "public"

    copy_file(public / "index.html", SITE_ROOT / "index.html")

    archive_dates = dates if include_latest_archive else dates[:-1]
    briefs_dir = SITE_ROOT / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    for date in archive_dates:
        copy_file(
            public / "briefs" / date / "index.html",
            briefs_dir / f"{date}.html",
        )

    latest_archive = briefs_dir / f"{latest}.html"
    if not include_latest_archive and latest_archive.exists():
        latest_archive.unlink()

    feed = public / "feed.json"
    if feed.exists():
        copy_file(feed, SITE_ROOT / "feed.json")

    print(f"Published latest brief to index.html: {latest}")
    if archive_dates:
        print(f"Archived date-named briefs through: {archive_dates[-1]}")
    else:
        print("No past briefs to archive yet.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build the personal-brand daily brief site and copy the live files "
            "into this DigitalOcean/Dropbox site repo."
        )
    )
    parser.add_argument(
        "--generator",
        type=Path,
        default=DEFAULT_GENERATOR,
        help=f"Path to the generator repo. Default: {DEFAULT_GENERATOR}",
    )
    parser.add_argument(
        "--include-latest-archive",
        action="store_true",
        help="Also write the latest brief to briefs/YYYY-MM-DD.html.",
    )
    args = parser.parse_args()
    publish(args.generator, args.include_latest_archive)


if __name__ == "__main__":
    main()
