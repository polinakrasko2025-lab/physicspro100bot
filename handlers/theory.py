import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import THEORY_DATA_PATH

def load_theory_data():
    """Загружает теоретический материал из JSON файла"""
    try:
        with open(THEORY_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {THEORY_DATA_PATH} не найден!")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из {THEORY_DATA_PATH}")
        return {}

async def theory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки 'Теоретический материал'"""
    query = update.callback_query
    await query.answer()
    
    data = load_theory_data()
    if not data:
        await query.edit_message_text("Теоретический материал временно недоступен.")
        return
    
    sections = list(data.keys())
    
    text = "📚 *Выберите раздел для изучения теоретического материала:*"
    
    from keyboards.inline_keyboards import get_sections_menu
    await query.edit_message_text(
        text,
        reply_markup=get_sections_menu(sections, 'main'),
        parse_mode='Markdown'
    )

async def section_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора раздела теории"""
    query = update.callback_query
    await query.answer()
    
    section = query.data.replace('section_', '')
    data = load_theory_data()
    
    if section not in data:
        await query.edit_message_text(f"Раздел '{section}' не найден.")
        return
    
    topics = data.get(section, [])
    
    if not topics:
        text = f"📖 *Раздел: {section}*\n\nПока нет доступных тем в этом разделе."
        keyboard = [
            [InlineKeyboardButton("🔢 Перейти к задачам", callback_data=f'problems_section_{section}')],
            [InlineKeyboardButton("🔙 Назад", callback_data='theory_back')]
        ]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        return
    
    text = f"📖 *Раздел: {section}*\n\n*Выберите тему:*"
    
    from keyboards.inline_keyboards import get_theory_topics_menu
    await query.edit_message_text(
        text,
        reply_markup=get_theory_topics_menu(topics, section, 'theory_back'),
        parse_mode='Markdown'
    )

async def topic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора темы теории"""
    query = update.callback_query
    await query.answer()
    
    # Разбираем callback_data: format is 'topic_{section}_{index}'
    parts = query.data.split('_')
    if len(parts) != 3:
        await query.edit_message_text("Ошибка в данных темы.")
        return
    
    section = parts[1]
    try:
        index = int(parts[2])
    except ValueError:
        await query.edit_message_text("Ошибка в индексе темы.")
        return
    
    data = load_theory_data()
    
    if section not in data or index >= len(data[section]):
        await query.edit_message_text("Тема не найдена.")
        return
    
    topic = data[section][index]
    
    text = f"📚 *{topic['title']}*\n\n{topic['content']}"
    
    if 'formulas' in topic and topic['formulas']:
        text += "\n\n📝 *Ключевые формулы:*\n"
        for formula in topic['formulas']:
            text += f"• `{formula}`\n"
    
    keyboard = [
        [
            #InlineKeyboardButton("📝 Изучить формулы раздела", callback_data=f'formulas_section_{section}'),
            InlineKeyboardButton("🔢 Перейти к решению задач", callback_data=f'problems_section_{section}')
        ],
        [InlineKeyboardButton("🔙 Назад к темам", callback_data=f'section_{section}')]
    ]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def topic_studied_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение изучения темы (упрощенная версия)"""
    query = update.callback_query
    await query.answer("✅ Информация сохранена!")
    
    # Просто возвращаемся к теме
    await topic_callback(update, context)