import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

TOKEN = "8885745148:AAGltJ84eT153H6Z89DUcn5GZX5CxE2m74U"
ADMIN_ID = 6375699767

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

class OrderState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_callback = State()

# --- КЛАВИАТУРЫ ---

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👟 Посмотреть каталог")],
        [KeyboardButton(text="📦 Доставка и оплата"), KeyboardButton(text="💬 Отзывы")],
        [KeyboardButton(text="📞 Связаться с менеджером")]
    ],
    resize_keyboard=True
)

gender_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🙋‍♂️ Мужская обувь", callback_data="cat_male")],
    [InlineKeyboardButton(text="🙋‍♀️ Женская обувь", callback_data="cat_female")]
])

brands_male = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Nike Air Max", callback_data="brand_nike_m")],
    [InlineKeyboardButton(text="Adidas Forum", callback_data="brand_adidas_m1")],
    [InlineKeyboardButton(text="Adidas Samba", callback_data="brand_adidas_m2")],
    [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="to_main_menu")]
])

brands_female = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Nike Dunk Low", callback_data="brand_nike_w")],
    [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="to_main_menu")]
])

product_inline_keyboard_nike_m = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Оформить заказ", callback_data="buy_nike_m_1")],
    [InlineKeyboardButton(text="⬅️ Назад к брендам", callback_data="back_to_brands_m")]
])

product_inline_keyboard_adidas_m1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Оформить заказ", callback_data="buy_adidas_m1")],
    [InlineKeyboardButton(text="⬅️ Назад к брендам", callback_data="back_to_brands_m")]
])

product_inline_keyboard_adidas_m2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Оформить заказ", callback_data="buy_adidas_m2")],
    [InlineKeyboardButton(text="⬅️ Назад к брендам", callback_data="back_to_brands_m")]
])

product_inline_keyboard_nike_w = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Оформить заказ", callback_data="buy_nike_w_1")],
    [InlineKeyboardButton(text="⬅️ Назад к брендам", callback_data="back_to_brands_w")]
])

share_phone_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Отправить свой номер", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# --- ХЕНДЛЕРЫ ---

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Добро пожаловать в наш магазин оригинальной обуви.\n"
        "У нас ты найдешь эксклюзивные модели, которых нет в СНГ. Используй меню ниже 👇",
        reply_markup=main_menu
    )

@router.message(F.text == "📦 Доставка и оплата")
async def info_delivery(message: Message):
    await message.answer(
        "🚚 **Доставка:**\n• По Беларуси: Белпочта / Европочта (1-3 дня).\n• По СНГ: СДЭК.\n\n"
        "💳 **Оплата:**\n• При получении (наложенный платеж) или картой онлайн."
    )

@router.message(F.text == "💬 Отзывы")
async def info_reviews(message: Message):
    await message.answer("Почитать отзывы наших клиентов и посмотреть фотоотчеты можно в нашем Instagram: [ССЫЛКА]")

@router.message(F.text == "👟 Посмотреть каталог")
async def show_catalog(message: Message):
    await message.answer("Выберите интересующий вас раздел:", reply_markup=gender_menu)

# --- НАВИГАЦИЯ ---

@router.callback_query(F.data == "to_main_menu")
async def to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text("Выберите интересующий вас раздел:", reply_markup=gender_menu)
    await callback.answer()

@router.callback_query(F.data == "cat_male")
async def male_brands(callback: CallbackQuery):
    await callback.message.edit_text("Выберите модель мужской обуви:", reply_markup=brands_male)
    await callback.answer()

@router.callback_query(F.data == "cat_female")
async def female_brands(callback: CallbackQuery):
    await callback.message.edit_text("Выберите модель женской обуви:", reply_markup=brands_female)
    await callback.answer()

@router.callback_query(F.data == "back_to_brands_m")
async def back_to_brands_m(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выберите модель мужской обуви:", reply_markup=brands_male)
    await callback.answer()

@router.callback_query(F.data == "back_to_brands_w")
async def back_to_brands_w(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выберите модель женской обуви:", reply_markup=brands_female)
    await callback.answer()

# --- КАРТОЧКИ ТОВАРОВ ---

# 1. Мужские Nike
@router.callback_query(F.data == "brand_nike_m")
async def show_nike(callback: CallbackQuery):
    await callback.message.delete()
    
    # Сюда вставляем твой ID картинки вместо старой ссылки с сайта
    photo_id = "AgACAgIAAxkBAAMtamDZ3P0ZZ5AoNRm-uJkRhxmf8esAAiAaaxthowlL_ftfBYdjfHEBAAMCAAN4AAM9BA"
    
    await callback.message.answer_photo(
        photo=photo_id, # Бот возьмет картинку напрямую из базы ТГ по этому ID
        caption="🔥 **Nike Air Max Plus TN (Мужские)**\n\n📌 Оригинал из Европы.\n💰 Цена: 450 BYN\n👟 Размеры: 41, 42, 43, 44",
        reply_markup=product_inline_keyboard_nike_m
    )
    await callback.answer()


# 2. Мужские Adidas Forum
@router.callback_query(F.data == "brand_adidas_m1")
async def show_adidas1(callback: CallbackQuery):
    await callback.message.delete()
    photo_url = "https://unsplash.com" # МЕНЯТЬ ССЫЛКУ ТУТ
    await callback.message.answer_photo(
        photo=photo_url,
        caption="👟 **Adidas Forum Low (Мужские)**\n\n📌 Классика в оригинале.\n💰 Цена: 390 BYN\n👟 Размеры: 42, 43, 45",
        reply_markup=product_inline_keyboard_adidas_m1
    )
    await callback.answer()

# 3. Мужские Adidas Samba
@router.callback_query(F.data == "brand_adidas_m2")
async def show_adidas2(callback: CallbackQuery):
    await callback.message.delete()
    photo_url = "https://unsplash.com" # МЕНЯТЬ ССЫЛКУ ТУТ
    await callback.message.answer_photo(
        photo=photo_url,
        caption="⚽ **Adidas Samba OG (Мужские)**\n\n📌 Главный тренд сезона.\n💰 Цена: 410 BYN\n👟 Размеры: 41, 42, 43",
        reply_markup=product_inline_keyboard_adidas_m2
    )
    await callback.answer()

# 4. Женские Nike Dunk
@router.callback_query(F.data == "brand_nike_w")
async def show_nike_w(callback: CallbackQuery):
    await callback.message.delete()
    photo_url = "https://unsplash.com" # МЕНЯТЬ ССЫЛКУ ТУТ
    await callback.message.answer_photo(
        photo=photo_url,
        caption="✨ **Nike Dunk Low (Женские)**\n\n📌 Идеальная базовая расцветка.\n💰 Цена: 420 BYN\n👟 Размеры: 36, 37, 38, 39",
        reply_markup=product_inline_keyboard_nike_w
    )
    await callback.answer()

# --- СБОР ЗАКАЗА (FSM) ---

@router.callback_query(F.data.startswith("buy_"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    # Автоматически определяем какой товар заказан на основе callback_data
    product_map = {
        "buy_nike_m_1": "Nike Air Max Plus TN (450 BYN) [Мужские]",
        "buy_adidas_m1": "Adidas Forum Low (390 BYN) [Мужские]",
        "buy_adidas_m2": "Adidas Samba OG (410 BYN) [Мужские]",
        "buy_nike_w_1": "Nike Dunk Low (420 BYN) [Женские]"
    }
    
    selected_product = product_map.get(callback.data, "Неизвестный товар")
    await state.update_data(product_name=selected_product)
    
    await callback.message.answer(
        "Отличный выбор! Подтвердите ваш номер телефона, нажав на кнопку ниже, чтобы менеджер связался с вами для уточнения размера.",
        reply_markup=share_phone_menu
    )
    await state.set_state(OrderState.waiting_for_phone)
    await callback.answer()

@router.message(OrderState.waiting_for_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    user_data = await state.get_data()
    product = user_data.get("product_name")
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет юзернейма"

    await message.answer("Спасибо! Заказ принят. Менеджер свяжется с вами в ближайшее время.", reply_markup=main_menu)

    admin_text = (
        f"🚨 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👟 **Товар:** {product}\n"
        f"👤 **Покупатель:** {message.from_user.full_name} ({username})\n"
        f"📱 **Телефон:** {phone}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
    await state.clear()

# --- ОБРАТНЫЙ ЗВОНОК ---

@router.message(F.text == "📞 Связаться с менеджером")
async def callback_request(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку ниже, чтобы передать свой номер телефона менеджеру.", reply_markup=share_phone_menu)
    await state.set_state(OrderState.waiting_for_callback)

@router.message(OrderState.waiting_for_callback, F.contact)
async def process_callback(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет юзернейма"

    await message.answer("Заявка отправлена. Менеджер перезвонит вам.", reply_markup=main_menu)

    admin_text = (
        f"☎️ **ЗАПРОС НА ОБРАТНЫЙ ЗВОНОК**\n\n"
        f"👤 **Клиент:** {message.from_user.full_name} ({username})\n"
        f"📱 **Телефон:** {phone}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
    await state.clear()

# --- ЗАПУСК ---

@router.message(F.photo)
async def get_photo_id(message: Message):
    # Берем самое лучшее качество фото и выводим его ID в консоль
    photo_id = message.photo[-1].file_id
    print(f"\nID ТВОЕЙ КАРТИНКИ: {photo_id}\n")
    await message.answer("ID картинки выведен в консоль PyCharm / VS Code!")

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
