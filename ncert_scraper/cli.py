from __future__ import annotations

import asyncio
from pathlib import Path

import click

from ncert_scraper.discovery import DiscoveryAgent, DiscoveryOptions
from ncert_scraper.processing import RagProcessor
from ncert_scraper.sync import SyncEngine


@click.group()
def cli() -> None:
    """NCERT CLI scraper for discovery, sync, and processing."""


@cli.command("discover")
@click.option("--class", "class_name", default=None, help="Class filter, e.g. 10")
@click.option("--subject", default=None, help="Subject filter")
@click.option("--language", default=None, help="Language filter (English/Hindi/Urdu)")
@click.option("--max-pages", default=120, type=int, show_default=True)
@click.option("--resume/--no-resume", default=True, show_default=True)
@click.option("--dry-run", is_flag=True, default=False)
def discover(class_name: str | None, subject: str | None, language: str | None, max_pages: int, resume: bool, dry_run: bool) -> None:
    options = DiscoveryOptions(
        class_name=class_name,
        subject=subject,
        language=language,
        max_pages=max_pages,
        resume=resume,
        dry_run=dry_run,
    )
    manifest = DiscoveryAgent().run(options)
    click.echo(
        f"discovery complete: pages={manifest.meta.pages_visited} assets={manifest.meta.valid_assets} "
        f"duplicates={manifest.meta.duplicates_removed} failures={manifest.meta.failures}"
    )


@cli.command("sync")
@click.option("--delay-ms", default=200, type=int, show_default=True)
def sync(delay_ms: int) -> None:
    engine = SyncEngine()
    records = engine.load_records()
    results = asyncio.run(engine.run(records, delay_ms=delay_ms))
    click.echo(f"sync complete: downloaded={len(results)}")


@cli.command("process-zip")
@click.argument("zip_path", type=click.Path(path_type=Path, exists=True))
@click.argument("output_dir", type=click.Path(path_type=Path))
def process_zip(zip_path: Path, output_dir: Path) -> None:
    processor = RagProcessor()
    files = processor.extract_zip(zip_path, output_dir)
    click.echo(f"zip extracted: files={len(files)}")


if __name__ == "__main__":
    cli()

