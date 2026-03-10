import { MetricCard } from '@/components/ui/MetricCard';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatDateTime, formatNumber } from '@/lib/format';

export default async function DashboardPage() {
  const token = await getServerToken();
  const [dashboard, risk, imports, trades, strategies] = await Promise.all([
    api.dashboardSummary(token),
    api.riskSummary(token),
    api.imports(token),
    api.trades(token),
    api.strategies(token),
  ]);

  return (
    <>
      <h1>Dashboard</h1>
      <p className="subtle">As of {formatDateTime(dashboard.as_of)}</p>

      <section className="grid four">
        <MetricCard label="Open Positions" value={formatNumber(dashboard.open_positions)} />
        <MetricCard label="Trades Today" value={formatNumber(dashboard.trades_today)} />
        <MetricCard label="Active Strategies" value={formatNumber(dashboard.active_strategies)} />
        <MetricCard label="Top Concentration" value={risk.concentration_top_underlying || 'None'} tone="warning" />
      </section>

      <section className="card section">
        <h2>Strategy Summary</h2>
        {strategies.length ? (
          <ul className="compact-list">
            {strategies.map((s) => <li key={s.id}><strong>{s.name}</strong> <span className="subtle">({s.id})</span></li>)}
          </ul>
        ) : <div className="state-empty">No strategies registered.</div>}
      </section>

      <section className="card section">
        <h2>Recent Activity</h2>
        {trades.length ? (
          <ul className="compact-list">
            {trades.slice(0, 8).map((t) => <li key={t.id}>{formatDateTime(t.executed_at)} — {t.symbol} {t.side} {t.quantity}</li>)}
          </ul>
        ) : <div className="state-empty">No trade activity available.</div>}
      </section>

      <section className="card section">
        <h2>System / Import Alerts</h2>
        {imports.length ? (
          <ul className="compact-list">
            {imports.slice(0, 6).map((batch) => (
              <li key={batch.id}>
                {batch.source_system_name} [{batch.intake_channel}] — <strong>{batch.status}</strong> <span className="subtle">({batch.error_count} errors)</span>
              </li>
            ))}
          </ul>
        ) : <div className="state-empty">No import alerts.</div>}
      </section>
    </>
  );
}
