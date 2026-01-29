import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import PROBLEMS_DATA_PATH

def load_problems_data():
    """Загружает задачи из JSON файла"""
    try:
        with open(PROBLEMS_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {PROBLEMS_DATA_PATH} не найден!")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из {PROBLEMS_DATA_PATH}")
        return {}

async def problems_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки 'Решение задач'"""
    query = update.callback_query
    await query.answer()
    
    data = load_problems_data()
    if not data:
        await query.edit_message_text("Задачи временно недоступны.")
        return
    
    sections = list(data.keys())
    
    text = "🔢 *Выберите раздел для решения задач:*"
    
    from keyboards.inline_keyboards import get_problems_sections_menu
    await query.edit_message_text(
        text,
        reply_markup=get_problems_sections_menu(sections, 'main'),
        parse_mode='Markdown'
    )

async def problem_section_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора раздела задач"""
    query = update.callback_query
    await query.answer()
    
    section = query.data.replace('problems_section_', '')
    data = load_problems_data()
    
    if section not in data:
        await query.edit_message_text(f"Раздел '{section}' не найден.")
        return
    
    problems = data.get(section, [])
    
    if not problems:
        text = f"В разделе '{section}' пока нет задач."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='problems_back')]]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        return
    
    # Показываем первую задачу
    await show_problem(update, context, section, 0)

async def show_problem(update: Update, context: ContextTypes.DEFAULT_TYPE, section: str, index: int):
    """Показывает конкретную задачу"""
    query = update.callback_query
    await query.answer()
    
    data = load_problems_data()
    
    if section not in data:
        await query.edit_message_text(f"Раздел '{section}' не найден.")
        return
    
    problems = data[section]
    
    # Проверяем корректность индекса
    if index < 0:
        index = 0  # Если индекс отрицательный, переходим к первой задаче
    elif index >= len(problems):
        index = 0  # Если индекс больше количества задач, переходим к первой
    
    problem = problems[index]
    
    text = f"📝 *Задача {index + 1} из {len(problems)}*\n\n"
    text += f"*Раздел: {section}*\n\n"
    text += f"{problem['problem']}\n\n"
    text += "Нажмите '👁 Показать решение', чтобы увидеть ответ."
    
    # Вычисляем индекс следующей задачи (линейная навигация только вперед)
    next_index = index + 1
    show_next_button = next_index < len(problems)
    
    keyboard = [
        [InlineKeyboardButton("👁 Показать решение", callback_data=f'solution_{section}_{index}')],
    ]
    
    # Добавляем кнопку "Следующая" только если есть следующая задача
    if show_next_button:
        keyboard.append([InlineKeyboardButton("Следующая ▶️", callback_data=f'next_problem_{section}_{index}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад к разделам", callback_data='problems_back')])
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )