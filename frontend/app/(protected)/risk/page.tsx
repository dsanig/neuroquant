import { MetricCard } from '@/components/ui/MetricCard';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatNumber } from '@/lib/format';

export default async function RiskPage() {
  const token = getServerToken();
  const risk = await api.riskSummary(token);

  return (
    <>
      <h1>Risk</h1>
      <p className="subtle">Greeks, concentration, exposure, and drawdown-ready scaffolding.</p>
      <section className="grid four">
        <MetricCard label="Portfolio Delta" value={formatNumber(risk.portfolio_delta)} tone="risk" />
        <MetricCard label="Portfolio Gamma" value={formatNumber(risk.portfolio_gamma)} tone="risk" />
        <MetricCard label="Portfolio Theta" value={formatNumber(risk.portfolio_theta)} tone="risk" />
        <MetricCard label="Portfolio Vega" value={formatNumber(risk.portfolio_vega)} tone="risk" />
      </section>
      <section className="card section">
        <h2>Concentration and Exposure</h2>
        <p className="subtle">Top Underlying: {risk.concentration_top_underlying || 'None'}</p>
        {Object.keys(risk.underlying_exposure).length ? (
          <ul className="compact-list">
            {Object.entries(risk.underlying_exposure).map(([name, value]) => (
              <li key={name}>{name}: {formatNumber(value)}</li>
            ))}
          </ul>
        ) : <div className="state-empty">No underlying exposures available.</div>}
      </section>
      <section className="card section">
        <h2>Drawdown Readiness Scaffold</h2>
        <p className="subtle">Hook scenario analytics into this section when calculation-service endpoints are available.</p>
      </section>
    </>
  );
}
