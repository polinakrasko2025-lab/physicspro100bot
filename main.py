import logging
import json
import warnings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN, PROBLEMS_DATA_PATH

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
    except:
        return {}

def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Импорты обработчиков
    from handlers.commands import start_command
    from handlers.theory import theory_callback, section_callback, topic_callback, topic_studied_callback
    from handlers.formulas import formulas_callback, formulas_section_callback
    from handlers.formulas_detail import formulas_detail_callback
    from handlers.problems import problems_callback, problem_section_callback, show_problem
    from handlers.help_handler import help_command, help_callback, faq_callback, contact_callback
    
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
    
    # Обработка помощи
    application.add_handler(CallbackQueryHandler(faq_callback, pattern='^faq$'))
    application.add_handler(CallbackQueryHandler(contact_callback, pattern='^contact$'))
    
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

async def handle_text_messages(update: Update, context):
    """Обработка текстовых сообщений"""
    text = update.message.text.lower()
    
    if any(word in text for word in ['привет', 'hello', 'hi', 'start']):
        await update.message.reply_text(
            "👋 Привет! Используйте /start для начала работы или /help для помощи."
        )
    elif any(word in text for word in ['спасибо', 'thanks', 'thank you']):
        await update.message.reply_text(
            "🙏 Пожалуйста! Рад помочь в подготовке к экзамену по физике!"
        )
    elif any(word in text for word in ['помощь', 'help', 'как пользоваться']):
        from handlers.help_handler import help_command
        await help_command(update, context)
    else:
        await update.message.reply_text(
            "🤖 Я бот, который поможет подготоится к экзамену по физике. Используйте меню для навигации.\n"
            "Доступные команды:\n"
            "/start - Главное меню\n"
            "/help - Помощь и инструкции",
            parse_mode='Markdown'
        )

async def handle_back_buttons(update: Update, context):
    """Обработчик кнопок 'Назад'"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data == 'main':
        from keyboards.inline_keyboards import get_main_menu
        await query.edit_message_text(
            "🎓 *Главное меню бота Физика PRO100*\n\nВыберите, с чего бы хотели начать изучение:",
            reply_markup=get_main_menu(),
            parse_mode='Markdown'
        )
    elif callback_data == 'theory_back':
        from handlers.theory import theory_callback
        await theory_callback(update, context)
    elif callback_data == 'formulas_back':
        from handlers.formulas import formulas_callback
        await formulas_callback(update, context)
    elif callback_data == 'problems_back':
        from handlers.problems import problems_callback
        await problems_callback(update, context)

async def handle_solution(update: Update, context):
    """Показать решение задачи"""
    query = update.callback_query
    await query.answer()
    
    # Разбираем callback_data: solution_{section}_{index}
    _, section, index = query.data.split('_')
    index = int(index)
    
    data = load_problems()
    
    if section not in data or index >= len(data[section]):
        await query.edit_message_text("Задача не найдена.")
        return
    
    problem = data[section][index]
    
    text = f"📝 *Задача {index + 1}*\n\n"
    text += f"*Раздел: {section}*\n\n"
    text += f"*Условие:*\n{problem['problem']}\n\n"
    text += f"*✅ Решение:*\n{problem['solution']}\n\n"
    text += f"*📌 Ответ:* {problem['answer']}"
    
    # Вычисляем индекс следующей задачи (линейная навигация только вперед)
    problems = data[section]
    next_index = index + 1
    show_next_button = next_index < len(problems)
    
    keyboard = []
    
    # Добавляем кнопку "Следующая" только если есть следующая задача
    if show_next_button:
        keyboard.append([InlineKeyboardButton("Следующая ▶️", callback_data=f'next_problem_{section}_{index}')])
    
    keyboard.extend([
       # [InlineKeyboardButton("🔢 Еще задачи", callback_data=f'problems_section_{section}')],
        [InlineKeyboardButton("🔙 Главное меню", callback_data='main')]
    ])
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_problem_navigation(update: Update, context):
    """Навигация по задачам (только вперед)"""
    query = update.callback_query
    await query.answer()
    
    # Разбираем callback_data: next_problem_{section}_{index}
    parts = query.data.split('_')
    section = parts[2]
    current_index = int(parts[3])
    
    data = load_problems()
    
    if section not in data:
        await query.edit_message_text("Раздел не найден.")
        return
    
    problems = data[section]
    
    # Определяем новый индекс (только следующая задача)
    new_index = current_index + 1
    
    # Если это последняя задача, не показываем кнопку "Следующая"
    if new_index >= len(problems):
        new_index = 0  # Или можно оставить текущий индекс и не показывать кнопку
    
    # Показываем задачу с новым индексом
    from handlers.problems import show_problem
    await show_problem(update, context, section, new_index)

if __name__ == '__main__':
    main()