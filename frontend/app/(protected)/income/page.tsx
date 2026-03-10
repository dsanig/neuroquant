import { DataTable } from '@/components/ui/DataTable';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatDate, formatMoney } from '@/lib/format';

export default async function IncomePage() {
  const token = await getServerToken();
  const income = await api.income(token);

  return (
    <>
      <h1>Income</h1>
      <p className="subtle">Dividends, interest, and option premium events.</p>
      <DataTable
        caption="Income ledger"
        rows={income}
        getKey={(row) => row.id}
        emptyText="No income events present."
        columns={[
          { key: 'date', title: 'Date', render: (row) => formatDate(row.event_date) },
          { key: 'type', title: 'Type', render: (row) => row.event_type },
          { key: 'strategy', title: 'Strategy', render: (row) => row.strategy_id || '—' },
          { key: 'amount', title: 'Amount', render: (row) => formatMoney(row.amount) },
        ]}
      />
    </>
  );
}
