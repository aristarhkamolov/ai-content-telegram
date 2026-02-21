import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_config
from database import Database
from handlers.content import ContentHandler
from services.openai_service import OpenAIService


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    config = load_config()
    if not config.bot_token or not config.openai_api_key:
        raise RuntimeError("Set BOT_TOKEN and OPENAI_API_KEY environment variables before запуском")

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    db = Database(config.database_path)
    ai_service = OpenAIService(
        api_key=config.openai_api_key,
        text_model=config.openai_model,
        image_model=config.image_model,
    )

    content_handler = ContentHandler(db=db, ai_service=ai_service)
    dp.include_router(content_handler.setup())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
