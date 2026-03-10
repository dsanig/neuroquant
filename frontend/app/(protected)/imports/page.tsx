import { DataTable } from '@/components/ui/DataTable';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function ImportsPage() {
  const token = await getServerToken();
  const batches = await api.imports(token);
  const firstDetail = batches[0] ? await api.importBatch(batches[0].id, token) : null;

  return (
    <>
      <h1>Imports</h1>
      <p className="subtle">Track batch status, parser metadata, and row-level diagnostics.</p>

      <DataTable
        caption="Import batches"
        rows={batches}
        getKey={(row) => row.id}
        emptyText="No imports yet."
        columns={[
          { key: 'source', title: 'Source', render: (row) => row.source_system_name },
          { key: 'channel', title: 'Channel', render: (row) => row.intake_channel },
          { key: 'status', title: 'Status', render: (row) => row.status },
          { key: 'parser', title: 'Parser', render: (row) => `${row.parser_name || 'n/a'}@${row.parser_version || 'n/a'}` },
          { key: 'rows', title: 'Rows', render: (row) => row.row_count },
          { key: 'errors', title: 'Errors', render: (row) => row.error_count },
        ]}
      />

      <section className="card section">
        <h2>Row-level Diagnostics {firstDetail ? `(Latest Batch: ${firstDetail.id})` : ''}</h2>
        {firstDetail?.row_errors.length ? (
          <DataTable
            caption="Row errors"
            rows={firstDetail.row_errors}
            getKey={(row) => row.id}
            emptyText="No row errors"
            columns={[
              { key: 'row', title: 'Row', render: (row) => row.row_number },
              { key: 'code', title: 'Code', render: (row) => row.code },
              { key: 'msg', title: 'Message', render: (row) => row.message },
              { key: 'parser', title: 'Parser Ver', render: (row) => row.parser_version },
            ]}
          />
        ) : (
          <div className="state-empty">No row-level diagnostics found.</div>
        )}
      </section>
    </>
  );
}
