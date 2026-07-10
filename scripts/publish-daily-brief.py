#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GENERATOR = (
    Path.home()
    / "Library/CloudStorage/Dropbox/AI/personal-brand/daily-brief-site"
)
DAYPART_ORDER = {
    "morning": 1,
    "afternoon": 2,
    "evening": 3,
}


def brief_sort_key(path: Path) -> tuple[str, int, str]:
    match = re.match(r"(\d{4}-\d{2}-\d{2})(?:-([a-z]+))?$", path.stem)
    if not match:
        return (path.stem, 99, path.stem)
    date, daypart = match.groups()
    return (date, DAYPART_ORDER.get(daypart or "morning", 1), path.stem)


def dated_briefs(generator: Path) -> list[str]:
    content_dir = generator / "content" / "briefs"
    dates = [path.stem for path in sorted(content_dir.glob("*.md"), key=brief_sort_key)]
    if not dates:
        raise SystemExit(f"No Markdown briefs found in {content_dir}")
    return dates


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise SystemExit(f"Missing expected build output: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def publish(generator: Path, include_latest_archive: bool, trmnl_only: bool) -> None:
    generator = generator.expanduser().resolve()
    subprocess.run(["python3", "scripts/build.py"], cwd=generator, check=True)

    dates = dated_briefs(generator)
    latest = dates[-1]
    public = generator / "public"

    if not trmnl_only:
        copy_file(public / "index.html", SITE_ROOT / "index.html")
        for asset_name in (
            "favicon-16x16.png",
            "favicon-32x32.png",
            "apple-touch-icon.png",
            "site-icon-512.png",
        ):
            asset = public / asset_name
            if asset.exists():
                copy_file(asset, SITE_ROOT / asset_name)

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

    trmnl_public = public / "trmnl"
    if trmnl_public.exists():
        copy_file(trmnl_public / "index.html", SITE_ROOT / "trmnl.html")
        trmnl_dir = SITE_ROOT / "trmnl"
        trmnl_dir.mkdir(exist_ok=True)

        trmnl_feed = trmnl_public / "feed.json"
        if trmnl_feed.exists():
            copy_file(trmnl_feed, trmnl_dir / "feed.json")

        for archive in sorted(
            (trmnl_public / "briefs").glob("*/index.html"),
            key=lambda path: brief_sort_key(path.parent),
        ):
            copy_file(archive, trmnl_dir / f"{archive.parent.name}.html")
        print("Published TRMNL brief to trmnl.html.")

    if trmnl_only:
        print("Skipped browser brief publication (--trmnl-only).")
    else:
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
        default=True,
        help="Also write the latest brief to briefs/YYYY-MM-DD.html.",
    )
    parser.add_argument(
        "--exclude-latest-archive",
        action="store_false",
        dest="include_latest_archive",
        help="Skip writing the latest brief archive and publish it only at index.html.",
    )
    parser.add_argument(
        "--trmnl-only",
        action="store_true",
        help="Publish only trmnl.html and its dated terminal archives.",
    )
    args = parser.parse_args()
    publish(args.generator, args.include_latest_archive, args.trmnl_only)


if __name__ == "__main__":
    main()
