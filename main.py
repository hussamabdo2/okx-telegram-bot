import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN غير موجود. أضفه في Railway → Variables"
    )


# =========================================================
# بيانات عالم الأطفال
# =========================================================

CATEGORIES = {

    "animals": (
        "🐾 الحيوانات",
        [
            ("🐶", "الكلب"),
            ("🐱", "القطة"),
            ("🦁", "الأسد"),
            ("🐰", "الأرنب"),
            ("🐘", "الفيل"),
            ("🦊", "الثعلب"),
            ("🐼", "الباندا"),
            ("🐯", "النمر"),
            ("🐸", "الضفدع"),
            ("🐵", "القرد"),
            ("🐢", "السلحفاة"),
            ("🦋", "الفراشة"),
            ("🐝", "النحلة"),
            ("🦒", "الزرافة"),
            ("🐴", "الحصان"),
        ],
    ),

    "trees": (
        "🌳 الأشجار والطبيعة",
        [
            ("🌳", "الشجرة"),
            ("🌲", "شجرة الصنوبر"),
            ("🌴", "النخلة"),
            ("🌵", "الصبار"),
            ("🌻", "زهرة عباد الشمس"),
            ("🌷", "زهرة"),
            ("🌹", "وردة"),
            ("🌱", "النبتة"),
            ("🍀", "البرسيم"),
            ("🌈", "قوس قزح"),
            ("☀️", "الشمس"),
            ("☁️", "السحابة"),
            ("🌙", "القمر"),
            ("⭐", "النجمة"),
        ],
    ),

    "food": (
        "🍎 الفواكه والطعام",
        [
            ("🍎", "التفاحة"),
            ("🍐", "الكمثرى"),
            ("🍊", "البرتقالة"),
            ("🍋", "الليمونة"),
            ("🍌", "الموزة"),
            ("🍉", "البطيخ"),
            ("🍇", "العنب"),
            ("🍓", "الفراولة"),
            ("🍒", "الكرز"),
            ("🍑", "الخوخ"),
            ("🥭", "المانجو"),
            ("🍍", "الأناناس"),
            ("🥝", "الكيوي"),
            ("🥕", "الجزر"),
            ("🌽", "الذرة"),
            ("🥦", "البروكلي"),
            ("🍅", "الطماطم"),
            ("🍕", "البيتزا"),
            ("🍰", "الكعكة"),
            ("🍦", "المثلجات"),
        ],
    ),

    "vehicles": (
        "🚗 المركبات",
        [
            ("🚗", "السيارة"),
            ("🚕", "سيارة الأجرة"),
            ("🚌", "الحافلة"),
            ("🚓", "سيارة الشرطة"),
            ("🚑", "سيارة الإسعاف"),
            ("🚒", "سيارة الإطفاء"),
            ("🚜", "الجرار"),
            ("🚲", "الدراجة"),
            ("🛴", "السكوتر"),
            ("✈️", "الطائرة"),
            ("🚁", "المروحية"),
            ("🚀", "الصاروخ"),
            ("🚢", "السفينة"),
            ("🚂", "القطار"),
        ],
    ),

    "school": (
        "📚 الأدوات والمدرسة",
        [
            ("✏️", "قلم الرصاص"),
            ("🖊️", "القلم"),
            ("📕", "الكتاب"),
            ("📗", "الدفتر"),
            ("📚", "الكتب"),
            ("📏", "المسطرة"),
            ("✂️", "المقص"),
            ("🎒", "الحقيبة"),
            ("🖍️", "الألوان"),
            ("🖌️", "الفرشاة"),
            ("🧮", "العداد"),
            ("🔍", "العدسة"),
            ("📐", "المسطرة الهندسية"),
        ],
    ),

    "toys": (
        "🧸 الألعاب",
        [
            ("🧸", "الدبدوب"),
            ("⚽", "كرة القدم"),
            ("🏀", "كرة السلة"),
            ("🎾", "كرة التنس"),
            ("🪁", "الطائرة الورقية"),
            ("🎈", "البالون"),
            ("🎁", "الهدية"),
            ("🎲", "النرد"),
            ("🪀", "اليويو"),
            ("🧩", "الأحجية"),
        ],
    ),

    "sea": (
        "🌊 عالم البحر",
        [
            ("🐟", "السمكة"),
            ("🐠", "السمكة الملونة"),
            ("🦈", "القرش"),
            ("🐬", "الدولفين"),
            ("🐳", "الحوت"),
            ("🐙", "الأخطبوط"),
            ("🦀", "السلطعون"),
            ("🦐", "الروبيان"),
            ("🐚", "الصدفة"),
        ],
    ),

    "space": (
        "🚀 عالم الفضاء",
        [
            ("🚀", "الصاروخ"),
            ("👨‍🚀", "رائد الفضاء"),
            ("🌍", "الأرض"),
            ("🌕", "القمر"),
            ("⭐", "النجمة"),
            ("🌟", "النجمة اللامعة"),
            ("☄️", "المذنب"),
            ("🪐", "الكوكب"),
        ],
    ),
}


LETTERS = [
    ("أ", "أسد 🦁"),
    ("ب", "بطة 🦆"),
    ("ت", "تفاحة 🍎"),
    ("ث", "ثعلب 🦊"),
    ("ج", "جمل 🐪"),
    ("ح", "حصان 🐴"),
    ("خ", "خروف 🐑"),
    ("د", "دجاجة 🐔"),
    ("ذ", "ذئب 🐺"),
    ("ر", "رمان 🍎"),
    ("ز", "زرافة 🦒"),
    ("س", "سمكة 🐟"),
    ("ش", "شجرة 🌳"),
    ("ص", "صقر 🦅"),
    ("ض", "ضفدع 🐸"),
    ("ط", "طائرة ✈️"),
    ("ظ", "ظرف ✉️"),
    ("ع", "عصفور 🐦"),
    ("غ", "غزال 🦌"),
    ("ف", "فيل 🐘"),
    ("ق", "قمر 🌙"),
    ("ك", "كتاب 📖"),
    ("ل", "ليمون 🍋"),
    ("م", "موز 🍌"),
    ("ن", "نحلة 🐝"),
    ("هـ", "هلال 🌙"),
    ("و", "وردة 🌹"),
    ("ي", "يد ✋"),
]


NUMBERS = [
    ("٠", "صفر"),
    ("١", "واحد"),
    ("٢", "اثنان"),
    ("٣", "ثلاثة"),
    ("٤", "أربعة"),
    ("٥", "خمسة"),
    ("٦", "ستة"),
    ("٧", "سبعة"),
    ("٨", "ثمانية"),
    ("٩", "تسعة"),
    ("١٠", "عشرة"),
]


# =========================================================
# نظام النجوم
# =========================================================

scores = {}


def get_score(user_id):
    return scores.get(user_id, 0)


def add_score(user_id, amount):
    scores[user_id] = get_score(user_id) + amount


# =========================================================
# القائمة الرئيسية
# =========================================================

def main_keyboard():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🎨 الرسم والتلوين",
                callback_data="drawing"
            )
        ],

        [
            InlineKeyboardButton(
                "🌳 الطبيعة",
                callback_data="cat_trees"
            ),
            InlineKeyboardButton(
                "🐾 الحيوانات",
                callback_data="cat_animals"
            ),
        ],

        [
            InlineKeyboardButton(
                "🍎 الفواكه والطعام",
                callback_data="cat_food"
            ),
            InlineKeyboardButton(
                "🚗 المركبات",
                callback_data="cat_vehicles"
            ),
        ],

        [
            InlineKeyboardButton(
                "📚 الأدوات",
                callback_data="cat_school"
            ),
            InlineKeyboardButton(
                "🧸 الألعاب",
                callback_data="cat_toys"
            ),
        ],

        [
            InlineKeyboardButton(
                "🌊 عالم البحر",
                callback_data="cat_sea"
            ),
            InlineKeyboardButton(
                "🚀 الفضاء",
                callback_data="cat_space"
            ),
        ],

        [
            InlineKeyboardButton(
                "🔤 الحروف",
                callback_data="letters"
            ),
            InlineKeyboardButton(
                "🔢 الأرقام",
                callback_data="numbers"
            ),
        ],

        [
            InlineKeyboardButton(
                "🧩 أكمل الصورة",
                callback_data="missing"
            ),
            InlineKeyboardButton(
                "🔀 إعادة تركيب الصورة",
                callback_data="puzzle"
            ),
        ],

        [
            InlineKeyboardButton(
                "⭐ نجومي",
                callback_data="score"
            )
        ],

    ])


# =========================================================
# /start
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = (
        "🌈✨ أهلاً بكم في ✨🌈\n\n"
        "🎨 **عالم أطفال ليليان وريناد ومحمد**\n\n"
        "👧 ليليان\n"
        "👧 ريناد\n"
        "👦 محمد\n\n"
        "🎨 نرسم ونلوّن\n"
        "🐾 نتعرف على الحيوانات\n"
        "🌳 نستكشف الطبيعة\n"
        "🔤 نتعلم الحروف\n"
        "🔢 نتعلم الأرقام\n"
        "🧩 نحل الألعاب\n"
        "🔀 نعيد تركيب الصور\n\n"
        "⭐ اجمع النجوم وكن بطلاً!\n\n"
        "اختاروا نشاطاً:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )


# =========================================================
# عرض التصنيف
# =========================================================

async def show_category(query, category):

    title, items = CATEGORIES[category]

    buttons = []

    row = []

    for index, (emoji, name) in enumerate(items):

        row.append(
            InlineKeyboardButton(
                f"{emoji} {name}",
                callback_data=f"item_{category}_{index}"
            )
        )

        if len(row) == 2:

            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            "🏠 الرئيسية",
            callback_data="home"
        )
    ])

    await query.edit_message_text(
        f"{title}\n\n"
        "اختار صورة لتبدأ النشاط 🎨",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# =========================================================
# عرض الصورة/العنصر داخل البوت
# =========================================================

async def show_item(query, category, index):

    emoji, name = CATEGORIES[category][1][index]

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🎨 تلوين",
                callback_data=f"color_{category}_{index}"
            )
        ],

        [
            InlineKeyboardButton(
                "⭐ أنجزت",
                callback_data=f"done_{category}_{index}"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 رجوع",
                callback_data=f"cat_{category}"
            )
        ],

    ])

    await query.edit_message_text(

        f"🎨 **صفحة التلوين**\n\n"
        f"{emoji}\n\n"
        f"🖼️ الصورة: **{name}**\n\n"
        "تخيل أنك تلوّن هذه الصورة بأجمل الألوان 🌈\n\n"
        "اختر ما تريد:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# =========================================================
# التلوين
# =========================================================

async def coloring(query, category, index):

    emoji, name = CATEGORIES[category][1][index]

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🔴 أحمر",
                callback_data="color_red"
            ),
            InlineKeyboardButton(
                "🔵 أزرق",
                callback_data="color_blue"
            ),
        ],

        [
            InlineKeyboardButton(
                "🟢 أخضر",
                callback_data="color_green"
            ),
            InlineKeyboardButton(
                "🟡 أصفر",
                callback_data="color_yellow"
            ),
        ],

        [
            InlineKeyboardButton(
                "🟣 بنفسجي",
                callback_data="color_purple"
            ),
            InlineKeyboardButton(
                "🟠 برتقالي",
                callback_data="color_orange"
            ),
        ],

        [
            InlineKeyboardButton(
                "🌈 اخترت ألواني",
                callback_data=f"done_{category}_{index}"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 رجوع",
                callback_data=f"item_{category}_{index}"
            )
        ],

    ])

    await query.edit_message_text(

        f"🎨 تلوين {name}\n\n"
        f"{emoji}\n\n"
        "اختر اللون الذي تحبه 🌈\n\n"
        "🔴 🔵 🟢 🟡 🟣 🟠",

        reply_markup=keyboard
    )


# =========================================================
# الحروف
# =========================================================

async def letters_menu(query):

    buttons = []

    row = []

    for index, (letter, word) in enumerate(LETTERS):

        row.append(
            InlineKeyboardButton(
                letter,
                callback_data=f"letter_{index}"
            )
        )

        if len(row) == 5:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            "🏠 الرئيسية",
            callback_data="home"
        )
    ])

    await query.edit_message_text(
        "🔤 **الحروف العربية**\n\n"
        "اختر حرفاً للتعلم والتلوين:",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )


async def show_letter(query, index):

    letter, word = LETTERS[index]

    await query.edit_message_text(

        f"🔤 **حرف اليوم**\n\n"
        f"🔠 {letter}\n\n"
        f"مثال: {word}\n\n"
        "🎨 لوّن الحرف في خيالك بأجمل لون! 🌈",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "⭐ تعلمت الحرف",
                    callback_data=f"letter_done_{index}"
                )
            ],

            [
                InlineKeyboardButton(
                    "➡️ حرف آخر",
                    callback_data="letters"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 الرئيسية",
                    callback_data="home"
                )
            ]

        ]),

        parse_mode="Markdown"
    )


# =========================================================
# الأرقام
# =========================================================

async def numbers_menu(query):

    buttons = []

    row = []

    for index, (number, name) in enumerate(NUMBERS):

        row.append(
            InlineKeyboardButton(
                number,
                callback_data=f"number_{index}"
            )
        )

        if len(row) == 5:

            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            "🏠 الرئيسية",
            callback_data="home"
        )
    ])

    await query.edit_message_text(
        "🔢 **الأرقام**\n\n"
        "اختر رقماً للتعلم:",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )


async def show_number(query, index):

    number, name = NUMBERS[index]

    await query.edit_message_text(

        f"🔢 **الرقم**\n\n"
        f"🔵 {number}\n\n"
        f"اسمه: {name}\n\n"
        "🎨 لوّن الرقم بأجمل لون! 🌈",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "⭐ تعلمت الرقم",
                    callback_data=f"number_done_{index}"
                )
            ],

            [
                InlineKeyboardButton(
                    "➡️ رقم آخر",
                    callback_data="numbers"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 الرئيسية",
                    callback_data="home"
                )
            ]

        ]),

        parse_mode="Markdown"
    )


# =========================================================
# أكمل الصورة
# =========================================================

MISSING = [

    (
        "🐶 + ؟",
        [
            ("🐾", True),
            ("🚀", False),
            ("🍎", False),
        ],
        "ما الشيء المناسب للكلب؟"
    ),

    (
        "🌳 + ؟",
        [
            ("🌱", True),
            ("🚗", False),
            ("🐟", False),
        ],
        "ما الذي يناسب الشجرة؟"
    ),

    (
        "🐟 + ؟",
        [
            ("🌊", True),
            ("🚀", False),
            ("🏠", False),
        ],
        "أين تعيش السمكة؟"
    ),

    (
        "☀️ + ؟",
        [
            ("🌈", True),
            ("🐠", False),
            ("🚗", False),
        ],
        "ما الشيء الجميل الذي قد يظهر مع الشمس؟"
    ),

]


async def missing_menu(query):

    question, answers, title = random.choice(MISSING)

    buttons = []

    for emoji, correct in answers:

        value = "yes" if correct else "no"

        buttons.append([
            InlineKeyboardButton(
                emoji,
                callback_data=f"missing_answer_{value}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "🔄 سؤال آخر",
            callback_data="missing"
        )
    ])

    buttons.append([
        InlineKeyboardButton(
            "🏠 الرئيسية",
            callback_data="home"
        )
    ])

    await query.edit_message_text(

        f"🧩 **أكمل الصورة**\n\n"
        f"{question}\n\n"
        f"{title}\n\n"
        "اختر الإجابة الصحيحة:",

        reply_markup=InlineKeyboardMarkup(buttons),

        parse_mode="Markdown"
    )


# =========================================================
# إعادة تركيب الصورة
# =========================================================

async def puzzle_menu(query):

    pieces = [
        "🌳",
        "☀️",
        "🏠",
        "🌸",
        "🐦",
        "🦋",
    ]

    random.shuffle(pieces)

    text = (
        "🔀 **إعادة تركيب الصورة**\n\n"
        "رتب هذه العناصر في خيالك لتكوين صورة جميلة:\n\n"
        + "   ".join(pieces)
        + "\n\n"
        "هل رتبتها؟"
    )

    await query.edit_message_text(

        text,

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "⭐ أكملت الصورة",
                    callback_data="puzzle_done"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔄 صورة أخرى",
                    callback_data="puzzle"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 الرئيسية",
                    callback_data="home"
                )
            ]

        ]),

        parse_mode="Markdown"
    )


# =========================================================
# الرسم
# =========================================================

async def drawing_menu(query):

    await query.edit_message_text(

        "🎨 **الرسم والتلوين**\n\n"

        "اختر ماذا تريد أن ترسم:\n\n"

        "🌳 شجرة\n"
        "🐶 حيوان\n"
        "🏠 بيت\n"
        "☀️ شمس\n"
        "🌈 قوس قزح\n"
        "🚗 سيارة\n"
        "🚀 صاروخ\n\n"

        "في نسخة Telegram العادية نستخدم "
        "الصور والأزرار داخل البوت بالكامل.",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🌳 شجرة",
                    callback_data="draw_tree"
                ),
                InlineKeyboardButton(
                    "🐶 حيوان",
                    callback_data="draw_animal"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 بيت",
                    callback_data="draw_house"
                ),
                InlineKeyboardButton(
                    "🚗 سيارة",
                    callback_data="draw_car"
                )
            ],

            [
                InlineKeyboardButton(
                    "🚀 صاروخ",
                    callback_data="draw_rocket"
                ),
                InlineKeyboardButton(
                    "🌈 قوس قزح",
                    callback_data="draw_rainbow"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 الرئيسية",
                    callback_data="home"
                )
            ]

        ]),

        parse_mode="Markdown"
    )


# =========================================================
# النجوم
# =========================================================

async def score_menu(query):

    user_id = query.from_user.id

    score = get_score(user_id)

    if score < 10:
        level = "🌱 مبتدئ صغير"
    elif score < 30:
        level = "🌟 فنان صغير"
    elif score < 60:
        level = "🏆 بطل"
    else:
        level = "👑 بطل عالم الأطفال"

    await query.edit_message_text(

        f"⭐ **نجومك**\n\n"
        f"⭐ عدد النجوم: **{score}**\n\n"
        f"🏅 المستوى:\n{level}\n\n"
        "استمر في اللعب والتعلم لتحصل على نجوم أكثر! 🌈",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🏠 الرئيسية",
                    callback_data="home"
                )
            ]

        ]),

        parse_mode="Markdown"
    )


# =========================================================
# معالجة الأزرار
# =========================================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id

    # الرئيسية
    if data == "home":

        await query.edit_message_text(
            "🌈✨ **عالم أطفال ليليان وريناد ومحمد** ✨🌈\n\n"
            "اختاروا نشاطاً:",
            reply_markup=main_keyboard(),
            parse_mode="Markdown"
        )

        return

    # التصنيفات
    if data.startswith("cat_"):

        category = data[4:]

        if category in CATEGORIES:

            await show_category(
                query,
                category
            )

        return

    # العناصر
    if data.startswith("item_"):

        parts = data.split("_")

        category = parts[1]
        index = int(parts[2])

        await show_item(
            query,
            category,
            index
        )

        return

    # التلوين
    if data.startswith("color_"):

        parts = data.split("_")

        if len(parts) >= 3:

            category = parts[1]
            index = int(parts[2])

            await coloring(
                query,
                category,
                index
            )

        return

    # إنهاء التلوين
    if data.startswith("done_"):

        add_score(
            user_id,
            5
        )

        await query.answer(
            "🎉 أحسنت! ⭐ +5",
            show_alert=True
        )

        await query.edit_message_text(

            "🎉 **أحسنت يا بطل!**\n\n"
            "⭐ حصلت على 5 نجوم.\n\n"
            "استمر في اللعب والتعلم! 🌈",

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "🏠 الرئيسية",
                        callback_data="home"
                    )
                ]

            ]),

            parse_mode="Markdown"
        )

        return

    # الحروف
    if data == "letters":

        await letters_menu(query)

        return

    if data.startswith("letter_"):

        if data.startswith("letter_done_"):

            add_score(
                user_id,
                5
            )

            await query.answer(
                "⭐ أحسنت! +5",
                show_alert=True
            )

            await letters_menu(query)

            return

        index = int(
            data.split("_")[1]
        )

        await show_letter(
            query,
            index
        )

        return

    # الأرقام
    if data == "numbers":

        await numbers_menu(query)

        return

    if data.startswith("number_"):

        if data.startswith("number_done_"):

            add_score(
                user_id,
                5
            )

            await query.answer(
                "⭐ أحسنت! +5",
                show_alert=True
            )

            await numbers_menu(query)

            return

        index = int(
            data.split("_")[1]
        )

        await show_number(
            query,
            index
        )

        return

    # أكمل الصورة
    if data == "missing":

        await missing_menu(query)

        return

    if data == "missing_answer_yes":

        add_score(
            user_id,
            10
        )

        await query.answer(
            "🎉 إجابة صحيحة! ⭐ +10",
            show_alert=True
        )

        await missing_menu(query)

        return

    if data == "missing_answer_no":

        await query.answer(
            "😊 حاول مرة أخرى",
            show_alert=True
        )

        return

    # إعادة التركيب
    if data == "puzzle":

        await puzzle_menu(query)

        return

    if data == "puzzle_done":

        add_score(
            user_id,
            15
        )

        await query.answer(
            "🏆 ممتاز! ⭐ +15",
            show_alert=True
        )

        await puzzle_menu(query)

        return

    # الرسم
    if data == "drawing":

        await drawing_menu(query)

        return

    if data.startswith("draw_"):

        names = {
            "draw_tree": "🌳 شجرة",
            "draw_animal": "🐶 حيوان",
            "draw_house": "🏠 بيت",
            "draw_car": "🚗 سيارة",
            "draw_rocket": "🚀 صاروخ",
            "draw_rainbow": "🌈 قوس قزح",
        }

        name = names.get(
            data,
            "🎨 صورة"
        )

        add_score(
            user_id,
            3
        )

        await query.edit_message_text(

            f"🎨 **صفحة التلوين**\n\n"
            f"{name}\n\n"
            "🖍️ أحسنت! اختر لونك المفضل:\n\n"
            "🔴 أحمر\n"
            "🔵 أزرق\n"
            "🟢 أخضر\n"
            "🟡 أصفر\n"
            "🟣 بنفسجي\n"
            "🟠 برتقالي\n\n"
            "⭐ حصلت على 3 نجوم!",

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "🔴",
                        callback_data="paint_red"
                    ),
                    InlineKeyboardButton(
                        "🔵",
                        callback_data="paint_blue"
                    ),
                    InlineKeyboardButton(
                        "🟢",
                        callback_data="paint_green"
                    ),
                ],

                [
                    InlineKeyboardButton(
                        "🟡",
                        callback_data="paint_yellow"
                    ),
                    InlineKeyboardButton(
                        "🟣",
                        callback_data="paint_purple"
                    ),
                    InlineKeyboardButton(
                        "🟠",
                        callback_data="paint_orange"
                    ),
                ],

                [
                    InlineKeyboardButton(
                        "🏠 الرئيسية",
                        callback_data="home"
                    )
                ]

            ]),

            parse_mode="Markdown"
        )

        return

    # الألوان
    if data.startswith("paint_"):

        await query.answer(
            "🎨 لون جميل!",
            show_alert=True
        )

        return

    # النجوم
    if data == "score":

        await score_menu(query)

        return


# =========================================================
# تشغيل البوت
# =========================================================

def main():

    print(
        "🌈 عالم أطفال ليليان وريناد ومحمد يعمل الآن..."
    )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            buttons
        )
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
