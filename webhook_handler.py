# webhook_handler.py
import os
import json
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота (можно через переменную окружения)
TOKEN = os.getenv('TELEGRAM_TOKEN', '8240699418:AAF4x6fnPglosNjE8c0PQhW8ReQEiubByuI')

# Глобальная переменная для приложения
application = None

async def setup_bot():
    """Настройка и инициализация бота"""
    global application
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Импорты обработчиков (делаем внутри функции чтобы избежать циклических импортов)
    from handlers.commands import start_command
    from handlers.help_handler import help_command, help_callback, faq_callback, contact_callback
    from handlers.theory import theory_callback, section_callback, topic_callback, topic_studied_callback
    from handlers.formulas import formulas_callback, formulas_section_callback
    from handlers.formulas_detail import formulas_detail_callback
    from handlers.problems import problems_callback, problem_section_callback, show_problem
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Регистрация обработчиков callback-запросов для главного меню
    application.add_handler(CallbackQueryHandler(theory_callback, pattern='^theory$'))
    application.add_handler(CallbackQueryHandler(formulas_callback, pattern='^formulas$'))
    application.add_handler(CallbackQueryHandler(problems_callback, pattern='^problems$'))
    application.add_handler(CallbackQueryHandler(help_callback, pattern='^help$'))
    application.add_handler(CallbackQueryHandler(contact_callback, pattern='^contact$'))
    application.add_handler(CallbackQueryHandler(faq_callback, pattern='^faq$'))
    
    # Обработка разделов теории
    application.add_handler(CallbackQueryHandler(section_callback, pattern='^section_'))
    application.add_handler(CallbackQueryHandler(topic_callback, pattern='^topic_'))
    application.add_handler(CallbackQueryHandler(topic_studied_callback, pattern='^topic_studied_'))
    
    # Обработка формул по разделам
    application.add_handler(CallbackQueryHandler(formulas_section_callback, pattern='^formulas_section_'))
    application.add_handler(CallbackQueryHandler(formulas_detail_callback, pattern='^formula_detail_'))
    
    # Обработка задач (упрощенно для Bothost)
    application.add_handler(CallbackQueryHandler(problems_callback, pattern='^problems$'))
    application.add_handler(CallbackQueryHandler(problem_section_callback, pattern='^problems_section_'))
    
    # Обработка текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text_messages
    ))
    
    # Инициализируем приложение
    await application.initialize()
    print("✅ Бот инициализирован и готов к работе на Bothost")
    
    # Устанавливаем вебхук
    webhook_url = os.getenv('WEBHOOK_URL', '')
    if webhook_url:
        await application.bot.set_webhook(webhook_url)
        print(f"✅ Вебхук установлен: {webhook_url}")

async def handle_text_messages(update: Update, context):
    """Обработка текстовых сообщений"""
    text = update.message.text.lower()
    
    if any(word in text for word in ['привет', 'hello', 'hi']):
        await update.message.reply_text(
            "👋 Привет! Используйте /start для начала работы."
        )
    else:
        await update.message.reply_text(
            "🤖 Я бот для подготовки к физике. Используйте /start для главного меню."
        )

def handle_webhook(request):
    """
    Основная функция для Bothost.
    Bothost будет вызывать эту функцию при каждом обновлении от Telegram.
    """
    global application
    
    # Инициализируем бота при первом вызове
    if application is None:
        print("🚀 Первая инициализация бота...")
        asyncio.run(setup_bot())
    
    try:
        # Получаем JSON данные из запроса
        update_data = request.get_json(force=True)
        
        # Создаем объект Update из полученных данных
        update = Update.de_json(update_data, application.bot)
        
        # Обрабатываем обновление асинхронно
        asyncio.run(application.process_update(update))
        
        return {"ok": True, "message": "Update processed successfully"}
        
    except Exception as e:
        print(f"❌ Ошибка при обработке вебхука: {e}")
        return {"ok": False, "error": str(e)}, 500

# Функция для проверки работоспособности (опционально)
def health_check():
    """Проверка здоровья бота для Bothost"""
    return {"status": "online", "service": "physics_bot"}, 200