import csv
from sqlalchemy.exc import SQLAlchemyError
from database import Base, engine, SessionLocal
from models import Account

Base.metadata.create_all(bind=engine)

CSV_FILE = "fraudshield_accounts.csv"


def seed_accounts():
    db = SessionLocal()
    accounts = []

    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                accounts.append(
                    Account(
                        vpa=row["vpa"].strip(),
                        acc_holder_name=row["acc_holder_name"].strip(),
                        account_type=row["account_type"],
                        mcc=row.get("mcc") or None,
                        kyc_status=row["kyc_status"],
                        geohash=row.get("geohash") or None,
                        account_age_days=int(row["account_age_days"] or 0),
                        status=row.get("status") or "ACTIVE",
                        fraud_reports=int(row.get("fraud_reports") or 0),
                    )
                )

        db.bulk_save_objects(accounts)
        db.commit()
        print(f"✅ Successfully seeded {len(accounts)} accounts")

    except FileNotFoundError:
        print(f"❌ CSV file not found: {CSV_FILE}")

    except SQLAlchemyError as e:
        db.rollback()
        print("❌ Database error while seeding accounts")
        print(e)

    except Exception as e:
        db.rollback()
        print("❌ Unexpected error occurred")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_accounts()
