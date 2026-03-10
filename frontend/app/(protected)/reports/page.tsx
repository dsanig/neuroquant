import { DataTable } from '@/components/ui/DataTable';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function ReportsPage() {
  const token = getServerToken();
  const imports = await api.imports(token);

  return (
    <>
      <h1>Reports</h1>
      <p className="subtle">Operational reporting queue using imported batch evidence.</p>
      <DataTable
        caption="Available report artifacts"
        rows={imports}
        getKey={(row) => row.id}
        emptyText="No report-ready imports found."
        columns={[
          { key: 'source', title: 'Source', render: (row) => row.source_system_name },
          { key: 'channel', title: 'Channel', render: (row) => row.intake_channel },
          { key: 'status', title: 'Status', render: (row) => row.status },
          { key: 'rows', title: 'Rows', render: (row) => row.row_count },
          { key: 'imported', title: 'Imported', render: (row) => row.imported_count },
          { key: 'errors', title: 'Errors', render: (row) => row.error_count },
        ]}
      />
    </>
  );
}
