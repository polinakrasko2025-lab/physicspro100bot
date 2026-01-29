import logging
import json
import warnings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN, PROBLEMS_DATA_PATH

load_dotenv()

import os

TOKEN = os.getenv('TOKEN', '8240699418:AAF4x6fnPglosNjE8c0PQhW8ReQEiubByuI')

# Пути к файлам с данными
THEORY_DATA_PATH = 'data/theory.json'
FORMULAS_DATA_PATH = 'data/formulas.json'
PROBLEMS_DATA_PATH = 'data/problems.json'

# Настройки для вебхуков
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
PORT = int(os.getenv('PORT', 8080))