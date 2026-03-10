export type MarginMetric = {
  measured_at: string;
  strategy_id: string | null;
  notional_exposure: number;
  margin_used: number;
  broker_requirement: number | null;
  source: string;
};

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export async function fetchMarginMetrics(): Promise<MarginMetric[]> {
  const response = await fetch(`${baseUrl}/margin`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Failed to load margin metrics');
  return response.json();
}
