import { DataTable } from '@/components/ui/DataTable';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatDateTime } from '@/lib/format';

export default async function AuditLogPage() {
  const token = getServerToken();
  const logs = await api.auditLog(token);

  return (
    <>
      <h1>Audit Log</h1>
      <p className="subtle">Immutable event listing.</p>
      <DataTable
        caption="Event stream"
        rows={logs}
        getKey={(row) => row.id}
        emptyText="No audit events captured."
        columns={[
          { key: 'time', title: 'Timestamp', render: (row) => formatDateTime(row.created_at) },
          { key: 'event', title: 'Event Type', render: (row) => row.event_type },
          { key: 'entity', title: 'Entity', render: (row) => `${row.entity_type}:${row.entity_id}` },
          { key: 'payload', title: 'Payload', render: (row) => <code>{JSON.stringify(row.payload)}</code> },
        ]}
      />
    </>
  );
}
