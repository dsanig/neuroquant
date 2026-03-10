import { ReactNode } from 'react';

export type TableColumn<T> = {
  key: string;
  title: string;
  render: (row: T) => ReactNode;
};

type DataTableProps<T> = {
  caption: string;
  columns: TableColumn<T>[];
  rows: T[];
  getKey: (row: T) => string;
  emptyText: string;
};

export function DataTable<T>({ caption, columns, rows, getKey, emptyText }: DataTableProps<T>) {
  if (!rows.length) {
    return <div className="state-empty">{emptyText}</div>;
  }

  return (
    <div className="table-wrap">
      <table className="table">
        <caption>{caption}</caption>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key}>{col.title}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={getKey(row)}>
              {columns.map((col) => (
                <td key={col.key}>{col.render(row)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
