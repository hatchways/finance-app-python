import json
from datetime import datetime

from api.core.security import get_password_hash
from api.dependencies.db import get_db
from api.models import Account, Transaction, User
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm.session import Session

SEED_DIRECTORY = "seed_data"


def convert_str_to_datetime(datetime_str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


def seed_data(db: Session):
    print("-- Seeding User --")

    # Create user
    user1 = User(email="test@test.com", password_digest=get_password_hash("sample"))
    db.add(user1)

    # Load account data
    print("-- Seeding Accounts --")
    with open(f"{SEED_DIRECTORY}/accounts.json", "r") as accounts_seed_file:
        seed_json = json.load(accounts_seed_file)
        for account in seed_json["accounts"]:
            account = Account(
                user=user1,
                name=account["name"],
                plaid_account_id=account["plaid_account_id"],
                mask=account["mask"],
                official_name=account["official_name"],
                current_balance_str=account["current_balance"] or 0,
                iso_currency_code=account["iso_currency_code"],
                unofficial_currency_code=account["unofficial_currency_code"],
                account_subtype=account["account_subtype"],
                account_type=account["account_type"],
            )
            db.add(account)
        db.commit()

    # Load transaction data
    print("-- Seeding Transactions --")
    with open(f"{SEED_DIRECTORY}/transactions.json", "r") as transactions_seed_file:
        seed_json = json.load(transactions_seed_file)

        latest_date = convert_str_to_datetime(seed_json["transactions"][0]["date"])
        for t in seed_json["transactions"]:
            if convert_str_to_datetime(t["date"]) > latest_date:
                latest_date = convert_str_to_datetime(t["date"])

        # Calculate date offset so all transactions are shifted to the correct date range
        today = datetime.today()
        months_offset_from_today = (today.year - latest_date.year) * 12 + (
            today.month - latest_date.month
        )
        months_offset_from_last_month = (
            months_offset_from_today - 1 if months_offset_from_today > 0 else 0
        )

        # loop through all transactions and save to db
        for transaction in seed_json["transactions"]:
            account = (
                db.query(Account)
                .filter_by(plaid_account_id=transaction["plaid_account_id"])
                .one_or_none()
            )
            if not account:
                continue

            transaction_date = convert_str_to_datetime(transaction["date"])

            # Shift the date based on offset calculated above
            new_transaction_date = transaction_date + relativedelta(
                months=months_offset_from_last_month
            )
            trans = Transaction(
                account=account,
                user=user1,
                plaid_transaction_id=transaction["plaid_transaction_id"],
                plaid_category_id=transaction["plaid_category_id"],
                categories=transaction["categories"],
                type=transaction["type"],
                name=transaction["name"],
                amount_str=transaction["amount"],
                iso_currency_code=transaction["iso_currency_code"],
                unofficial_currency_code=transaction["unofficial_currency_code"],
                date=new_transaction_date,
                pending=transaction["pending"],
            )
            db.add(trans)

    try:
        db.commit()
        print("-- Seeding Complete --")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    db = next(get_db())
    seed_data(db)
