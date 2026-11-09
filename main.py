from datetime import datetime
import logging
import random
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "9072083795:AAFNIkjPB7ycGVH9XiiFP7j1aa59QyeAPck"

# --- ADMIN ID ---
# O'z Telegram ID raqamingizni shu yerga yozing (admin huquqi faqat sizda bo'ladi)
ADMIN_IDS = [
    1048256299
]  # <--- O'z Telegram ID raqamingizni shu yerga yozing!

# Asosiy baza (Dastlabki 13 ta so'z)
WORDS_DATA = [
    {
        "word": "Run",
        "translate": "Yugurmoq",
        "mnemonic": (
            "Kalit so'z: Randa\n\n"
            "Tasavvur qiling:\n"
            "Siz dadangiz bilan ish qilyapsiz va dadangiz ustaxonadan RANDAni olib kel dedi "
            "siz ustaxonaga borsangiz RANDAga jon kirib xona bo'ylab yugurib yuribdi ekan.\n\n"
            "Ran - yugurmoq\n"
            "Yugurmoq - ran"
        ),
    },
    {
        "word": "Walk",
        "translate": "Yurmoq",
        "mnemonic": (
            "Kalit so'z: Vokzal\n\n"
            "Tasavvur qiling:\n"
            "Siz chet davlatga sayohatga ketyapsiz ammo siz kechasi ketayotganingiz bois ko'chada taksi yo'q "
            "va siz vokzalga piyoda ketyapsiz çamadonlaringiz bilan.\n\n"
            "Vok - yurmoq\n"
            "Yurmoq - vok"
        ),
    },
    {
        "word": "Jump",
        "translate": "Sakramoq",
        "mnemonic": (
            "Kalit so'z: Jem\n\n"
            "Tasavvur qiling:\n"
            "Siz jem (murabbo) yaxshi ko'rasiz va ertalab turib qarasangiz issiq non bilan jem turibdi ekan "
            "va xursandligingizdan sakrab yubordingiz.\n\n"
            "Jamp - sakramoq\n"
            "Sakramoq - jump"
        ),
    },
    {
        "word": "Crawl",
        "translate": "Emaklamoq",
        "mnemonic": (
            "Kalit so'z: Qirol\n\n"
            "Tasavvur qiling:\n"
            "Siz tush ko'ryapsiz va tushingizda bir qirollikdasiz va u qirollikda hamma tik yurar "
            "ammo faqat qirol emaklab yurar ekan.\n\n"
            "Krol - emaklamoq\n"
            "Emaklamoq - krol"
        ),
    },
    {
        "word": "Climb",
        "translate": "Tirmaashmoq, chiqmoq",
        "mnemonic": (
            "Kalit so'z: Kley\n\n"
            "Tasavvur qiling:\n"
            "Siz o'rgimchak odamga taqlid qilib qo'lingizga kley surkab olib devorga yopishib "
            "xona shiftiga chiqmoqchisiz.\n\n"
            "Klamb - tirmaashmoq, chiqmoq\n"
            "Chiqmoq, tirmaashmoq - klamb"
        ),
    },
    {
        "word": "Push",
        "translate": "Itarmoq",
        "mnemonic": (
            "Kalit so'z: Puşka\n\n"
            "Tasavvur qiling:\n"
            "Siz yotoqxonangizga uhlagani kirdingiz ammo divangiz ustida puşka turib va siz uhlash uchun "
            "yotog'ingizdan rosa itardingiz.\n\n"
            "Push - itarmoq\n"
            "Itarmoq - push"
        ),
    },
    {
        "word": "Pull",
        "translate": "Tortmoq",
        "mnemonic": (
            "Kalit so'z: Pul 💸\n\n"
            "Tasavvur qiling:\n"
            "Siz do'stingizga qarz bergansiz va qaytarishga kelganda u gapni cho'zyapti, mavzuni boshqa mavzuga "
            "burib yuboryapti va siz oxir oqibat pulni uning qo'lidan tortib oldingiz.\n\n"
            "Pul - tortib olmoq\n"
            "Tortib olmoq - pul"
        ),
    },
    {
        "word": "Throw",
        "translate": "Otmoq, tashlamoq",
        "mnemonic": (
            "Kalit so'z: Surogi muddatidan o'tgan narsalar\n\n"
            "Tasavvur qiling:\n"
            "Siz korzinkadasiz va bir payt xodimlar kelib surogi o'tgan mahsulotlarni hamma joyga otib yuboryapti.\n\n"
            "Srov - otmoq\n"
            "Otmoq - srov"
        ),
    },
    {
        "word": "Catch",
        "translate": "Tutmoq, tutib olmoq",
        "mnemonic": (
            "Kalit so'z: Ketçub\n\n"
            "Tasavvur qiling:\n"
            "Siz kechki ovqatda o'tiribsiz va jiyangiz birdan sizga ketçubni otib yubordi "
            "siz bo'lsa epchillik qilib ketçubni tutib oldingiz.\n\n"
            "Kaç - tutib olmoq\n"
            "Tutib olmoq - kaç"
        ),
    },
    {
        "word": "Lift",
        "translate": "Ko'tarilmoq",
        "mnemonic": (
            "Kalit so'z: Lift so'zining o'zi\n\n"
            "Tasavvur qiling:\n"
            "Uyingizda lift bor va hattoki 2-qavatga ham liftda ko'tarilasiz.\n\n"
            "Lift - ko'tarilmoq\n"
            "Ko'tarilmoq - lift"
        ),
    },
    {
        "word": "Shake",
        "translate": "Qo'lni qismoq",
        "mnemonic": (
            "Kalit so'z: Sheyx\n\n"
            "Tasavvur qiling:\n"
            "Siz Dubayga bordingiz va aylanib yurganingizda Dubayning eng boy sheyxlaridan biri kelib "
            "siz bilan qo'l siqishib ko'rishdi.\n\n"
            "Sheyk - qo'l siqmoq\n"
            "Qo'l siqmoq - sheyk"
        ),
    },
    {
        "word": "Slide",
        "translate": "Sirpanmoq",
        "mnemonic": (
            "Kalit so'z: Sklad (ombor)\n\n"
            "Tasavvur qiling:\n"
            "Siz skladdan yuk olib chiqayotganingizda polga moy to'kilgani sababli sirpanib ketdingiz.\n\n"
            "Slayd - sirpanmoq\n"
            "Sirpanmoq - slayd"
        ),
    },
    {
        "word": "Bend",
        "translate": "Egilmoq",
        "mnemonic": (
            "Kalit so'z: Bentley avtomashinasi\n\n"
            "Tasavvur qiling:\n"
            "Siz do'stlaringiz bilan mahallada futbol o'ynayapsiz ammo birdan kimdir topni tepib yubordi "
            "va u to'g'ri Bentley mashinasi tagiga kirib ketdi va siz uni olish uchun egildingiz.\n\n"
            "Bend - egilmoq\n"
            "Egilmoq - bend"
        ),
    },
]

# Tasks (Vazifalar) va Memes ro'yxati
TASKS_DATA = [
    "Bugun o'rganilgan 13 ta so'zni 3 martadan ovoz chiqarib takrorlang! 🗣",
    "Listen & Find o'yinida kamida 50 ta coin yig'ing! 🎮",
]

MEMES_DATA = [
    "Ingliz tilini o'rganayotganda 1-kun: Men inglizchani yoraman! 🔥\n10-kun: I am table... 🪑😂",
    "Qachonki o'qituvchi 'bu juda oson mavzu' deganda: 🤡",
]

user_progress = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    admin_btn = (
        "\n\n👑 Siz adminsiz! /admin buyrug'i orqali panelga o'tishingiz mumkin."
        if user_id in ADMIN_IDS
        else ""
    )

    await update.message.reply_text(
        f"Salom! Mnemonika botiga xush kelibsiz.\n"
        "📖 Yangi so'z olish uchun /soz\n"
        "🎮 Coin yig'ish uchun /oyin\n"
        "📋 Vazifalar uchun /tasks\n"
        "🤪 Memelar uchun /memes larni bosing!{admin_btn}"
    )


# --- USER QISMI: SO'ZLAR ---
async def send_next_word(update_or_query, user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    if user_id not in user_progress or user_progress[user_id]["date"] != today:
        user_progress[user_id] = {
            "index": 0,
            "date": today,
            "count": 0,
            "coins": 0,
            "playing": False,
            "target_word": None,
        }

    data = user_progress[user_id]
    total_words = len(WORDS_DATA)

    if data["count"] >= total_words:
        text = f"Bugungi barcha ({total_words} ta) so'zlar tugadi! /oyin orqali coin yig'ishingiz mumkin! 🚀"
        if hasattr(update_or_query, "message") and update_or_query.message:
            await update_or_query.message.reply_text(text)
        else:
            await update_or_query.edit_message_text(text)
        return

    idx = data["index"] % total_words
    item = WORDS_DATA[idx]

    message = (
        f"📖 So'z ({data['count'] + 1}/{total_words}):\n"
        f"So'z: {item['word']}\n"
        f"Tarjimasi: {item['translate']}\n\n"
        f"{item['mnemonic']}"
    )

    keyboard = [[InlineKeyboardButton("Keyingi so'z ➡️", callback_data="next_word")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    data["index"] = (idx + 1) % total_words
    data["count"] += 1

    if hasattr(update_or_query, "message") and update_or_query.message:
        await update_or_query.message.reply_text(message, reply_markup=reply_markup)
    else:
        await update_or_query.edit_message_text(
            message, reply_markup=reply_markup
        )


async def cmd_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_next_word(update, update.effective_user.id)


# --- O'YIN QISMI ---
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress or user_progress[user_id]["count"] == 0:
        await update.message.reply_text(
            "Siz hali birorta ham so'z o'rganmadingiz! Avval /soz buyrug'i bilan so'zlarni oching."
        )
        return

    data = user_progress[user_id]
    data["playing"] = True
    available = WORDS_DATA[: min(data["count"], len(WORDS_DATA))]
    target = random.choice(available)
    data["target_word"] = target["word"].lower()

    await update.message.reply_text(
        "🎮 **Listen & Find O'yini**\n"
        f"Mana bu tarjimaga mos keluvchi inglizcha so'zni yozing:\n\n"
        f"🇺🇿 **Tarjimasi:** `{target['translate']}`\n"
        f"💰 Balansingiz: {data['coins']} coin"
    )


async def check_game_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress or not user_progress[user_id].get(
        "playing", False
    ):
        return

    data = user_progress[user_id]
    user_text = update.message.text.strip().lower()

    if user_text == data["target_word"]:
        data["coins"] += 10
        data["playing"] = False
        await update.message.reply_text(
            f"✅ To'g'ri! Barakalla!\n"
            f"🎉 Sizga **10 coin** berildi!\n"
            f"💰 Jami coinlar: {data['coins']} ta\n\n"
            "Yana o'ynash uchun /oyin ni bosing."
        )
    else:
        await update.message.reply_text(
            "❌ Xato! Qaytadan o'ylab, to'g'ri so'zni yozing:"
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "next_word":
        await send_next_word(query, query.from_user.id)


# --- TASKS & MEMES (User qismi) ---
async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not TASKS_DATA:
        await update.message.reply_text(
            "Hozircha vazifalar mavjud emas. Tez kunda qo'shiladi! 📋"
        )
        return
    text = "📋 **Kunlik Vazifalar:**\n\n"
    for i, t in enumerate(TASKS_DATA, 1):
        text += f"{i}. {t}\n"
    await update.message.reply_text(text)


async def show_memes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not MEMES_DATA:
        await update.message.reply_text(
            "Hozircha memelar mavjud emas! 🤪"
        )
        return
    meme = random.choice(MEMES_DATA)
    await update.message.reply_text(f"🤪 **Meme vaqti:**\n\n{meme}")


# ==========================================
# --- ADMIN PANEL ---
# ==========================================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(
            "Sizda bu buyruqni ishlatish uchun huquq yo'q! ❌"
        )
        return

    text = (
        "👑 **Admin Panelga Xush Kelibsiz!**\n\n"
        "Quyidagi buyruqlar orqali ma'lumotlarni boshqarishingiz mumkin:\n\n"
        "📖 **So'zlar uchun:**\n"
        "• `/addword So'z | Tarjima | Mnemonika` - Yangi so'z qo'shish\n"
        "• `/delword So'z` - So'zni o'chirish\n"
        "• `/listwords` - Barcha so'zlarni ko'rish\n\n"
        "📋 **Vazifalar (Tasks) uchun:**\n"
        "• `/addtask Matn` - Yangi vazifa qo'shish\n"
        "• `/deltask Nomer` - Vazifani o'chirish\n\n"
        "🤪 **Memelar uchun:**\n"
        "• `/addmeme Matn` - Yangi meme qo'shish\n"
        "• `/delmeme Nomer` - Memeni o'chirish"
    )
    await update.message.reply_text(text)


# Admin: So'z qo'shish (/addword Run | Yugurmoq | Kalit so'z...)
async def admin_add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    text = " ".join(context.args)
    if "|" not in text:
        await update.message.reply_text(
            "Xato format! Ishlatish:\n`/addword So'z | Tarjima | Mnemonika`",
            parse_mode="Markdown",
        )
        return

    parts = [p.strip() for p in text.split("|")]
    if len(parts) < 3:
        await update.message.reply_text(
            "Barcha qismlarini to'ldiring: So'z | Tarjima | Mnemonika"
        )
        return

    WORDS_DATA.append(
        {"word": parts[0], "translate": parts[1], "mnemonic": parts[2]}
    )
    await update.message.reply_text(
        f"✅ Muvaffaqiyatli qo'shildi!\nSo'z: {parts[0]}"
    )


# Admin: So'zni o'chirish (/delword Run)
async def admin_del_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not context.args:
        await update.message.reply_text(
            "O'chiriladigan so'zni kiriting: `/delword Run`", parse_mode="Markdown"
        )
        return
    word_to_del = context.args[0].lower()
    global WORDS_DATA
    initial_len = len(WORDS_DATA)
    WORDS_DATA = [w for w in WORDS_DATA if w["word"].lower() != word_to_del]

    if len(WORDS_DATA) < initial_len:
        await update.message.reply_text(
            f"🗑 '{word_to_del.capitalize}' bazadan o'chirildi!"
        )
    else:
        await update.message.reply_text("❌ Bunday so'z topilmadi!")


# Admin: So'zlar ro'yxati
async def admin_list_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    text = f"📚 **Bazada {len(WORDS_DATA)} ta so'z bor:**\n\n"
    for w in WORDS_DATA:
        text += f"- {w['word']} ({w['translate']})\n"
    await update.message.reply_text(text)


# Admin: Task qo'shish (/addtask Ingliz tilida kitob o'qing)
async def admin_add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    task_text = " ".join(context.args)
    if not task_text:
        await update.message.reply_text("Vazifa matnini kiriting!")
        return
    TASKS_DATA.append(task_text)
    await update.message.reply_text("✅ Yangi vazifa qo'shildi!")


# Admin: Task o'chirish (/deltask 1)
async def admin_del_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        idx = int(context.args[0]) - 1
        removed = TASKS_DATA.pop(idx)
        await update.message.reply_text(f"🗑 O'chirildi: {removed}")
    except:
        await update.message.reply_text(
            "Xato! To'g'ri nomerni kiriting (masalan: `/deltask 1`)",
            parse_mode="Markdown",
        )


# Admin: Meme qo'shish (/addmeme Hazil matni)
async def admin_add_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    meme_text = " ".join(context.args)
    if not meme_text:
        await update.message.reply_text("Meme matnini kiriting!")
        return
    MEMES_DATA.append(meme_text)
    await update.message.reply_text("✅ Yangi meme qo'shildi!")


# Admin: Meme o'chirish (/delmeme 1)
async def admin_del_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        idx = int(context.args[0]) - 1
        removed = MEMES_DATA.pop(idx)
        await update.message.reply_text(f"🗑 Meme o'chirildi: {removed}")
    except:
        await update.message.reply_text(
            "Xato! To'g'ri nomerni kiriting (masalan: `/delmeme 1`)",
            parse_mode="Markdown",
        )


def main():
  application = ApplicationBuilder().token(TOKEN).build()

  # User buyruqlari
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("words", cmd_word))
  application.add_handler(CommandHandler("sozlar", cmd_word))
  application.add_handler(CommandHandler("soz", cmd_word))
  application.add_handler(CommandHandler("oyin", start_game))
  application.add_handler(CommandHandler("game", start_game))
  application.add_handler(CommandHandler("tasks", show_tasks))
  application.add_handler(CommandHandler("memes", show_memes))

  # Admin buyruqlari
  application.add_handler(CommandHandler("admin", admin_panel))
  application.add_handler(CommandHandler("addword", admin_add_word))
  application.add_handler(CommandHandler("delword", admin_del_word))
  application.add_handler(CommandHandler("listwords", admin_list_words))
  application.add_handler(CommandHandler("addtask", admin_add_task))
  application.add_handler(CommandHandler("deltask", admin_del_task))
  application.add_handler(CommandHandler("addmeme", admin_add_meme))
  application.add_handler(CommandHandler("delmeme", admin_del_meme))

  # Xabar va tugmalar
  application.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, check_game_answer)
  )
  application.add_handler(CallbackQueryHandler(button_handler))

  print("Bot ishga tushmoqda...")
  # ESKI YAMOQ: application.run_polling(drop_pending_updates=True)
  # YANGI TO'G'RI QATOR (Shuni yozasiz):
  application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  main()
