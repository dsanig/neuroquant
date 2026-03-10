from app.services.imports.parsers.sample_trade_csv import SampleTradeCsvParser


def test_sample_trade_csv_parser_parses_and_flags_errors() -> None:
    parser = SampleTradeCsvParser()
    rows = [
        {
            "external_trade_id": "T-1",
            "broker_account": "ACC-1",
            "strategy": "Income",
            "symbol": "AAPL",
            "side": "buy",
            "quantity": "3",
            "price": "1.23",
            "executed_at": "2026-03-10T10:00:00Z",
        },
        {
            "external_trade_id": "T-2",
            "broker_account": "ACC-1",
            "strategy": "Income",
            "symbol": "AAPL",
            "side": "sell",
            "quantity": "x",
            "price": "1.20",
            "executed_at": "2026-03-10T10:05:00Z",
        },
    ]

    records, errors = parser.parse(rows=rows, import_batch_id="batch-1", source_file="sample.csv")

    assert len(records) == 1
    assert records[0].metadata.import_batch_id == "batch-1"
    assert records[0].metadata.source_file == "sample.csv"
    assert records[0].metadata.source_row == 2
    assert records[0].metadata.parser_version == parser.parser_version
    assert len(errors) == 1
    assert errors[0][0] == 3
