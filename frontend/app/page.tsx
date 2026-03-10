import AppShell from '@/components/AppShell';
import { fetchMarginMetrics } from '@/lib/api';

export default async function HomePage() {
  let marginError = '';
  let metrics = [] as Awaited<ReturnType<typeof fetchMarginMetrics>>;

  try {
    metrics = await fetchMarginMetrics();
  } catch {
    marginError = 'Margin service unavailable';
  }

  return (
    <AppShell>
      <h1>Portfolio Control Center</h1>
      <p className="subtle">Institutional oversight for risk, margin, and strategy operations.</p>
      <div className="grid">
        <section className="card"><div className="subtle">Open Strategies</div><div className="metric">7</div></section>
        <section className="card"><div className="subtle">Portfolio Notional</div><div className="metric">$2.84M</div></section>
        <section className="card"><div className="subtle">Margin Utilization</div><div className="metric">41.2%</div></section>
      </div>

      <section className="card" style={{ marginTop: 16 }}>
        <h3>Margin Metrics (Broker + App)</h3>
        {marginError ? (
          <p className="subtle">{marginError}</p>
        ) : metrics.length === 0 ? (
          <p className="subtle">No metrics yet.</p>
        ) : (
          <table className="table">
            <thead><tr><th>Source</th><th>Notional</th><th>Margin Used</th><th>Broker Requirement</th></tr></thead>
            <tbody>
              {metrics.map((m, idx) => (
                <tr key={idx}><td>{m.source}</td><td>{m.notional_exposure}</td><td>{m.margin_used}</td><td>{m.broker_requirement ?? '-'}</td></tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </AppShell>
  );
}
