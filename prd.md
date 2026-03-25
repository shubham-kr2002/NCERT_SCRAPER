# Product Requirements Document: NCERT CLI Scraper

## 1. Objective
To create a high-speed, CLI-based utility that downloads the entire NCERT library into a structured, metadata-rich format specifically optimized for training or querying RAG-based LLMs.

## 2. User Stories
- **As a Developer,** I want to download all Class 10 Science books with one command so I can build a tutor bot.
- **As a Researcher,** I want each PDF to have a corresponding JSON file with its metadata so my RAG system knows the context of each text chunk.
- **As a User with slow internet,** I want the scraper to resume downloads if the connection breaks.

## 3. Functional Requirements
- **FR1: Discovery:** Must be able to generate a full map of the NCERT website without hardcoded URLs.
- **FR2: Filtering:** CLI must support filtering by `--class`, `--subject`, and `--language` (English/Hindi/Urdu).
- **FR3: Post-Processing:** Must rename cryptic files (e.g., `jesc101.pdf`) to human-readable names (`Class10_Science_Ch1.pdf`).
- **FR4: Structure:** Must output a nested directory: `NCERT_Data/Class/Subject/Book/Chapters`.

## 4. Non-Functional Requirements
- **Performance:** Download speed > 10 files/minute on 100Mbps.
- **Reliability:** 100% success rate on ZIP extraction.
- **Politeness:** Must implement delays between requests to respect NCERT server limits.