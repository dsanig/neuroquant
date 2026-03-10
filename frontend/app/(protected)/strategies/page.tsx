import { DataTable } from '@/components/ui/DataTable';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function StrategiesPage() {
  const token = getServerToken();
  const strategies = await api.strategies(token);

  return (
    <>
      <h1>Strategies</h1>
      <DataTable
        caption="Strategy register"
        rows={strategies}
        getKey={(row) => row.id}
        emptyText="No strategies configured."
        columns={[
          { key: 'name', title: 'Name', render: (row) => row.name },
          { key: 'id', title: 'ID', render: (row) => row.id },
          { key: 'description', title: 'Description', render: (row) => row.description || '—' },
        ]}
      />
    </>
  );
}
