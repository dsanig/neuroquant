'use client';

import { useMemo, useState } from 'react';

import { DataTable } from '@/components/ui/DataTable';
import { FilterBar } from '@/components/ui/FilterBar';
import { formatDateTime, formatMoney, formatNumber } from '@/lib/format';
import { ImportBatch, Strategy, Trade } from '@/lib/types';

type Props = {
  trades: Trade[];
  strategies: Strategy[];
  imports: ImportBatch[];
};

export default function TradesView({ trades, strategies, imports }: Props) {
  const [search, setSearch] = useState('');
  const [strategy, setStrategy] = useState('all');
  const [sort, setSort] = useState('executed-desc');

  const strategyMap = useMemo(() => Object.fromEntries(strategies.map((s) => [s.id, s.name])), [strategies]);
  const importStatus = imports.length ? `${imports[0].status} / ${imports[0].filename}` : 'No import batches';

  const filtered = useMemo(() => {
    let rows = trades.filter((t) => {
      const byStrategy = strategy === 'all' ? true : t.strategy_id === strategy;
      const text = `${t.id} ${t.symbol} ${t.side}`.toLowerCase();
      return byStrategy && text.includes(search.toLowerCase());
    });

    rows = [...rows].sort((a, b) => {
      if (sort === 'executed-asc') return new Date(a.executed_at).getTime() - new Date(b.executed_at).getTime();
      return new Date(b.executed_at).getTime() - new Date(a.executed_at).getTime();
    });
    return rows;
  }, [search, sort, strategy, trades]);

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
          { label: 'Executed (Newest first)', value: 'executed-desc' },
          { label: 'Executed (Oldest first)', value: 'executed-asc' },
        ]}
        onSortChange={setSort}
      />
      <DataTable
        caption="Historical trade ledger with provenance"
        rows={filtered}
        getKey={(row) => row.id}
        emptyText="No trades found."
        columns={[
          { key: 'executed', title: 'Executed', render: (row) => formatDateTime(row.executed_at) },
          { key: 'id', title: 'Trade ID', render: (row) => row.id },
          { key: 'strategy', title: 'Strategy', render: (row) => strategyMap[row.strategy_id] || row.strategy_id },
          { key: 'symbol', title: 'Symbol', render: (row) => row.symbol },
          { key: 'side', title: 'Side', render: (row) => row.side },
          { key: 'qty', title: 'Qty', render: (row) => formatNumber(row.quantity) },
          { key: 'price', title: 'Price', render: (row) => formatMoney(row.price) },
          { key: 'premium', title: 'Premium', render: (row) => formatMoney(row.premium) },
          { key: 'roll', title: 'Roll Group', render: (row) => row.roll_group_id || '—' },
          { key: 'source', title: 'Source Metadata', render: () => importStatus },
        ]}
      />
    </>
  );
}
