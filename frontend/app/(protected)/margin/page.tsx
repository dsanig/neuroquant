import { MetricCard } from '@/components/ui/MetricCard';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatMoney } from '@/lib/format';

export default async function MarginPage() {
  const token = await getServerToken();
  const margin = await api.marginSummary(token);
  const discrepancy = Number(margin.margin_used) - Number(margin.broker_requirement);

  return (
    <>
      <h1>Margin Analysis</h1>
      <section className="grid four">
        <MetricCard label="Broker Requirement" value={formatMoney(margin.broker_requirement)} />
        <MetricCard label="Total Margin Used" value={formatMoney(margin.margin_used)} />
        <MetricCard label="Total Notional Exposure" value={formatMoney(margin.notional_exposure)} />
        <MetricCard label="Discrepancy" value={formatMoney(discrepancy)} tone={discrepancy > 0 ? 'warning' : 'default'} />
      </section>

      <section className="grid four">
        <MetricCard label="Broker Margin Used" value={formatMoney(margin.broker_margin_used)} />
        <MetricCard label="App Margin Used" value={formatMoney(margin.app_margin_used)} />
        <MetricCard label="Broker Notional" value={formatMoney(margin.broker_notional_exposure)} />
        <MetricCard label="App Notional" value={formatMoney(margin.app_notional_exposure)} />
      </section>

      <section className="card section">
        <h2>Capital at Risk</h2>
        <p>{formatMoney(margin.capital_at_risk)}</p>
      </section>
    </>
  );
}
