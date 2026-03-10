'use client';

import { useMemo, useState } from 'react';

import { DataTable } from '@/components/ui/DataTable';
import { FilterBar } from '@/components/ui/FilterBar';
import { formatMoney, formatNumber } from '@/lib/format';
import { Position, Strategy, Trade } from '@/lib/types';

type Props = {
  positions: Position[];
  strategies: Strategy[];
  trades: Trade[];
};

export default function PositionsView({ positions, strategies, trades }: Props) {
  const [search, setSearch] = useState('');
  const [strategy, setStrategy] = useState('all');
  const [sort, setSort] = useState('qty-desc');

  const strategyMap = useMemo(() => Object.fromEntries(strategies.map((s) => [s.id, s.name])), [strategies]);
  const rollGroupsByStrategy = useMemo(() => {
    const grouped = new Map<string, number>();
    trades.forEach((t) => {
      if (t.roll_group_id) grouped.set(t.strategy_id, (grouped.get(t.strategy_id) || 0) + 1);
    });
    return grouped;
  }, [trades]);

  const filtered = useMemo(() => {
    let rows = positions.filter((p) => {
      const byStrategy = strategy === 'all' ? true : p.strategy_id === strategy;
      const name = strategyMap[p.strategy_id] || p.strategy_id;
      const text = `${p.id} ${name}`.toLowerCase();
      const bySearch = text.includes(search.toLowerCase());
      return byStrategy && bySearch;
    });

    rows = [...rows].sort((a, b) => {
      if (sort === 'qty-asc') return a.quantity - b.quantity;
      if (sort === 'qty-desc') return b.quantity - a.quantity;
      if (sort === 'pnl-desc') return Number(b.realized_pnl) - Number(a.realized_pnl);
      return Number(a.realized_pnl) - Number(b.realized_pnl);
    });
    return rows;
  }, [positions, search, sort, strategy, strategyMap]);

  return (
    <>
      <FilterBar
        search={search}
        onSearchChange={setSearch}
        strategy={strategy}
        strategyOptions={strategies.map((s) => s.id)}
        onStrategyChange={setStrategy}
        sort={sort}
        sortOptions={[
          { label: 'Quantity (High to Low)', value: 'qty-desc' },
          { label: 'Quantity (Low to High)', value: 'qty-asc' },
          { label: 'Realized PnL (High to Low)', value: 'pnl-desc' },
          { label: 'Realized PnL (Low to High)', value: 'pnl-asc' },
        ]}
        onSortChange={setSort}
      />

      <DataTable
        caption="Positions grouped by strategy with roll-aware context"
        rows={filtered}
        getKey={(row) => row.id}
        emptyText="No positions match the selected filters."
        columns={[
          {
            key: 'strategy',
            title: 'Strategy',
            render: (row) => (
              <div>
                <strong>{strategyMap[row.strategy_id] || row.strategy_id}</strong>
                {rollGroupsByStrategy.get(row.strategy_id) ? (
                  <p className="subtle">Roll activity detected ({rollGroupsByStrategy.get(row.strategy_id)})</p>
                ) : (
                  <p className="subtle">No current roll markers</p>
                )}
              </div>
            ),
          },
          { key: 'id', title: 'Position ID', render: (row) => row.id },
          { key: 'qty', title: 'Quantity', render: (row) => formatNumber(row.quantity) },
          { key: 'avg', title: 'Average Price', render: (row) => formatMoney(row.avg_price) },
          { key: 'mark', title: 'Mark Price', render: (row) => formatMoney(row.mark_price) },
          { key: 'pnl', title: 'Realized PnL', render: (row) => formatMoney(row.realized_pnl) },
        ]}
      />
    </>
  );
}
