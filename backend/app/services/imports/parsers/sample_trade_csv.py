from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation

from app.services.imports.contracts import NormalizedMetadata, NormalizedTradeRecord
from app.services.imports.parsers.base import ImportParser


class SampleTradeCsvParser(ImportParser):
    parser_name = "sample_trade_csv"
    parser_version = "1.0.0"
    required_headers = {
        "external_trade_id",
        "broker_account",
        "strategy",
        "symbol",
        "side",
        "quantity",
        "price",
        "executed_at",
    }

    def can_parse(self, headers: list[str], source_system_name: str) -> bool:
        return self.required_headers.issubset(set(headers)) and source_system_name in {"sample_broker", "custom"}

    def parse(self, *, rows: list[dict[str, str]], import_batch_id: str, source_file: str) -> tuple[list[NormalizedTradeRecord], list[tuple[int, str, str, dict[str, str]]]]:
        records: list[NormalizedTradeRecord] = []
        errors: list[tuple[int, str, str, dict[str, str]]] = []
        for row_number, row in enumerate(rows, start=2):
            try:
                quantity = int(row["quantity"])
                price = Decimal(row["price"])
                executed_at = datetime.fromisoformat(row["executed_at"].replace("Z", "+00:00"))
                records.append(
                    NormalizedTradeRecord(
                        external_trade_id=row["external_trade_id"],
                        broker_account_number=row["broker_account"],
                        strategy_name=row["strategy"],
                        symbol=row["symbol"],
                        side=row["side"].upper(),
                        quantity=quantity,
                        price=price,
                        executed_at=executed_at,
                        metadata=NormalizedMetadata(
                            import_batch_id=import_batch_id,
                            source_file=source_file,
                            source_row=row_number,
                            parser_version=self.parser_version,
                        ),
                    )
                )
            except (KeyError, ValueError, InvalidOperation) as exc:
                errors.append((row_number, "ROW_PARSE_ERROR", str(exc), row))
        return records, errors
