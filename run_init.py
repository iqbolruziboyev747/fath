# ============================================
# RUN INIT — BARCHA DATABASELARNI YARATISH
# ============================================

import os
import sys
from datetime import datetime

# Joriy papkani PYTHON pathga qo‘shish
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

print("📁 Project root:", base_dir)

# Config
import config

# SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Database bazaviy obyektlar
from database.base import Base, trading_engine, license_engine

# Trading DB modellar
from database.trading_models import (
    User,
    Analysis,
    EconomicData,
    InsiderNews
)

# License DB modellar
from database.license_models import (
    License,
    PricingPlan,
    Referral,
    ReferralCode
)

# ============================================
# TRADING DATABASE INIT
# ============================================

def init_trading_database():
    print("\n🔧 Trading database yaratilmoqda...")

    # Jadvallarni yaratish
    Base.metadata.create_all(bind=trading_engine)

    # Session
    Session = sessionmaker(bind=trading_engine)
    session = Session()

    # Boshlang‘ich EconomicData mavjudmi?
    try:
        if not session.query(EconomicData).first():
            session.add(
                EconomicData(
                    inflation='3.2%',
                    fed_rate='5.25-5.5%',
                    dollar_index='104.8',
                    unemployment='3.8%',
                    gdp_growth='2.1%',
                    btc_news="Bitcoin ETF oqimlari: So'nggi haftada $500M kirim|FED raisi bayonoti: Foiz stavkalari barqaror|Global regulyator: Kripto qonunchiligi muhokamasi",
                    gold_news="Oltin narxi: Markaziy banklar zaxira o‘sishi|Inflyatsiya: So‘nggi ma’lumotlar ijobiy|Geosiyosiy: Yaqin Sharq vaziyati ta’siri",
                    updated_by=config.ADMINS[0]
                )
            )
            session.commit()
            print("✅ Boshlang‘ich EconomicData qo‘shildi")

    except Exception as e:
        print("❌ Trading DB init error:", e)

    finally:
        session.close()

    print("✅ Trading database tayyor!")

# ============================================
# LICENSE DATABASE INIT
# ============================================

def init_license_database():
    print("\n🔧 License database yaratilmoqda...")

    # Jadvallarni yaratish
    Base.metadata.create_all(bind=license_engine)

    Session = sessionmaker(bind=license_engine)
    session = Session()

    try:
        # Boshlang'ich tariflar
        if session.query(PricingPlan).count() == 0:
            for plan in config.DEFAULT_PLANS:
                session.add(PricingPlan(**plan))

            session.commit()
            print(f"✅ {len(config.DEFAULT_PLANS)} ta tarif qo‘shildi")

    except Exception as e:
        print("❌ License DB init error:", e)

    finally:
        session.close()

    print("✅ License database tayyor!")


# ============================================
# ALL INIT
# ============================================

def initialize_all():
    print("="*50)
    print("📊 DATABASE INITIALIZATION")
    print("="*50)

    init_trading_database()
    init_license_database()

    print("\n🎉 BARCHA DATABASELAR MUVAFFAQIYATLI YARATILDI!")
    print("="*50)


# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    initialize_all()
