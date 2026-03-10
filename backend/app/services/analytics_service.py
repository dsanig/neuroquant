from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import DashboardSummaryOut, MarginSummaryOut, PerformanceSummaryOut, RiskSummaryOut


class AnalyticsService:
    def __init__(self, repo: DomainRepository):
        self.repo = repo

    def dashboard_summary(self) -> DashboardSummaryOut:
        now = self.repo.utc_now()
        return DashboardSummaryOut(
            as_of=now,
            open_positions=self.repo.count_open_positions(),
            trades_today=self.repo.count_trades_for_day(now.date()),
            active_strategies=self.repo.count_active_strategies(),
        )

    def margin_summary(self) -> MarginSummaryOut:
        metrics = self.repo.latest_margin_summary()
        z = Decimal("0")
        if not metrics:
            return MarginSummaryOut(
                as_of=self.repo.utc_now(),
                notional_exposure=z,
                capital_at_risk=z,
                margin_used=z,
                broker_requirement=z,
                app_margin_used=z,
                broker_margin_used=z,
                app_notional_exposure=z,
                broker_notional_exposure=z,
            )

        app_metrics = [m for m in metrics if m.source == "app"]
        broker_metrics = [m for m in metrics if m.source == "broker"]

        return MarginSummaryOut(
            as_of=metrics[0].measured_at,
            notional_exposure=sum((m.notional_exposure for m in metrics), z),
            capital_at_risk=sum((m.capital_at_risk for m in metrics), z),
            margin_used=sum((m.margin_used for m in metrics), z),
            broker_requirement=sum((m.broker_requirement or z for m in metrics), z),
            app_margin_used=sum((m.margin_used for m in app_metrics), z),
            broker_margin_used=sum((m.margin_used for m in broker_metrics), z),
            app_notional_exposure=sum((m.notional_exposure for m in app_metrics), z),
            broker_notional_exposure=sum((m.notional_exposure for m in broker_metrics), z),
        )

    def risk_summary(self) -> RiskSummaryOut:
        greeks = self.repo.latest_greeks()
        risk = self.repo.latest_risk_metrics()
        exposure_map: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        for metric in risk:
            if metric.metric_name == "underlying_exposure" and metric.instrument_id:
                exposure_map[str(metric.instrument_id)] += metric.metric_value
        top_underlying = max(exposure_map, key=lambda k: abs(exposure_map[k])) if exposure_map else None
        z = Decimal("0")
        return RiskSummaryOut(
            as_of=self.repo.utc_now(),
            portfolio_delta=sum((g.delta for g in greeks), z),
            portfolio_gamma=sum((g.gamma for g in greeks), z),
            portfolio_theta=sum((g.theta for g in greeks), z),
            portfolio_vega=sum(((g.vega or z) for g in greeks), z),
            concentration_top_underlying=top_underlying,
            underlying_exposure=dict(exposure_map),
        )

    def performance_summary(self) -> PerformanceSummaryOut:
        perf = self.repo.latest_performance()
        if not perf:
            return PerformanceSummaryOut(as_of_date=date.today(), nav=Decimal("0"), pnl_day=Decimal("0"), pnl_mtd=Decimal("0"), pnl_ytd=Decimal("0"))
        return PerformanceSummaryOut(
            as_of_date=perf.snapshot_date,
            nav=perf.nav,
            pnl_day=perf.pnl_day,
            pnl_mtd=perf.pnl_mtd,
            pnl_ytd=perf.pnl_ytd,
        )
