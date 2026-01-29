# config.py - ТОЛЬКО конфигурационные переменные
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Конфигурационные переменные (НИКАКИХ ИМПОРТОВ ДРУГИХ ФАЙЛОВ)
TOKEN = os.getenv('TELEGRAM_TOKEN', '8240699418:AAF4x6fnPglosNjE8c0PQhW8ReQEiubByuI')

# Пути к файлам с данными
THEORY_DATA_PATH = 'data/theory.json'
FORMULAS_DATA_PATH = 'data/formulas.json'
PROBLEMS_DATA_PATH = 'data/problems.json'

# Настройки для вебхуков
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
PORT = int(os.getenv('PORT', 8080))

# НИЧЕГО БОЛЬШЕ НЕ ДОБАВЛЯТЬ!