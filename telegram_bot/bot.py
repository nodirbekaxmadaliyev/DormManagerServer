# import os, django — O'chirilsin!
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router
from asgiref.sync import sync_to_async

from student.models import Student  # Django allaqachon setup qilgan

BOT_TOKEN = "8461684638:AAFL-YIZQKYPkgzqrtBdMohdlCXfTiwd0FY"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

@router.message(CommandStart())
async def start_handler(message: Message):
    button = KeyboardButton(text="📱 Telefon raqam yuborish", request_contact=True)
    kb = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Iltimos, telefon raqamingizni yuboring:", reply_markup=kb)

@router.message(lambda msg: msg.contact is not None)
async def contact_handler(message: Message):
    phone = message.contact.phone_number.replace("+", "").replace(" ", "")
    chat_id = message.chat.id

    from asgiref.sync import sync_to_async

    # Student topish
    @sync_to_async
    def get_student_by_phone(phone):
        # parent_full_name ichida phone borligini tekshirish
        return Student.objects.get(parent_full_name__icontains=phone)

    # chat_id saqlash
    @sync_to_async
    def save_chat_id(student, chat_id):
        student.chat_id = chat_id
        student.save()

    try:
        student = await get_student_by_phone(phone)
        await save_chat_id(student, chat_id)
        await message.answer("✅ Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz.")
    except Student.DoesNotExist:
        await message.answer("❌ Bu raqamga mos o‘quvchi topilmadi.")
