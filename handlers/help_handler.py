import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки 'Помощь' из главного меню"""
    query = update.callback_query
    await query.answer()
    
    help_text = """
    🤖 **Физика PRO100 - Помощь**
    
    *Основные возможности бота:*
    
    📚 **Теоретический материал**
    • Полная теория по всем разделам физики
    • Структурировано по темам
    • Ключевые формулы в каждой теме
    
    📝 **Формулы**
    • Сборник всех основных формул
    • Подробные объяснения каждой формулы
    • Возможность подробного изучения
    • Разделено по темам для удобства
    
    🔢 **Решение задач**
    • Задачи разного уровня сложности
    • Пошаговые решения
    • Ответы с пояснениями
    • Навигация между задачами
    
    *Основные команды:*
    /start - Начать работу с ботом
    /help - Показать это сообщение
    
    *Как пользоваться ботом:*
    1. Нажмите /start для начала работы
    2. Выберите нужный раздел в меню
    3. Переходите по разделам и темам
    4. Используйте кнопку "Назад" для возврата
    
    *Разделы физики в боте:*
    1. Механика
    2. Молекулярная физика
    3. Термодинамика
    4. Электродинамика
    5. Оптика
    6. Квантовая физика
    7. Колебания и волны
    
    *Если возникли проблемы:*
    • Попробуйте перезапустить бот командой /start
    • Проверьте интернет-соединение
    • Убедитесь, что у вас последняя версия Telegram
    """
    
    keyboard = [
        [InlineKeyboardButton("❓ Часто задаваемые вопросы", callback_data='faq')],
        [InlineKeyboardButton("📞 Связь с разработчиком", callback_data='contact')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main')]
       ]
    
    await query.edit_message_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
    *Физика PRO100 - Команды и помощь*
    
    *Доступные команды:*
    /start - Запустить бота и показать главное меню
    /help - Показать это сообщение справки
    
    *Основные разделы бота:*
    • Теория - теоретический материал по всем темам
    • Формулы - сборник формул с пояснениями
    • Задачи - решение задач разной сложности
    
    *Для начала работы используйте:* /start
    
    *Советы по подготовке к экзамену:*
    1. Начинайте с теоретического материала
    2. Изучайте формулы с пониманием
    3. Решайте задачи от простых к сложным
    4. Регулярно повторяйте пройденное
    """

    keyboard = [
        [InlineKeyboardButton("❓ Часто задаваемые вопросы", callback_data='faq')],
        [InlineKeyboardButton("📞 Связь с разработчиком", callback_data='contact')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        help_text,
        reply_markup=reply_markup,  # Используем созданную клавиатуру
        parse_mode='Markdown'
    )

async def faq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Часто задаваемые вопросы"""
    query = update.callback_query
    await query.answer()
    
    faq_text = """
    ❓ *Часто задаваемые вопросы*
    
    *Q: Как часто обновляется материал?*
    A: Материал регулярно дополняется и обновляется.
    
    *Q: Достаточно ли материала для подготовки к экзамену?*
    A: Да, материал охватывает всю программу по предмету.
    
    *Q: Можно ли использовать бота на нескольких устройствах?*
    A: Да, бот доступен с любого устройства в Telegram.
    
    *Q: Бот бесплатный?*
    A: Да, бот полностью бесплатный.
    
    *Q: Как сообщить об ошибке?*
    A: Напишите разработчику через кнопку "Связь с разработчиком".
    """
    
    keyboard = [
        #[InlineKeyboardButton("📞 Связь с разработчиком", callback_data='contact')],
        [InlineKeyboardButton("🔙 Назад", callback_data='help')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main')]
    ]
    
    await query.edit_message_text(
        faq_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def contact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Связь с разработчиком"""
    query = update.callback_query
    await query.answer()
    
    contact_text = """
    📞 *Связь с разработчиком*
    
    Если вы нашли ошибку в боте, у вас есть предложения по улучшению или вопросы:
    
    *Email:* polinakrasko2025@gmail.com
    *Telegram:* @Mjoer
    
    *Что сообщать при обращении:*
    1. Ваш username в Telegram
    2. Описание проблемы
    3. Шаги для воспроизведения ошибки
    4. Скриншоты (если есть)
    
    *Время ответа:* 1-2 рабочих дня
    
    Спасибо за обратную связь! Она помогает делать бота лучше. ✨
    """
    
    keyboard = [
        #[InlineKeyboardButton("❓ Часто задаваемые вопросы", callback_data='faq')],
        [InlineKeyboardButton("🔙 Назад в помощь", callback_data='help')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main')]
    ]

    await query.edit_message_text(
        contact_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )