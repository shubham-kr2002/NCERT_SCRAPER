# NCERT-RAG-Sync Architecture

## 1. System Design
The system follows a **Producer-Consumer** architecture with contract-first data flow.

- **Producer (Discovery Agent):** Playwright-driven crawler that discovers and normalizes NCERT assets.
- **Queue contract:** `catalog.json` is the single source of truth consumed by Sync Engine.
- **Audit trail:** `catalog.jsonl` stores append-only discovery events.
- **Recovery state:** `crawl_state.json` supports resume and idempotent reruns.
- **Consumer (Sync Engine):** Async downloader that materializes files and metadata into the target hierarchy.

## 2. Component Breakdown

### A. Discovery Agent (Playwright-first)
- `BrowserSession`: headless Chromium lifecycle and context setup.
- `RouteExplorer`: deterministic page traversal with in-domain link expansion.
- `EntityNormalizer`: transforms raw links into typed `DiscoveryRecord`.
- `ManifestBuilder`: deduplicates by stable ID and writes manifest artifacts.
- `StateStore`: checkpoint queue/visited state for restart safety.

Discovery guarantees:
- No hardcoded deep NCERT URLs.
- Stable record IDs based on class/subject/book/chapter/language.
- Structured crawl errors with retryability hints.

### B. Manifest Contract
- `catalog.json`: `{ meta, records, errors }` snapshot for Sync Engine.
- `catalog.jsonl`: per-record append log for audit and debugging.
- `errors.json`: extraction/navigation failures.
- `crawl_state.json`: resumable queue and visited set checkpoint.

### C. Sync Engine (Asyncio + HTTPX)
- Bounded concurrency (`Semaphore(5)` default).
- HEAD validation before GET.
- Output structure:
  - `NCERT_Data/<Class>/<Subject>/<Book>/Chapters/<Class_Subject_Chapter>.pdf`
  - sibling `<file>.metadata.json`
- Metadata fields include class/subject/book/chapter/language/source URL/download URL/book ID.

### D. RAG Processor
- ZIP extraction for NCERT bundles.
- Metadata injection for downstream chunking/retrieval.

## 3. Data Models
- `DiscoveryRecord`: class/subject/book/chapter/language/book_id/source_page/download_url/breadcrumbs/stable_id
- `CrawlMeta`: crawl counters, timestamps, schema version
- `CrawlError`: stage, message, retryable flag
- `DiscoveryManifest`: aggregate payload used by sync

## 4. CLI Surface
- `discover --class --subject --language --max-pages --resume --dry-run`
- `sync --delay-ms`
- `process-zip <zip_path> <output_dir>`

## 5. Tech Stack
- CLI: `Click`
- Discovery automation: `Playwright`
- Networking: `HTTPX`
- Validation/modeling: `Pydantic`
- Packaging/testing: `setuptools`, `pytest`
