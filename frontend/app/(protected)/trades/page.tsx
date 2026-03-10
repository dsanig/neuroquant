import TradesView from '@/components/TradesView';
import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function TradesPage() {
  const token = await getServerToken();
  const [trades, strategies, imports] = await Promise.all([api.trades(token), api.strategies(token), api.imports(token)]);

  return (
    <>
      <h1>Trades</h1>
      <p className="subtle">Historical ledger with source metadata and import provenance.</p>
      <TradesView trades={trades} strategies={strategies} imports={imports} />
    </>
  );
}
