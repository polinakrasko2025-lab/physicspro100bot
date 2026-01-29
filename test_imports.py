# test_imports.py
try:
    import telegram
    import telegram.ext
    import dotenv
    print("✅ Все библиотеки установлены!")
    print(f"python-telegram-bot версия: {telegram.__version__}")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Установите библиотеки: pip install python-telegram-bot python-dotenv")