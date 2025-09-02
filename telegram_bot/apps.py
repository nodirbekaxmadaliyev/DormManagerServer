from django.apps import AppConfig
import threading
import asyncio
import os

class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        # Django autoreload bilan xatolik chiqmasligi uchun
        if os.environ.get("RUN_MAIN"):
            from .bot import dp, bot
            def start_loop():
                asyncio.run(dp.start_polling(bot))
            threading.Thread(target=start_loop, daemon=True).start()
