# main.py - ОСНОВНОЙ ФАЙЛ
import os
import json
import logging
import warnings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# НЕ импортируем из config.py в начале, если есть циклические импорты
# Вместо этого определим переменные здесь или используем os.getenv()

# Получаем токен напрямую из переменных окружения
TOKEN = os.getenv('TELEGRAM_TOKEN', '8240699418:AAF4x6fnPglosNjE8c0PQhW8ReQEiubByuI')

# Пути к файлам
PROBLEMS_DATA_PATH = 'data/problems.json'

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Игнорируем предупреждение о pkg_resources
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

def load_problems():
    """Загружает задачи"""
    try:
        with open(PROBLEMS_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading problems: {e}")
        return {}

def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Импорты обработчиков (ДЕЛАЕМ ВНУТРИ ФУНКЦИИ)
    try:
        from handlers.commands import start_command
        from handlers.theory import theory_callback, section_callback, topic_callback, topic_studied_callback
        from handlers.formulas import formulas_callback, formulas_section_callback
        from handlers.formulas_detail import formulas_detail_callback
        from handlers.problems import problems_callback, problem_section_callback, show_problem
        from handlers.help_handler import help_command, help_callback, faq_callback, contact_callback
        
        print("✅ Все обработчики успешно импортированы")
    except ImportError as e:
        logging.error(f"Import error: {e}")
        return
    
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
    
    # Обработка задач
    application.add_handler(CallbackQueryHandler(problem_section_callback, pattern='^problems_section_'))
    application.add_handler(CallbackQueryHandler(handle_problem_navigation, pattern='^next_problem_'))
    application.add_handler(CallbackQueryHandler(handle_solution, pattern='^solution_'))
    
    # Обработка кнопок "Назад"
    application.add_handler(CallbackQueryHandler(handle_back_buttons, pattern='^(main|theory_back|formulas_back|problems_back)$'))
    
    # Обработка текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text_messages
    ))
    
    # Обработчик ошибок
    async def error_handler(update: Update, context):
        logging.error(f"Ошибка при обработке обновления: {update}")
        if context.error:
            logging.error(f"Контекст ошибки: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ Произошла ошибка. Попробуйте еще раз или используйте /help для помощи.",
                parse_mode='Markdown'
            )
    
    application.add_error_handler(error_handler)
    
    # Запуск бота
    print("✅ Бот запущен и ожидает сообщений...")
    print("🔗 Ссылка на бота: https://t.me/PhysicsPRO100bot")
    print("📚 Доступные разделы: Теория, Формулы, Задачи, Помощь")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

# ... остальные функции handle_text_messages, handle_back_buttons и т.д.
# ОСТАВЬТЕ ИХ БЕЗ ИЗМЕНЕНИЙ