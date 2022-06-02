from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button_contact = KeyboardButton('☎️ Контакты ☎️')
button_inforamation = KeyboardButton('🔎 О компании 🔍')
button_catalog = KeyboardButton('🗂 Каталог 🗂')
keyboard_client.row(button_contact, button_inforamation).add(button_catalog)

keyboard_client_catalog = InlineKeyboardMarkup(row_width=1)
inline_button_chemical = InlineKeyboardButton(text='🧪 Агрохимикаты', callback_data='Client catalog chemical')
inline_button_devices = InlineKeyboardButton(text='📟 Агроприборы', callback_data='Client catalog devices')
inline_button_fertilizers = InlineKeyboardButton(text='🪵 Удобрения', callback_data='Client catalog fertilizers')
inline_button_seeds = InlineKeyboardButton(text='🌱 Семена и растения', callback_data='Client catalog seeds')
keyboard_client_catalog.add(inline_button_chemical, inline_button_devices, inline_button_fertilizers, inline_button_seeds)


inl_clien_button_description = {}
inl_clien_button_basket = {"-": {}, "main": {}, "+": {}}
inl_client_button_send_basket = {}

inl_clien_button_conf = {}
inl_clien_button_cancel = {}

# Work "Desciption" button in item-message
async def menu_start_state_init(callback, item, id):
    global inl_clien_button_description, inl_clien_button_basket
    inline_client_keyboard = InlineKeyboardMarkup()
    inl_clien_button_description[id] = InlineKeyboardButton(text='Описание', callback_data=f'description {item[2]}')
    inl_clien_button_basket["main"][id] = InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add in basket {callback.data.replace("Client catalog ", "")} {item[1]}')
    inline_client_keyboard.add(inl_clien_button_description[id]).add(inl_clien_button_basket["main"][id])
    return inline_client_keyboard

async def menu_state_with_back(callback):
    global inl_clien_button_description, inl_clien_button_basket, inl_client_button_send_basket
    inline_client_keyboard = InlineKeyboardMarkup()
    inl_clien_button_description[callback.message.message_id] = InlineKeyboardButton(text='↩️ Назад', callback_data=f'reverse {callback.message.caption}')
    inline_client_keyboard.add(inl_clien_button_description[callback.message.message_id])
    if inl_clien_button_basket['-'].get(callback.message.message_id) is None:
        inline_client_keyboard.add(inl_clien_button_basket["main"][callback.message.message_id])
    else:
        if inl_clien_button_conf.get(callback.message.message_id) is None:
            inline_client_keyboard.row(inl_clien_button_basket["-"][callback.message.message_id],
                inl_clien_button_basket["main"][callback.message.message_id],
                inl_clien_button_basket["+"][callback.message.message_id]).\
            add(inl_client_button_send_basket[callback.message.message_id])
        else:
            inline_client_keyboard.add(inl_clien_button_conf[callback.message.message_id]).add(inl_clien_button_cancel[callback.message.message_id])
    return inline_client_keyboard

async def menu_start_state_with_description(callback):
    global inl_clien_button_description, inl_clien_button_basket, inl_client_button_send_basket
    inline_client_keyboard = InlineKeyboardMarkup()
    inl_clien_button_description[callback.message.message_id] = InlineKeyboardButton(text='Описание', callback_data=f'description {callback.message.caption.replace("Описание: ", "")}')
    inline_client_keyboard.add(inl_clien_button_description[callback.message.message_id])
    if inl_clien_button_basket['-'].get(callback.message.message_id) is None:
        inline_client_keyboard.add(inl_clien_button_basket["main"][callback.message.message_id])
    else:
        if inl_clien_button_conf.get(callback.message.message_id) is None:
            inline_client_keyboard.row(inl_clien_button_basket["-"][callback.message.message_id],
                inl_clien_button_basket["main"][callback.message.message_id],
                inl_clien_button_basket["+"][callback.message.message_id]).\
            add(inl_client_button_send_basket[callback.message.message_id])
        else:
            inline_client_keyboard.add(inl_clien_button_conf[callback.message.message_id]).add(inl_clien_button_cancel[callback.message.message_id])
    return inline_client_keyboard

# Work "Basket" button in item-message
async def change_basket_state(callback, count):
    global inl_clien_button_description, inl_clien_button_basket, inl_client_button_send_basket
    inline_client_keyboard = InlineKeyboardMarkup()
    split_data = callback.data.split()
    inl_client_button_send_basket[callback.message.message_id] = InlineKeyboardButton(text="Заказать", callback_data=f'send basket {split_data[3]} {split_data[4]}')
    inl_clien_button_basket['-'][callback.message.message_id] = InlineKeyboardButton(text="➖", callback_data=f'remove from basket {split_data[3]} {split_data[4]}')
    inl_clien_button_basket['+'][callback.message.message_id] = InlineKeyboardButton(text="➕", callback_data=f'add in basket {split_data[3]} {split_data[4]}')
    inl_clien_button_basket['main'][callback.message.message_id] = InlineKeyboardButton(text=f"{count}", callback_data=f'count')
    inline_client_keyboard.add(inl_clien_button_description[callback.message.message_id]).\
        row(inl_clien_button_basket["-"][callback.message.message_id],
        inl_clien_button_basket["main"][callback.message.message_id],
        inl_clien_button_basket["+"][callback.message.message_id]).\
        add(inl_client_button_send_basket[callback.message.message_id])
    return inline_client_keyboard

async def confirmation_state(callback):
    global inl_clien_button_description, inl_clien_button_conf, inl_clien_button_cancel
    inline_client_keyboard = InlineKeyboardMarkup()
    split_data = callback.data.split()
    inl_clien_button_conf[callback.message.message_id] = InlineKeyboardButton(text="Подтвердить заказ", callback_data=f'confirm  {split_data[2]} {split_data[3]}')
    inl_clien_button_cancel[callback.message.message_id] = InlineKeyboardButton(text="Отменить заказ", callback_data='cancel')
    inline_client_keyboard.add(inl_clien_button_description[callback.message.message_id]).\
        add(inl_clien_button_conf[callback.message.message_id]).\
        add(inl_clien_button_cancel[callback.message.message_id])
    return inline_client_keyboard

async def cancel_state(callback):
    global inl_clien_button_conf, inl_clien_button_cancel
    inline_client_keyboard = InlineKeyboardMarkup()
    inl_clien_button_conf[callback.message.message_id] = None
    inl_clien_button_cancel[callback.message.message_id] = None
    inline_client_keyboard.add(inl_clien_button_description[callback.message.message_id]).\
        row(inl_clien_button_basket["-"][callback.message.message_id],
        inl_clien_button_basket["main"][callback.message.message_id],
        inl_clien_button_basket["+"][callback.message.message_id]).\
            add(inl_client_button_send_basket[callback.message.message_id])
    return inline_client_keyboard

async def confirm_state(callback):
    global inl_clien_button_conf, inl_clien_button_cancel
    inline_client_keyboard = InlineKeyboardMarkup()
    inl_clien_button_conf[callback.message.message_id] = None
    inl_clien_button_cancel[callback.message.message_id] = None
    inl_clien_button_basket["main"][callback.message.message_id] = InlineKeyboardButton(text=f"{1}", callback_data=f'1')
    inline_client_keyboard.add(inl_clien_button_description[callback.message.message_id]).\
        row(inl_clien_button_basket["-"][callback.message.message_id],
        inl_clien_button_basket["main"][callback.message.message_id],
        inl_clien_button_basket["+"][callback.message.message_id]).\
            add(inl_client_button_send_basket[callback.message.message_id])
    return inline_client_keyboard
