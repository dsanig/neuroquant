from collections import defaultdict

from app.models.entities import OptionContract, Trade


class RollDetectionService:
    """Detect option rolls by exact timestamp, same underlying, and matched quantities."""

    @staticmethod
    def assign_roll_groups(trades: list[Trade], contracts_by_id: dict[str, OptionContract]) -> int:
        buckets: dict[tuple, list[Trade]] = defaultdict(list)
        for trade in trades:
            contract = contracts_by_id.get(str(trade.option_contract_id)) if trade.option_contract_id else None
            underlying = contract.underlying if contract else trade.symbol
            key = (trade.executed_at, underlying, abs(trade.quantity))
            buckets[key].append(trade)

        groups_found = 0
        for key, grouped in buckets.items():
            buys = [t for t in grouped if t.side.upper() == "BUY"]
            sells = [t for t in grouped if t.side.upper() == "SELL"]
            for idx, (buy_trade, sell_trade) in enumerate(zip(sorted(buys, key=lambda t: t.id), sorted(sells, key=lambda t: t.id), strict=False)):
                roll_id = f"roll-{key[0].isoformat()}-{key[1]}-{idx}"
                buy_trade.roll_group_id = roll_id
                sell_trade.roll_group_id = roll_id
                groups_found += 1
        return groups_found
