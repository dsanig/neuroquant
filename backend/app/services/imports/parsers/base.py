from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.imports.contracts import NormalizedTradeRecord


class ImportParser(ABC):
    parser_name: str
    parser_version: str

    @abstractmethod
    def can_parse(self, headers: list[str], source_system_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, *, rows: list[dict[str, str]], import_batch_id: str, source_file: str) -> tuple[list[NormalizedTradeRecord], list[tuple[int, str, str, dict[str, str]]]]:
        """Return (normalized_records, row_errors). row_errors = (row_number, code, message, source_row)."""
        raise NotImplementedError
