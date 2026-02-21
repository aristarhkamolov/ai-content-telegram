from dotenv import load_dotenv
from dataclasses import dataclass
import os


@dataclass
class Config:
    bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    image_model: str = "gpt-image-1"
    database_path: str = "bot.db"




load_dotenv()

def load_config() -> Config:
    return Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        image_model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1"),
        database_path=os.getenv("DATABASE_PATH", "bot.db"),
    )
