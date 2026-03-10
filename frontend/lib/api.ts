import {
  AuditLog,
  DashboardSummary,
  ImportBatch,
  ImportBatchDetail,
  IncomeEvent,
  MarginSummary,
  PerformanceSummary,
  Position,
  RiskSummary,
  Strategy,
  TokenResponse,
  Trade,
  UserMe,
} from '@/lib/types';

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export class ApiError extends Error {
  constructor(
    public status: number,
    public endpoint: string,
    message: string,
  ) {
    super(message);
  }
}

async function request<T>(endpoint: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${endpoint}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    const text = await response.text();
    throw new ApiError(response.status, endpoint, text || `Request failed for ${endpoint}`);
  }

  return response.json() as Promise<T>;
}

function authHeaders(token?: string): HeadersInit {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(email: string, password: string) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new ApiError(response.status, '/api/auth/login', text || 'Authentication failed');
  }

  return { access_token: 'cookie-session' } as TokenResponse;
}

export const api = {
  me: (token?: string) => request<UserMe>('/auth/me', { headers: authHeaders(token) }),
  dashboardSummary: (token?: string) => request<DashboardSummary>('/dashboard/summary', { headers: authHeaders(token) }),
  positions: (token?: string) => request<Position[]>('/positions', { headers: authHeaders(token) }),
  trades: (token?: string) => request<Trade[]>('/trades', { headers: authHeaders(token) }),
  strategies: (token?: string) => request<Strategy[]>('/strategies', { headers: authHeaders(token) }),
  riskSummary: (token?: string) => request<RiskSummary>('/risk/summary', { headers: authHeaders(token) }),
  marginSummary: (token?: string) => request<MarginSummary>('/margin/summary', { headers: authHeaders(token) }),
  performanceSummary: (token?: string) => request<PerformanceSummary>('/performance/summary', { headers: authHeaders(token) }),
  income: (token?: string) => request<IncomeEvent[]>('/income', { headers: authHeaders(token) }),
  imports: (token?: string) => request<ImportBatch[]>('/imports', { headers: authHeaders(token) }),
  importBatch: (id: string, token?: string) => request<ImportBatchDetail>(`/imports/${id}`, { headers: authHeaders(token) }),
  auditLog: (token?: string) => request<AuditLog[]>('/audit-log', { headers: authHeaders(token) }),
};
