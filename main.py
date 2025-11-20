# ============================================
# FATH UNIFIED BOT - MAIN FILE
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

# Handlers
from handlers.start_handler import register_start_handlers
from handlers.trading_handler import register_trading_handlers
from handlers.license_handler import register_license_handlers
from handlers.admin_handler import register_admin_handlers
from handlers.premium_handler import register_premium_handlers

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot va Dispatcher
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Barcha handlerlarni ro'yxatdan o'tkazish
register_start_handlers(dp)
register_admin_handlers(dp)
register_trading_handlers(dp)
register_license_handlers(dp)
register_premium_handlers(dp)


async def on_startup(dp):
    """Bot ishga tushganda"""
    print("\n" + "="*50)
    print("🤖 FATH UNIFIED BOT ISHGA TUSHDI!")
    print("="*50)
    print(f"📊 Bot Token: {config.BOT_TOKEN[:20]}...")
    print(f"👑 Adminlar: {config.ADMINS}")
    print(f"🗄️ Trading DB: {config.TRADING_DB_PATH}")
    print(f"🗄️ License DB: {config.LICENSE_DB_PATH}")
    print("="*50 + "\n")


async def on_shutdown(dp):
    """Bot to'xtaganda"""
    print("\n" + "="*50)
    print("⚠️ FATH BOT TO'XTATILDI")
    print("="*50 + "\n")
    
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == "__main__":
    try:
        # Papkalarni tekshirish
        os.makedirs(config.ANALYSES_DIR, exist_ok=True)
        os.makedirs(config.PRO_ANALYSES_DIR, exist_ok=True)
        
        # Botni ishga tushirish
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown
        )
    except KeyboardInterrupt:
        print("\n⚠️ Bot to'xtatildi (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ XATOLIK: {e}")