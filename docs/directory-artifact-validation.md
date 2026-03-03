# Directory artifact validation (SAD-1 / GRID)

The CTS primarily validates TRQP API conformance. However, many authoritative directories publish **verifier-first**
artifacts as files or feeds.

To support end-to-end evaluation, the CTS ships schemas and a lightweight validator for these artifacts.

## What this validates

- Directory entry (`authoritative-directory-entry.schema.json`)
- Publication manifest (`directory-publication-manifest.schema.json`)
- Status feed (`directory-status-feed.schema.json`)

## Usage

Validate a directory entry:

```bash
python scripts/validate_directory_artifacts.py --entry path/to/entry.json
```

Validate a publication manifest:

```bash
python scripts/validate_directory_artifacts.py --manifest path/to/manifest.json
```

Validate a status feed:

```bash
python scripts/validate_directory_artifacts.py --status path/to/status-feed.json
```

## Relationship to profiles

- SAD-1 is the generic authoritative directory profile in the Assurance Hub.
- GRID is an instance profile aligned to UN/CEFACT directory patterns.

This CTS capability is intentionally minimal: it validates structure so that assessments can reliably reference
machine-readable artifacts as evidence.
