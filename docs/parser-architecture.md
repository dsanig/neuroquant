# Parser Architecture

## Components
- `ImportParser` base abstraction (`app/services/imports/parsers/base.py`)
- `ParserRegistry` broker parser selector (`.../registry.py`)
- normalized contracts (`app/services/imports/contracts.py`)

## Detection strategy
A parser is selected by:
- source system name
- required header superset match

## Current concrete parser
- `SampleTradeCsvParser` (`sample_trade_csv` v`1.0.0`)
- expects columns:
  - `external_trade_id`
  - `broker_account`
  - `strategy`
  - `symbol`
  - `side`
  - `quantity`
  - `price`
  - `executed_at` (ISO8601)
- returns:
  - `NormalizedTradeRecord[]`
  - row-level parse errors with deterministic row numbers

## Extension points
- Add broker-specific parser by implementing `ImportParser`
- Register parser in `ParserRegistry`
- Evolve normalized contracts to include snapshots and non-transactional domain objects
- Add decrypt stage before validation for FTP/PGP pipelines
