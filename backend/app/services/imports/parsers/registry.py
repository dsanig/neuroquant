from app.services.imports.parsers.base import ImportParser
from app.services.imports.parsers.sample_trade_csv import SampleTradeCsvParser


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: list[ImportParser] = [SampleTradeCsvParser()]

    def detect(self, headers: list[str], source_system_name: str) -> ImportParser | None:
        for parser in self._parsers:
            if parser.can_parse(headers, source_system_name):
                return parser
        return None
