# Repository guidance

## Purpose

This repository is a historical Excel stock-analysis learning archive. The
workbook and CSV snapshots are evidence artifacts, not a current market-data
pipeline or a maintained TypeScript application.

## Canonical command

```sh
python3 scripts/check_repository.py
```

The validator uses only the Python standard library and must not open Excel,
execute Office add-ins, contact a market-data provider, or mutate the archive.

## Working rules

- Preserve the workbook and historical CSV files unless a task explicitly
  authorizes an artifact migration.
- Do not claim that the Script Lab source is reproducible; it is not committed
  as a reviewable file.
- Treat historical prices as unverified third-party data with unknown
  redistribution rights.
- Do not add live scraping, trading, brokerage, or investment-advice behavior.
- Stage explicit files only and preserve unrelated artifacts.
- Run the canonical command before opening or updating a pull request.
