import logging

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async

from railway.keyboards import get_main_menu
from railway.models import BotAdmin

from django.conf import settings
from aiogram.client.default import DefaultBotProperties

from railway.states import AdminState

router = Router()
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logger = logging.getLogger(__name__)


def is_admin(user_id):
    return BotAdmin.objects.filter(user_id=user_id).exists()


@router.message(CommandStart())
async def welcome(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    user = await BotAdmin.objects.filter(telegram_id=user_id).afirst()

    if not user:
        await message.answer("❌ Siz admin emassiz!")
        return

    update_data = {}
    if not user.full_name and full_name:
        update_data["full_name"] = full_name
    if not user.tg_username and username:
        update_data["tg_username"] = username

    if update_data:
        await BotAdmin.objects.filter(telegram_id=user_id).aupdate(**update_data)

    main_menu_markup = get_main_menu()
    await message.answer(
        text="🔹 Salom, Admin! Asosiy menyudasiz.",
        reply_markup=main_menu_markup,
        parse_mode="HTML"
    )


@router.message(lambda message: message.text == "admin ➕")
async def ask_for_admin_id(message: Message, state: FSMContext):
    await state.set_state(AdminState.waiting_for_admin_id)
    await message.answer("🆔 Yangi adminning Telegram ID sini yuboring:")


@router.message(AdminState.waiting_for_admin_id)
async def add_admin(message: Message, state: FSMContext):
    try:
        new_admin_id = int(message.text)
        existing_admin = await BotAdmin.objects.filter(telegram_id=new_admin_id).afirst()

        if existing_admin:
            await message.answer("❗ Bu foydalanuvchi allaqachon admin!")
        else:
            await BotAdmin.objects.acreate(telegram_id=new_admin_id)
            await message.answer(f"✅ Foydalanuvchi (ID: {new_admin_id}) admin sifatida qo‘shildi!")

        await state.clear()
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam yuboring!")


@router.message(lambda message: message.text == "admin ➖")
async def show_admin_list(message: Message):
    admins = list(await sync_to_async(list)(BotAdmin.objects.all()))

    if not admins:
        await message.answer("❗ Hech qanday admin mavjud emas.")
        return

    keyboard = InlineKeyboardBuilder()

    for admin in admins:
        button_text = f"{admin.full_name or 'Noma‘lum'} ({admin.telegram_id})"
        keyboard.button(text=button_text, callback_data=f"del_admin:{admin.telegram_id}")

    keyboard.adjust(1)
    await message.answer("🛑 O‘chirmoqchi bo‘lgan adminni tanlang:", reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data.startswith("del_admin:"))
async def delete_admin(callback: CallbackQuery):
    admin_id = int(callback.data.split(":")[1])
    admin = await BotAdmin.objects.filter(telegram_id=admin_id).afirst()

    if admin:
        await admin.adelete()
        await callback.message.answer(f"❌ {admin.full_name or 'Admin'} (ID: {admin.telegram_id}) o‘chirildi!")
        await callback.answer("Admin o‘chirildi!", show_alert=True)
    else:
        await callback.answer("❗ Bu admin topilmadi.", show_alert=True)