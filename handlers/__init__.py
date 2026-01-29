"""
Пакет обработчиков команд и callback-запросов бота
"""

from .commands import start_command
from .theory import (
    theory_callback, 
    section_callback, 
    topic_callback,
    topic_studied_callback,
    load_theory_data
)
from .formulas import (
    formulas_callback,
    formulas_section_callback,
    load_formulas_data
)
from .formulas_detail import formulas_detail_callback
from .problems import (
    problems_callback,
    problem_section_callback,
    show_problem,
    load_problems_data
)
from .help_handler import (
    help_callback,
    help_command,
    faq_callback,
    contact_callback
)

__all__ = [
    # Команды
    'start_command',
    'help_command',
    
    # Теория
    'theory_callback',
    'section_callback',
    'topic_callback',
    'topic_studied_callback',
    'load_theory_data',
    
    # Формулы
    'formulas_callback',
    'formulas_section_callback',
    'formulas_detail_callback',
    'load_formulas_data',
    
    # Задачи
    'problems_callback',
    'problem_section_callback',
    'show_problem',
    'load_problems_data',
    
    # Помощь
    'help_callback',
    'faq_callback',
    'contact_callback'
]