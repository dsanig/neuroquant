import { ReactNode } from 'react';

type MetricCardProps = {
  label: string;
  value: string;
  helper?: string;
  tone?: 'default' | 'risk' | 'warning';
  icon?: ReactNode;
};

export function MetricCard({ label, value, helper, tone = 'default', icon }: MetricCardProps) {
  return (
    <section className={`card metric-card ${tone}`}>
      <div className="metric-head">
        <p className="subtle">{label}</p>
        {icon}
      </div>
      <p className="metric">{value}</p>
      {helper ? <p className="subtle">{helper}</p> : null}
    </section>
  );
}
