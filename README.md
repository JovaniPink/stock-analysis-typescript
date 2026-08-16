# Stock Analysis Workbook

This repository preserves a historical Excel and Script Lab exercise for
exploring stock-data calculations with the Excel JavaScript API. The durable
artifact is [`green_stocks_javascript.xlsx`](green_stocks_javascript.xlsx),
supported by two committed CSV snapshots for 2017 and 2018.

## Project status

This is a **historical learning archive**, not a maintained TypeScript
application, current market-data feed, or reproducible analytics pipeline.
There is no standalone TypeScript source, package manifest, dependency lock,
test runner, or automated data refresh in the repository.

The workbook retains an Office Script Lab add-in binding, but the Script Lab
source is not committed as a reviewable file. The original calculation logic
therefore cannot be rebuilt from this repository alone. Treat the workbook and
its computed cells as historical evidence, not as a supported application.

## Repository map

| Path | Role |
| --- | --- |
| `green_stocks_javascript.xlsx` | Excel workbook with `2017`, `2018`, and `DQ Analysis` worksheets |
| `data/2017_green_stocks.csv` | Historical 2017 stock-price snapshot |
| `data/2018_green_stocks.csv` | Historical 2018 stock-price snapshot |
| `scripts/check_repository.py` | Dependency-free structural validation; it never opens Excel or executes add-in code |

Both CSV files use the same columns:

```text
Ticker,Date,Open,High,Low,Close,Adj Close,Volume
```

## Validate the archive

Run the repository's complete local gate with Python 3.11 or newer:

```sh
python3 scripts/check_repository.py
```

The check verifies that:

- the required archive files exist;
- both CSV snapshots have the expected schema and non-empty data rows;
- the workbook is a readable Open XML package;
- the expected worksheet names are present; and
- no VBA binary or macro-enabled content type has been introduced.

This proves structural integrity only. It does not validate historical prices,
reconstruct the missing Script Lab source, or establish that the data may be
redistributed.

## Safe use and provenance

The committed prices are historical snapshots and must not be represented as
current market observations or investment advice. The repository does not
record sufficient source and license lineage for production or redistribution
use. Before reusing any data, establish the original provider, applicable
terms, retrieval date, adjustments, and permitted purpose.

Opening an Office workbook can load external add-ins. Inspect the file and use
a trusted Excel environment; do not treat the archived add-in reference as an
endorsement or a maintained dependency.

## License

Repository-authored material is available under the [MIT License](LICENSE.md).
That license does not grant rights to third-party market data, Microsoft Excel,
or external Office add-ins.
