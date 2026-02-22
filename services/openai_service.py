import base64
from openai import AsyncOpenAI


class OpenAIService:
    def __init__(self, api_key: str, text_model: str, image_model: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.text_model = text_model
        self.image_model = image_model

    @staticmethod
    def _profile_block(user: dict) -> str:
        return (
            f"Ниша: {user['niche']}\n"
            f"Стиль: {user['style']}\n"
            f"Цель канала: {user['goal']}\n"
            f"Целевая аудитория: {user['audience']}"
        )

    async def generate_week_plan(self, user: dict) -> str:
        prompt = (
            "Создай контент-план на 7 дней для Telegram канала. "
            "Сделай структуру: День, тема, формат, цель поста. "
            "Пиши на русском, ясно и практично.\n\n"
            f"Данные:\n{self._profile_block(user)}"
        )
        response = await self.client.responses.create(
            model=self.text_model,
            input=prompt,
            temperature=0.7,
        )
        return response.output_text.strip()

    async def generate_post(self, user: dict) -> str:
        prompt = (
            "Напиши готовый Telegram-пост для канала на русском языке. "
            "Добавь цепляющий заголовок, основную мысль, призыв к действию и 3 релевантных хэштега.\n\n"
            f"Данные:\n{self._profile_block(user)}"
        )
        response = await self.client.responses.create(
            model=self.text_model,
            input=prompt,
            temperature=0.8,
        )
        return response.output_text.strip()

    async def generate_reels_ideas(self, user: dict) -> str:
        prompt = (
            "Сгенерируй 5 идей Reels для продвижения Telegram-канала. "
            "Для каждой идеи укажи: хук, сценарий (3 шага), CTA. "
            "Пиши кратко и по делу на русском.\n\n"
            f"Данные:\n{self._profile_block(user)}"
        )
        response = await self.client.responses.create(
            model=self.text_model,
            input=prompt,
            temperature=0.8,
        )
        return response.output_text.strip()

    async def generate_image(self, user: dict) -> bytes:
        prompt = (
            "Создай реалистичную и современную иллюстрацию для Telegram-поста с учетом брифа:\n"
            f"{self._profile_block(user)}\n"
            "Без текста на изображении, композиция под формат 1:1."
        )
        response = await self.client.images.generate(
            model=self.image_model,
            prompt=prompt,
            size="1024x1024",
        )
        b64_data = response.data[0].b64_json
        return base64.b64decode(b64_data)
