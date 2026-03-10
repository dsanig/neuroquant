import PositionsView from '@/components/PositionsView';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function PositionsPage() {
  const token = await getServerToken();
  const [positions, strategies, trades] = await Promise.all([api.positions(token), api.strategies(token), api.trades(token)]);

  return (
    <>
      <h1>Positions</h1>
      <p className="subtle">Grouped by strategy with roll-aware status indicators.</p>
      <PositionsView positions={positions} strategies={strategies} trades={trades} />
    </>
  );
}
