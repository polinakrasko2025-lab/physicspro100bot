# webhook_handler.py - ДЛЯ BOTHOST
import os
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен напрямую (для Bothost)
TOKEN = '8240699418:AAF4x6fnPglosNjE8c0PQhW8ReQEiubByuI'

print("🚀 Starting PhysicsPRO100Bot on Bothost...")

def handle_webhook(request):
    """
    Основная функция для Bothost.
    Bothost будет вызывать эту функцию при каждом обновлении.
    """
    try:
        print("📨 Received webhook request")
        
        # Импортируем ВНУТРИ функции чтобы избежать циклических импортов
        from telegram import Update
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler
        
        # Инициализируем приложение
        app = Application.builder().token(TOKEN).build()
        
        # Импортируем и регистрируем обработчики
        from handlers.commands import start_command
        from handlers.help_handler import help_command, help_callback
        
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CallbackQueryHandler(help_callback, pattern='^help$'))
        
        # Получаем данные от Telegram
        update_data = request.get_json(force=True)
        
        # Обрабатываем обновление
        import asyncio
        
        async def process_update():
            await app.initialize()
            update = Update.de_json(update_data, app.bot)
            await app.process_update(update)
        
        asyncio.run(process_update())
        
        print("✅ Update processed successfully")
        return {"ok": True}
        
    except Exception as e:
        print(f"❌ Error in handle_webhook: {e}")
        return {"ok": False, "error": str(e)}, 500

def health_check():
    """Проверка здоровья бота"""
    return {"status": "online", "service": "PhysicsPRO100Bot"}, 200

print("✅ Webhook handler initialized and ready")