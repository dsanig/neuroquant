export type UserMe = {
  id: string;
  email: string;
  full_name: string;
  roles: string[];
};

export type Strategy = {
  id: string;
  name: string;
  description: string | null;
};

export type Position = {
  id: string;
  strategy_id: string;
  quantity: number;
  avg_price: string;
  mark_price: string | null;
  realized_pnl: string;
};

export type Trade = {
  id: string;
  strategy_id: string;
  symbol: string;
  side: string;
  quantity: number;
  price: string;
  premium: string | null;
  executed_at: string;
  roll_group_id: string | null;
};

export type DashboardSummary = {
  as_of: string;
  open_positions: number;
  trades_today: number;
  active_strategies: number;
};

export type RiskSummary = {
  as_of: string;
  portfolio_delta: string;
  portfolio_gamma: string;
  portfolio_theta: string;
  portfolio_vega: string;
  concentration_top_underlying: string | null;
  underlying_exposure: Record<string, string>;
};

export type MarginSummary = {
  as_of: string;
  notional_exposure: string;
  capital_at_risk: string;
  margin_used: string;
  broker_requirement: string;
};

export type PerformanceSummary = {
  as_of_date: string;
  nav: string;
  pnl_day: string;
  pnl_mtd: string | null;
  pnl_ytd: string | null;
};

export type IncomeEvent = {
  id: string;
  strategy_id: string | null;
  event_date: string;
  amount: string;
  event_type: string;
};

export type ImportBatch = {
  id: string;
  filename: string;
  source_checksum: string;
  status: string;
  row_count: number;
  imported_count: number;
  error_count: number;
};

export type AuditLog = {
  id: string;
  event_type: string;
  entity_type: string;
  entity_id: string;
  payload: Record<string, unknown>;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};
