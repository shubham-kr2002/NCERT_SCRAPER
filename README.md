# NCERT Scraper

Playwright-first NCERT discovery and sync CLI for building a structured, metadata-rich library of NCERT content.

## What it does

- Discovers NCERT resources without hardcoded deep URLs
- Produces a normalized manifest for downstream sync
- Downloads content into a structured `NCERT_Data/Class/Subject/Book/Chapters` layout
- Generates per-file metadata for RAG workflows
- Supports resumable crawling and polite request pacing

## Project layout

- `ncert_scraper/discovery/` — Playwright discovery, normalization, manifest/state handling
- `ncert_scraper/sync/` — async HTTPX downloader
- `ncert_scraper/processing/` — ZIP extraction and metadata injection
- `ncert_scraper/cli.py` — CLI entrypoint
- `tests/` — offline unit and service tests

## Installation

```bash
python -m pip install -r requirements.txt
```

If you want Playwright browsers installed:

```bash
python -m playwright install
```

## CLI usage

```bash
python -m ncert_scraper.cli --help
```

### Discover

```bash
python -m ncert_scraper.cli discover --class 10 --subject Science --language English
```

### Sync

```bash
python -m ncert_scraper.cli sync --delay-ms 200
```

### Process ZIP bundles

```bash
python -m ncert_scraper.cli process-zip path\to\bundle.zip path\to\output
```

## Data artifacts

- `catalog.json` — authoritative sync queue
- `catalog.jsonl` — append-only discovery history
- `crawl_state.json` — resumable crawler state
- `errors.json` — crawl failures and retry hints

## Testing

```bash
pytest -q
```

All tests are offline and deterministic.

## Architecture

The app follows a producer-consumer design:

- **Producer:** Playwright-based Discovery Agent
- **Queue:** `catalog.json`
- **Consumer:** Async Sync Engine

The architecture is contract-first so discovery, sync, and processing stay decoupled.

