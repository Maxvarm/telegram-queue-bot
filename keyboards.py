from telegram import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_ADD_ID, MAIN_ADD_TOP_ID, MAIN_ADD_BOTTOM_ID, MAIN_DELETE_ID = map(chr, range(0, 4))
INIT_START_ID, INIT_CONFIG_ID = map(chr, range(4, 6))
CONFIG_BACK_ID, CONFIG_SORT_ID, CONFIG_REVERSE_ID, CONFIG_PRIORITY_ID = map(chr, range(6, 10))

MAIN_PRIORITIZED = InlineKeyboardMarkup([
    [InlineKeyboardButton("🐎 I want to be first 🐎", callback_data=MAIN_ADD_TOP_ID)],
    [InlineKeyboardButton("🦧 I don't really care 🦧", callback_data=MAIN_ADD_ID)],
    [InlineKeyboardButton("🦥 I want to be last 🦥", callback_data=MAIN_ADD_BOTTOM_ID)],
    [InlineKeyboardButton("❌ Delete me ❌", callback_data=MAIN_DELETE_ID)]
    ])

MAIN = InlineKeyboardMarkup([
    [InlineKeyboardButton("✅ Add me ✅", callback_data=MAIN_ADD_ID)],
    [InlineKeyboardButton("❌ Delete me ❌", callback_data=MAIN_DELETE_ID)]
    ])

INIT = InlineKeyboardMarkup([
    [InlineKeyboardButton("💃 Start 🕺", callback_data=INIT_START_ID)],
    [InlineKeyboardButton("⚙️ Configure ⚙️", callback_data=INIT_CONFIG_ID)]
    ])

CONFIG = InlineKeyboardMarkup([
    [InlineKeyboardButton("📈 Sort 📉", callback_data=CONFIG_SORT_ID)],
    [
        InlineKeyboardButton("♻️ Reverse ♻️", callback_data=CONFIG_REVERSE_ID),
        InlineKeyboardButton("🥇 Priority 🥉", callback_data=CONFIG_PRIORITY_ID)
        ],
    [InlineKeyboardButton("⏪⏪", callback_data=CONFIG_BACK_ID)],
    ])