from datetime import UTC, datetime

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.entities import BrokerAccount, MarginMetric, Role, Strategy, Trade, User


def run() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(User).where(User.email == "admin@icc.local")):
            return

        admin = User(email="admin@icc.local", full_name="Platform Admin", password_hash=hash_password("ChangeMe123!"))
        role = Role(name="admin")
        broker = BrokerAccount(account_number="U123456", broker_name="Internal Broker")
        strategy = Strategy(name="Income Wheel", description="CSP and covered call cycle")
        db.add_all([admin, role, broker, strategy])
        db.flush()

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
