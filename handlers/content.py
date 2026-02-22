from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, Message

from database import Database
from services.openai_service import OpenAIService


router = Router()


class RegistrationStates(StatesGroup):
    niche = State()
    style = State()
    goal = State()
    audience = State()


class ContentHandler:
    def __init__(self, db: Database, ai_service: OpenAIService) -> None:
        self.db = db
        self.ai_service = ai_service

    def setup(self) -> Router:
        router.message.register(self.start, Command("start"))
        router.message.register(self.niche, RegistrationStates.niche)
        router.message.register(self.style, RegistrationStates.style)
        router.message.register(self.goal, RegistrationStates.goal)
        router.message.register(self.audience, RegistrationStates.audience)
        router.message.register(self.plan, Command("plan"))
        router.message.register(self.post, Command("post"))
        router.message.register(self.image, Command("image"))
        router.message.register(self.fallback, F.text)
        return router

    async def start(self, message: Message, state: FSMContext) -> None:
        await state.set_state(RegistrationStates.niche)
        await message.answer(
            "Привет! Я AI-контент агент для Telegram.\n"
            "Сначала зарегистрируем твой бриф.\n\n"
            "1/4: Какая у тебя ниша?"
        )

    async def niche(self, message: Message, state: FSMContext) -> None:
        self.db.upsert_user_field(message.from_user.id, "niche", message.text)
        await state.set_state(RegistrationStates.style)
        await message.answer("2/4: Какой стиль контента предпочитаешь?")

    async def style(self, message: Message, state: FSMContext) -> None:
        self.db.upsert_user_field(message.from_user.id, "style", message.text)
        await state.set_state(RegistrationStates.goal)
        await message.answer("3/4: Какая цель канала?")

    async def goal(self, message: Message, state: FSMContext) -> None:
        self.db.upsert_user_field(message.from_user.id, "goal", message.text)
        await state.set_state(RegistrationStates.audience)
        await message.answer("4/4: Кто твоя целевая аудитория?")

    async def audience(self, message: Message, state: FSMContext) -> None:
        self.db.upsert_user_field(message.from_user.id, "audience", message.text)
        await state.clear()
        await message.answer(
            "Отлично, профиль сохранен ✅\n"
            "Доступные команды:\n"
            "/plan — контент-план на 7 дней\n"
            "/post — готовый Telegram-пост + идеи Reels\n"
            "/image — сгенерировать изображение"
        )

    def _get_user_or_warn(self, telegram_id: int):
        if not self.db.is_profile_complete(telegram_id):
            return None
        return self.db.get_user(telegram_id)

    async def plan(self, message: Message) -> None:
        user = self._get_user_or_warn(message.from_user.id)
        if not user:
            await message.answer("Сначала заполни профиль через /start.")
            return

        await message.answer("Готовлю контент-план на 7 дней... ⏳")
        plan = await self.ai_service.generate_week_plan(user)
        await message.answer(plan)

    async def post(self, message: Message) -> None:
        user = self._get_user_or_warn(message.from_user.id)
        if not user:
            await message.answer("Сначала заполни профиль через /start.")
            return

        await message.answer("Генерирую пост и идеи Reels... ⏳")
        post_text = await self.ai_service.generate_post(user)
        reels = await self.ai_service.generate_reels_ideas(user)
        await message.answer(f"📝 Пост:\n\n{post_text}\n\n🎬 Идеи Reels:\n\n{reels}")

    async def image(self, message: Message) -> None:
        user = self._get_user_or_warn(message.from_user.id)
        if not user:
            await message.answer("Сначала заполни профиль через /start.")
            return

        await message.answer("Генерирую изображение... ⏳")
        image_bytes = await self.ai_service.generate_image(user)
        image_file = BufferedInputFile(image_bytes, filename="content-image.png")
        await message.answer_photo(image_file, caption="Готово! Изображение для твоего контента.")

    async def fallback(self, message: Message) -> None:
        await message.answer("Не понял команду. Используй /start, /plan, /post или /image.")
