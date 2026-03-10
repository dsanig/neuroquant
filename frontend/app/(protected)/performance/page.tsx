import { MetricCard } from '@/components/ui/MetricCard';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatDate, formatMoney } from '@/lib/format';

export default async function PerformancePage() {
  const token = getServerToken();
  const perf = await api.performanceSummary(token);

  return (
    <>
      <h1>Performance</h1>
      <p className="subtle">Snapshot and trend-ready view.</p>
      <section className="grid four">
        <MetricCard label="As Of" value={formatDate(perf.as_of_date)} />
        <MetricCard label="NAV" value={formatMoney(perf.nav)} />
        <MetricCard label="PnL Day" value={formatMoney(perf.pnl_day)} />
        <MetricCard label="PnL MTD" value={formatMoney(perf.pnl_mtd)} />
      </section>
      <section className="card section">
        <h2>Trend Scaffolding</h2>
        <p className="subtle">Introduce a historical performance endpoint for line-chart rendering.</p>
      </section>
    </>
  );
}
