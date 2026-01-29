from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
    🎓 *Добро пожаловать в Физика PRO100!*
    
    Я помогу вам подготовиться к экзамену по физике.
    
    *Возможности бота:*
    📚 Теоретический материал по всем разделам
    📝 Формулы с подробным описанием
    🔢 Решение задач с пошаговыми объяснениями
    ❓ Помощь и поддержка
            """

    from keyboards.inline_keyboards import get_main_menu
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )
