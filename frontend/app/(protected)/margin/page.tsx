import { MetricCard } from '@/components/ui/MetricCard';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';
import { formatMoney } from '@/lib/format';

export default async function MarginPage() {
  const token = getServerToken();
  const margin = await api.marginSummary(token);
  const discrepancy = Number(margin.margin_used) - Number(margin.broker_requirement);

  return (
    <>
      <h1>Margin Analysis</h1>
      <section className="grid four">
        <MetricCard label="Broker Requirement" value={formatMoney(margin.broker_requirement)} />
        <MetricCard label="Margin Used" value={formatMoney(margin.margin_used)} />
        <MetricCard label="Calculated Exposure" value={formatMoney(margin.notional_exposure)} />
        <MetricCard label="Discrepancy" value={formatMoney(discrepancy)} tone={discrepancy > 0 ? 'warning' : 'default'} />
      </section>
      <section className="card section">
        <h2>Capital at Risk</h2>
        <p>{formatMoney(margin.capital_at_risk)}</p>
      </section>
    </>
  );
}
