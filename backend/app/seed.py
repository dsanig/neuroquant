from datetime import UTC, datetime

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.entities import BrokerAccount, Firm, MarginMetric, Role, Strategy, Trade, User, UserRole


def run() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(User).where(User.email == "admin@neuroquant.local")):
            return

        admin = User(email="admin@neuroquant.local", full_name="NeuroQuant Admin", password_hash=hash_password("admin"))
        role = Role(name="admin")
        firm = Firm(name="Northstar Capital", legal_name="Northstar Capital Management LLC", base_currency="USD")
        strategy = Strategy(name="Income Wheel", description="CSP and covered call cycle")
        operator_role = Role(name="operator")
        auditor_role = Role(name="auditor")
        db.add_all([admin, role, operator_role, auditor_role, firm, strategy])
        db.flush()
        broker = BrokerAccount(firm_id=firm.id, account_number="U123456", broker_name="Internal Broker")
        db.add(broker)
        db.flush()
        db.add(UserRole(user_id=admin.id, role_id=role.id))

        db.add(
            Trade(
                broker_account_id=broker.id,
                strategy_id=strategy.id,
                option_contract_id=None,
                external_trade_id="T-001",
                symbol="AAPL",
                side="SELL",
                quantity=1,
                price=2.12,
                executed_at=datetime.now(UTC),
            )
        )
        db.add(
            MarginMetric(
                strategy_id=strategy.id,
                measured_at=datetime.now(UTC),
                notional_exposure=25000,
                margin_used=5200,
                broker_requirement=5000,
                source="broker",
            )
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
