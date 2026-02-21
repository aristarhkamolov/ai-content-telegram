# AI Content Telegram Bot

Telegram-бот на **Python + aiogram + OpenAI + SQLite** для генерации контента.

## Возможности

- Регистрация и сбор брифа пользователя:
  - ниша
  - стиль
  - цель канала
  - целевая аудитория
- Генерация:
  - контент-план на 7 дней (`/plan`)
  - готовый пост для Telegram + идеи Reels (`/post`)
  - изображение через OpenAI (`/image`)

## Структура проекта

- `bot.py` — точка входа
- `config.py` — конфигурация и env-переменные
- `database.py` — SQLite работа с пользователями
- `handlers/` — обработчики команд и FSM-анкета
- `services/` — интеграция с OpenAI API
- `requirements.txt` — зависимости

## Команды бота

- `/start` — старт и регистрация
- `/plan` — контент-план на 7 дней
- `/post` — Telegram-пост + идеи Reels
- `/image` — генерация изображения

## Быстрый запуск

### 1. Клонируйте проект и создайте venv

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Создайте `.env`

```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_IMAGE_MODEL=gpt-image-1
DATABASE_PATH=bot.db
```

### 4. Запустите бота

```bash
python bot.py
```

## Примечания

- SQLite база (`bot.db`) создается автоматически.
- Перед использованием команд `/plan`, `/post`, `/image` нужно пройти `/start` и заполнить профиль.
