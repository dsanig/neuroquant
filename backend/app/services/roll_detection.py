from collections import defaultdict

from app.models.entities import OptionContract, Trade


class RollDetectionService:
    """Detects option rolls when buy/sell share exact timestamp, underlying, and quantity."""

    @staticmethod
    def assign_roll_groups(trades: list[Trade], contracts_by_id: dict[str, OptionContract]) -> int:
        buckets: dict[tuple, list[Trade]] = defaultdict(list)
        for trade in trades:
            contract = contracts_by_id.get(str(trade.option_contract_id)) if trade.option_contract_id else None
            underlying = contract.underlying if contract else trade.symbol
            key = (trade.executed_at.replace(microsecond=0), underlying, abs(trade.quantity))
            buckets[key].append(trade)

        groups_found = 0
        for key, grouped in buckets.items():
            buys = [t for t in grouped if t.side.upper() == "BUY"]
            sells = [t for t in grouped if t.side.upper() == "SELL"]
            pairs = min(len(buys), len(sells))
            if pairs > 0:
                groups_found += pairs
                for idx in range(pairs):
                    roll_id = f"roll-{key[0].isoformat()}-{key[1]}-{idx}"
                    buys[idx].roll_group_id = roll_id
                    sells[idx].roll_group_id = roll_id
        return groups_found
