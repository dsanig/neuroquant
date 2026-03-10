# Frontend Architecture - Investment Control Center

## Objectives
- Authenticated internal operations console for portfolio control.
- Data-dense, institutional UX for daily risk/margin/position workflows.
- Typed integration to backend APIs with central error handling.

## Structure
- `frontend/app/(auth)/login`: unauthenticated entry.
- `frontend/app/(protected)/*`: authenticated modules (Dashboard, Positions, Trades, Strategies, Risk, Margin, Performance, Income, Reports, Audit Log, Settings).
- `frontend/components/ui/*`: reusable primitives (`MetricCard`, `DataTable`, `FilterBar`).
- `frontend/lib/api.ts`: typed API client and shared `ApiError`.
- `frontend/middleware.ts`: route guards and pathname forwarding for navigation state.

## Auth and route guard
- Auth token is stored in `auth_token` cookie after successful login.
- `middleware.ts` redirects unauthenticated users to `/login`.
- Protected layout validates session via `/auth/me`; unauthorized responses redirect to `/login`.

## Rendering strategy
- Module pages are Server Components by default for operational data freshness.
- Client Components are used for interactive filtering/sorting (`PositionsView`, `TradesView`, filter controls).
- Page-level loading and error boundaries are provided under `app/(protected)/loading.tsx` and `error.tsx`.

## API integration
- All endpoint contracts are captured in `frontend/lib/types.ts`.
- `api` object contains typed methods matching backend routes.
- No domain calculations are embedded in UI components; UI only formats backend-provided metrics.

## Key component architecture choices
1. **Shell-first composition**: one institutional layout shell (`AppShell`) standardizes navigation, identity, and page framing.
2. **Primitive reuse**: table/metric/filter primitives keep implementation consistent across modules.
3. **State surfaces**: each data view provides explicit loading/empty/error state affordances for operational reliability.
4. **Roll-aware positions UX**: positions stay strategy-grouped while exposing roll markers as contextual metadata instead of split visual positions.
