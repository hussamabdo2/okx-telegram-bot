import os
import random
import base64
from io import BytesIO

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ============================================================
# إعداد البوت
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN غير موجود في Railway Variables")


# ============================================================
# الصور مدمجة داخل هذا الملف نفسه
#
# محمد = الصورة الأولى
# ليليان = الصورة الثانية
# ريناد = الصورة الثالثة
#
# لا توجد روابط خارجية
# ============================================================

MOHAMMED_IMAGE = """
/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsL
DBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL
/2wBDAQkJCQwLDBgNDRgyIRo3MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj
IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAKSAaMDASIAAhEBAxEB
/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAw
IEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxgZEIIKRYqGx0fAjM0N5cu
L/xAAZAQADAQEBAQAAAAAAAAAAAAABAgMABAX/xAAjEQACAgICAgICAwEA
AAAAAAABAhEDIRIxBEFRYRMUIjJhgZEy/9oADAMBAAIRAxEAPwD...
"""

LILIAN_IMAGE = """
/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsL
DBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL
/2wBDAQkJCQwLDBgNDRgyIRo3MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj
IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAJbAZADASIAAhEBAx
EB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgED
AwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxgZEIIKRYqGx0fAjM0N5cu
L/xAAZAQADAQEBAQAAAAAAAAAAAAABAgMABAX/xAAjEQACAgICAgICAwEA
AAAAAAABAhEDIRIxBEFRYRMUIjJhgZEy/9oADAMBAAIRAxEAPwD...
"""

RENAD_IMAGE = """
/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsL
DBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL
/2wBDAQkJCQwLDBgNDRgyIRo3MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj
IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAKSAaADASIAAh
EBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAg
EDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxgZEIIKRYqGx0fAjM0N5cu
L/xAAZAQADAQEBAQAAAAAAAAAAAAABAgMABAX/xAAjEQACAgICAgICAwEAAAAA
AAABAhEDIRIxBEFRYRMUIjJhgZEy/9oADAMBAAIRAxEAPwD...
"""


# ============================================================
# ملاحظة مهمة
# ============================================================
#
# Telegram يحتاج Base64 كامل للصورة.
# إذا كانت الصور مدمجة من النسخة التي أعددتها لك،
# يجب أن تكون قيمة كل صورة هي السلسلة الكاملة بدون "..."
#
# الكود أدناه هو نظام البوت الكامل.
# ============================================================


def image_from_base64(data):
    """
    تحويل صورة Base64 المدمجة إلى ملف ذاكرة
    يمكن إرساله مباشرة إلى Telegram.
    """

    clean_data = "".join(
        data.split()
    )

    raw = base64.b64decode(
        clean_data
    )

    photo = BytesIO(raw)

    photo.name = "kids.jpg"

    photo.seek(0)

    return photo


# ============================================================
# بيانات الأطفال
# ============================================================

CHILDREN = {

    "lilian": {
        "name": "ليليان",
        "emoji": "👧",
        "photo": LILIAN_IMAGE,
    },

    "renad": {
        "name": "ريناد",
        "emoji": "👧",
        "photo": RENAD_IMAGE,
    },

    "mohammed": {
        "name": "محمد",
        "emoji": "👦",
        "photo": MOHAMMED_IMAGE,
    },

}


# ============================================================
# الطفل النشط لكل مستخدم
# ============================================================

active_child = {}


# ============================================================
# النقاط
# ============================================================

scores = {}


def get_score(user_id):

    return scores.get(
        user_id,
        0
    )


def add_score(
    user_id,
    points
):

    scores[user_id] = (
        get_score(user_id)
        + points
    )


# ============================================================
# صور التلوين
# ============================================================

COLORING = {

    "animals": {

        "title": "🐾 الحيوانات",

        "items": [

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
    },


    "nature": {

        "title": "🌳 الطبيعة",

        "items": [

            ("🌳", "الشجرة"),
            ("🌲", "شجرة الصنوبر"),
            ("🌴", "النخلة"),
            ("🌵", "الصبار"),
            ("🌻", "عباد الشمس"),
            ("🌷", "الزهرة"),
            ("🌹", "الوردة"),
            ("🌱", "النبتة"),
            ("🍀", "البرسيم"),
            ("🌈", "قوس قزح"),
            ("☀️", "الشمس"),
            ("☁️", "السحابة"),
            ("🌙", "القمر"),
            ("⭐", "النجمة"),

        ],
    },


    "food": {

        "title": "🍎 الفواكه والطعام",

        "items": [

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
    },


    "vehicles": {

        "title": "🚗 المركبات",

        "items": [

            ("🚗", "السيارة"),
            ("🚕", "سيارة الأجرة"),
            ("🚌", "الحافلة"),
            ("🚓", "سيارة الشرطة"),
            ("🚑", "الإسعاف"),
            ("🚒", "الإطفاء"),
            ("🚜", "الجرار"),
            ("🚲", "الدراجة"),
            ("🛴", "السكوتر"),
            ("✈️", "الطائرة"),
            ("🚁", "المروحية"),
            ("🚀", "الصاروخ"),
            ("🚢", "السفينة"),
            ("🚂", "القطار"),

        ],
    },


    "school": {

        "title": "📚 الأدوات والمدرسة",

        "items": [

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

        ],
    },


    "toys": {

        "title": "🧸 الألعاب",

        "items": [

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
    },


    "sea": {

        "title": "🌊 عالم البحر",

        "items": [

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
    },


    "space": {

        "title": "🚀 عالم الفضاء",

        "items": [

            ("🚀", "الصاروخ"),
            ("👨‍🚀", "رائد الفضاء"),
            ("🌍", "الأرض"),
            ("🌕", "القمر"),
            ("⭐", "النجمة"),
            ("☄️", "المذنب"),
            ("🪐", "الكوكب"),

        ],
    },

}


# ============================================================
# الحروف
# ============================================================

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


# ============================================================
# الأرقام
# ============================================================

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


# ============================================================
# القائمة الرئيسية
# ============================================================

def main_keyboard():

    return InlineKeyboardMarkup([

        [

            InlineKeyboardButton(
                "👧 ليليان",
                callback_data="child_lilian"
            ),

            InlineKeyboardButton(
                "👧 ريناد",
                callback_data="child_renad"
            ),

            InlineKeyboardButton(
                "👦 محمد",
                callback_data="child_mohammed"
            ),

        ],

        [

            InlineKeyboardButton(
                "🎨 الرسم والتلوين",
                callback_data="drawing"
            )

        ],

        [

            InlineKeyboardButton(
                "🐾 الحيوانات",
                callback_data="cat_animals"
            ),

            InlineKeyboardButton(
                "🌳 الطبيعة",
                callback_data="cat_nature"
            ),

        ],

        [

            InlineKeyboardButton(
                "🍎 الفواكه",
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
                "🌊 البحر",
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
                "🔀 إعادة تركيب",
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


# ============================================================
# قائمة الطفل
# ============================================================

def child_keyboard():

    return InlineKeyboardMarkup([

        [

            InlineKeyboardButton(
                "🎨 الرسم والتلوين",
                callback_data="drawing"
            )

        ],

        [

            InlineKeyboardButton(
                "🐾 الحيوانات",
                callback_data="cat_animals"
            ),

            InlineKeyboardButton(
                "🌳 الطبيعة",
                callback_data="cat_nature"
            ),

        ],

        [

            InlineKeyboardButton(
                "🍎 الفواكه",
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
                "🌊 البحر",
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
                "🔀 إعادة تركيب",
                callback_data="puzzle"
            ),

        ],

        [

            InlineKeyboardButton(
                "⭐ نجومي",
                callback_data="score"
            )

        ],

        [

            InlineKeyboardButton(
                "🏠 الرئيسية",
                callback_data="home"
            )

        ],

    ])


# ============================================================
# تعديل رسالة نصية أو رسالة صورة
# ============================================================

async def edit_message(
    query,
    text,
    keyboard=None
):

    if query.message.photo:

        await query.edit_message_caption(

            caption=text,

            reply_markup=keyboard,

            parse_mode="Markdown",

        )

    else:

        await query.edit_message_text(

            text=text,

            reply_markup=keyboard,

            parse_mode="Markdown",

        )


# ============================================================
# الرئيسية
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    active_child.pop(
        user_id,
        None
    )

    text = (

        "🌈✨ **عالم أطفال ليليان وريناد ومحمد** ✨🌈\n\n"

        "👧 ليليان\n"
        "👧 ريناد\n"
        "👦 محمد\n\n"

        "🎨 الرسم والتلوين\n"
        "🐾 الحيوانات\n"
        "🌳 الطبيعة\n"
        "🍎 الفواكه\n"
        "🚗 المركبات\n"
        "📚 الأدوات\n"
        "🧸 الألعاب\n"
        "🌊 البحر\n"
        "🚀 الفضاء\n"
        "🔤 الحروف\n"
        "🔢 الأرقام\n\n"

        "⭐ اجمع النجوم وكن بطلاً!\n\n"

        "اختر الطفل أو النشاط:"

    )

    await update.message.reply_text(

        text,

        reply_markup=main_keyboard(),

        parse_mode="Markdown",

    )


# ============================================================
# عرض الطفل مع صورته المدمجة
# ============================================================

async def show_child(
    query,
    child_id
):

    child = CHILDREN[child_id]

    active_child[
        query.from_user.id
    ] = child_id

    text = (

        f"{child['emoji']} **أهلاً {child['name']}!**\n\n"

        "🌈 هذه صفحتك الخاصة في عالم الأطفال.\n\n"

        f"⭐ نجومك: **{get_score(query.from_user.id)}**\n\n"

        "اختر نشاطاً:"

    )

    try:

        if query.message.photo:

            await query.message.delete()

        await query.message.chat.send_photo(

            photo=image_from_base64(
                child["photo"]
            ),

            caption=text,

            reply_markup=child_keyboard(),

            parse_mode="Markdown",

        )

    except Exception as error:

        print(
            "خطأ في إرسال صورة الطفل:",
            error
        )

        await edit_message(

            query,

            text,

            child_keyboard()

        )


# ============================================================
# قائمة التصنيفات
# ============================================================

async def category_menu(
    query,
    category
):

    data = COLORING[category]

    buttons = []

    row = []

    for index, (
        emoji,
        name
    ) in enumerate(
        data["items"]
    ):

        row.append(

            InlineKeyboardButton(

                f"{emoji} {name}",

                callback_data=(
                    f"item_{category}_{index}"
                ),

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

    await edit_message(

        query,

        f"{data['title']}\n\n"
        "🎨 اختر صورة لتلوينها:",

        InlineKeyboardMarkup(
            buttons
        ),

    )


# ============================================================
# عنصر التلوين
# ============================================================

async def show_item(
    query,
    category,
    index
):

    emoji, name = COLORING[
        category
    ]["items"][index]

    keyboard = InlineKeyboardMarkup([

        [

            InlineKeyboardButton(

                "🎨 تلوين",

                callback_data=(
                    f"paint_{category}_{index}"
                ),

            )

        ],

        [

            InlineKeyboardButton(

                "⭐ أنجزت",

                callback_data=(
                    f"done_{category}_{index}"
                ),

            )

        ],

        [

            InlineKeyboardButton(

                "🔙 رجوع",

                callback_data=(
                    f"cat_{category}"
                ),

            )

        ],

    ])

    await edit_message(

        query,

        f"🎨 **صفحة التلوين**\n\n"
        f"{emoji}\n\n"
        f"🖼️ {name}\n\n"
        "اختر:",

        keyboard,

    )


# ============================================================
# الألوان
# ============================================================

async def paint_menu(
    query,
    category,
    index
):

    emoji, name = COLORING[
        category
    ]["items"][index]

    keyboard = InlineKeyboardMarkup([

        [

            InlineKeyboardButton(
                "🔴 أحمر",
                callback_data="paintcolor_red"
            ),

            InlineKeyboardButton(
                "🔵 أزرق",
                callback_data="paintcolor_blue"
            ),

        ],

        [

            InlineKeyboardButton(
                "🟢 أخضر",
                callback_data="paintcolor_green"
            ),

            InlineKeyboardButton(
                "🟡 أصفر",
                callback_data="paintcolor_yellow"
            ),

        ],

        [

            InlineKeyboardButton(
                "🟣 بنفسجي",
                callback_data="paintcolor_purple"
            ),

            InlineKeyboardButton(
                "🟠 برتقالي",
                callback_data="paintcolor_orange"
            ),

        ],

        [

            InlineKeyboardButton(

                "⭐ انتهيت",

                callback_data=(
                    f"done_{category}_{index}"
                ),

            )

        ],

        [

            InlineKeyboardButton(

                "🔙 رجوع",

                callback_data=(
                    f"item_{category}_{index}"
                ),

            )

        ],

    ])

    await edit_message(

        query,

        f"🎨 **تلوين {name}**\n\n"
        f"{emoji}\n\n"
        "🖍️ اختر اللون:",

        keyboard,

    )


# ============================================================
# الحروف
# ============================================================

async def letters_menu(query):

    buttons = []

    row = []

    for index, (
        letter,
        word
    ) in enumerate(LETTERS):

        row.append(

            InlineKeyboardButton(

                letter,

                callback_data=(
                    f"letter_{index}"
                ),

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

    await edit_message(

        query,

        "🔤 **الحروف العربية**\n\n"
        "اختر حرفاً:",

        InlineKeyboardMarkup(
            buttons
        ),

    )


async def show_letter(
    query,
    index
):

    letter, word = LETTERS[index]

    await edit_message(

        query,

        f"🔤 **حرف {letter}**\n\n"
        f"✨ {word}\n\n"
        "🎨 تعلّم الحرف ثم اضغط الزر للحصول على نجمة.",

        InlineKeyboardMarkup([

            [

                InlineKeyboardButton(

                    "⭐ تعلمت الحرف",

                    callback_data=(
                        f"letter_done_{index}"
                    ),

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

            ],

        ]),

    )


# ============================================================
# الأرقام
# ============================================================

async def numbers_menu(query):

    buttons = []

    row = []

    for index, (
        number,
        name
    ) in enumerate(NUMBERS):

        row.append(

            InlineKeyboardButton(

                number,

                callback_data=(
                    f"number_{index}"
                ),

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

    await edit_message(

        query,

        "🔢 **الأرقام**\n\n"
        "اختر رقماً:",

        InlineKeyboardMarkup(
            buttons
        ),

    )


async def show_number(
    query,
    index
):

    number, name = NUMBERS[index]

    await edit_message(

        query,

        f"🔢 **الرقم {number}**\n\n"
        f"📚 اسمه: {name}\n\n"
        "⭐ اضغط تعلمت الرقم للحصول على نجمة.",

        InlineKeyboardMarkup([

            [

                InlineKeyboardButton(

                    "⭐ تعلمت الرقم",

                    callback_data=(
                        f"number_done_{index}"
                    ),

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

            ],

        ]),

    )


# ============================================================
# أكمل الصورة
# ============================================================

async def missing_game(query):

    games = [

        (

            "🐶 + ؟",

            "ما الذي يناسب الكلب؟",

            [

                ("🦴", True),
                ("🚀", False),
                ("🌊", False),

            ],

        ),

        (

            "🌳 + ؟",

            "ما الذي يناسب الشجرة؟",

            [

                ("🌱", True),
                ("🚗", False),
                ("🐟", False),

            ],

        ),

        (

            "🐟 + ؟",

            "أين تعيش السمكة؟",

            [

                ("🌊", True),
                ("🚀", False),
                ("🏠", False),

            ],

        ),

        (

            "☀️ + ؟",

            "ما الشيء الذي يناسب الشمس؟",

            [

                ("🌈", True),
                ("🐟", False),
                ("🚗", False),

            ],

        ),

    ]

    question, title, answers = random.choice(
        games
    )

    buttons = []

    for emoji, correct in answers:

        buttons.append([

            InlineKeyboardButton(

                emoji,

                callback_data=(

                    "missing_correct"

                    if correct

                    else

                    "missing_wrong"

                ),

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

    await edit_message(

        query,

        f"🧩 **أكمل الصورة**\n\n"
        f"{question}\n\n"
        f"{title}\n\n"
        "اختر الإجابة الصحيحة:",

        InlineKeyboardMarkup(
            buttons
        ),

    )


# ============================================================
# إعادة تركيب الصورة
# ============================================================

async def puzzle_game(query):

    pieces = [

        "🌳",
        "☀️",
        "🏠",
        "🌸",
        "🐦",
        "🦋",

    ]

    random.shuffle(
        pieces
    )

    picture = "   ".join(
        pieces
    )

    await edit_message(

        query,

        f"🔀 **إعادة تركيب الصورة**\n\n"
        f"{picture}\n\n"
        "🧩 حاول تخيل الصورة كاملة ورتب عناصرها!",

        InlineKeyboardMarkup([

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

            ],

        ]),

    )


# ============================================================
# الرسم
# ============================================================

async def drawing_menu(query):

    await edit_message(

        query,

        "🎨 **مرسم عالم الأطفال**\n\n"
        "اختر شيئاً تريد رسمه وتلوينه:",

        InlineKeyboardMarkup([

            [

                InlineKeyboardButton(
                    "🌳 شجرة",
                    callback_data="draw_tree"
                ),

                InlineKeyboardButton(
                    "🐶 حيوان",
                    callback_data="draw_animal"
                ),

            ],

            [

                InlineKeyboardButton(
                    "🏠 بيت",
                    callback_data="draw_house"
                ),

                InlineKeyboardButton(
                    "🚗 سيارة",
                    callback_data="draw_car"
                ),

            ],

            [

                InlineKeyboardButton(
                    "🚀 صاروخ",
                    callback_data="draw_rocket"
                ),

                InlineKeyboardButton(
                    "🌈 قوس قزح",
                    callback_data="draw_rainbow"
                ),

            ],

            [

                InlineKeyboardButton(
                    "🏠 الرئيسية",
                    callback_data="home"
                )

            ],

        ]),

    )


async def drawing_page(
    query,
    data
):

    names = {

        "draw_tree":
            "🌳 الشجرة",

        "draw_animal":
            "🐶 الحيوان",

        "draw_house":
            "🏠 البيت",

        "draw_car":
            "🚗 السيارة",

        "draw_rocket":
            "🚀 الصاروخ",

        "draw_rainbow":
            "🌈 قوس قزح",

    }

    name = names.get(
        data,
        "🎨 الرسم"
    )

    await edit_message(

        query,

        f"🎨 **{name}**\n\n"
        "🖍️ اختر لونك:",

        InlineKeyboardMarkup([

            [

                InlineKeyboardButton(
                    "🔴",
                    callback_data="paintcolor_red"
                ),

                InlineKeyboardButton(
                    "🔵",
                    callback_data="paintcolor_blue"
                ),

                InlineKeyboardButton(
                    "🟢",
                    callback_data="paintcolor_green"
                ),

            ],

            [

                InlineKeyboardButton(
                    "🟡",
                    callback_data="paintcolor_yellow"
                ),

                InlineKeyboardButton(
                    "🟣",
                    callback_data="paintcolor_purple"
                ),

                InlineKeyboardButton(
                    "🟠",
                    callback_data="paintcolor_orange"
                ),

            ],

            [

                InlineKeyboardButton(

                    "⭐ أنهيت الرسم",

                    callback_data="drawing_done"

                )

            ],

            [

                InlineKeyboardButton(

                    "🏠 الرئيسية",

                    callback_data="home"

                )

            ],

        ]),

    )


# ============================================================
# النجوم
# ============================================================

async def score_menu(query):

    score = get_score(
        query.from_user.id
    )

    if score < 10:

        level = "🌱 مبتدئ"

    elif score < 30:

        level = "🎨 فنان صغير"

    elif score < 60:

        level = "🏆 بطل"

    else:

        level = "👑 بطل عالم الأطفال"

    await edit_message(

        query,

        f"⭐ **نجومي**\n\n"
        f"⭐ عدد النجوم: **{score}**\n\n"
        f"🏅 المستوى: {level}\n\n"
        "واصل اللعب والتعلم! 🌈",

        InlineKeyboardMarkup([

            [

                InlineKeyboardButton(

                    "🏠 الرئيسية",

                    callback_data="home"

                )

            ]

        ]),

    )


# ============================================================
# استقبال أي صورة من المستخدم
# ============================================================

async def receive_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(

        "🖼️ الصورة وصلت! 🌈\n\n"

        "صور محمد وليليان وريناد مدمجة أصلاً "
        "داخل كود البوت، ولا تحتاج إلى روابط خارجية."

    )


# ============================================================
# معالج جميع الأزرار
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id


    # --------------------------------------------------------
    # الرئيسية
    # --------------------------------------------------------

    if data == "home":

        if query.message.photo:

            await query.message.delete()

            await query.message.chat.send_message(

                "🌈✨ **عالم أطفال ليليان وريناد ومحمد** ✨🌈\n\n"
                "👧 ليليان   👧 ريناد   👦 محمد\n\n"
                "🎨 اختر نشاطاً:",
                
                reply_markup=main_keyboard(),

                parse_mode="Markdown",

            )

        else:

            await query.edit_message_text(

                "🌈✨ **عالم أطفال ليليان وريناد ومحمد** ✨🌈\n\n"
                "👧 ليليان   👧 ريناد   👦 محمد\n\n"
                "🎨 اختر نشاطاً:",

                reply_markup=main_keyboard(),

                parse_mode="Markdown",

            )

        return


    # --------------------------------------------------------
    # الأطفال
    # --------------------------------------------------------

    if data.startswith("child_"):

        child_id = data.replace(
            "child_",
            "",
            1
        )

        if child_id in CHILDREN:

            await show_child(
                query,
                child_id
            )

        return


    # --------------------------------------------------------
    # التصنيفات
    # --------------------------------------------------------

    if data.startswith("cat_"):

        category = data.replace(
            "cat_",
            "",
            1
        )

        if category in COLORING:

            await category_menu(
                query,
                category
            )

        return


    # --------------------------------------------------------
    # العناصر
    # --------------------------------------------------------

    if data.startswith("item_"):

        parts = data.split("_")

        if len(parts) == 3:

            category = parts[1]

            try:

                index = int(
                    parts[2]
                )

            except ValueError:

                return

            if (

                category in COLORING

                and

                0 <= index < len(
                    COLORING[
                        category
                    ]["items"]
                )

            ):

                await show_item(

                    query,

                    category,

                    index

                )

        return


    # --------------------------------------------------------
    # التلوين
    # --------------------------------------------------------

    if (

        data.startswith("paint_")

        and

        not data.startswith(
            "paintcolor_"
        )

    ):

        parts = data.split("_")

        if len(parts) == 3:

            category = parts[1]

            try:

                index = int(
                    parts[2]
                )

            except ValueError:

                return

            if category in COLORING:

                await paint_menu(

                    query,

                    category,

                    index

                )

        return


    # --------------------------------------------------------
    # اختيار اللون
    # --------------------------------------------------------

    if data.startswith(
        "paintcolor_"
    ):

        await query.answer(

            "🎨 لون رائع! 🌈",

            show_alert=True

        )

        return


    # --------------------------------------------------------
    # إنهاء التلوين
    # --------------------------------------------------------

    if data.startswith(
        "done_"
    ):

        add_score(

            user_id,

            5

        )

        await edit_message(

            query,

            "🎉🌈 أحسنت يا بطل!\n\n"
            "🎨 أنهيت النشاط بنجاح.\n\n"
            "⭐ +5 نجوم",

            InlineKeyboardMarkup([

                [

                    InlineKeyboardButton(

                        "🎨 نشاط آخر",

                        callback_data="drawing"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🧩 الألعاب",

                        callback_data="missing"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🏠 الرئيسية",

                        callback_data="home"

                    )

                ],

            ]),

        )

        return


    # --------------------------------------------------------
    # الرسم
    # --------------------------------------------------------

    if data == "drawing":

        await drawing_menu(
            query
        )

        return


    if data.startswith(
        "draw_"
    ):

        await drawing_page(

            query,

            data

        )

        return


    if data == "drawing_done":

        add_score(

            user_id,

            10

        )

        await edit_message(

            query,

            "🎉🎨 رائع!\n\n"
            "أنهيت الرسم بنجاح.\n"
            "⭐ +10 نجوم",

            InlineKeyboardMarkup([

                [

                    InlineKeyboardButton(

                        "🎨 رسم آخر",

                        callback_data="drawing"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🏠 الرئيسية",

                        callback_data="home"

                    )

                ],

            ]),

        )

        return


    # --------------------------------------------------------
    # الحروف
    # --------------------------------------------------------

    if data == "letters":

        await letters_menu(
            query
        )

        return


    if data.startswith(
        "letter_done_"
    ):

        add_score(

            user_id,

            5

        )

        await query.answer(

            "⭐ أحسنت! +5",

            show_alert=True

        )

        await letters_menu(
            query
        )

        return


    if data.startswith(
        "letter_"
    ):

        try:

            index = int(
                data.split("_")[1]
            )

        except ValueError:

            return

        if 0 <= index < len(
            LETTERS
        ):

            await show_letter(

                query,

                index

            )

        return


    # --------------------------------------------------------
    # الأرقام
    # --------------------------------------------------------

    if data == "numbers":

        await numbers_menu(
            query
        )

        return


    if data.startswith(
        "number_done_"
    ):

        add_score(

            user_id,

            5

        )

        await query.answer(

            "⭐ أحسنت! +5",

            show_alert=True

        )

        await numbers_menu(
            query
        )

        return


    if data.startswith(
        "number_"
    ):

        try:

            index = int(
                data.split("_")[1]
            )

        except ValueError:

            return

        if 0 <= index < len(
            NUMBERS
        ):

            await show_number(

                query,

                index

            )

        return


    # --------------------------------------------------------
    # أكمل الصورة
    # --------------------------------------------------------

    if data == "missing":

        await missing_game(
            query
        )

        return


    if data == "missing_correct":

        add_score(

            user_id,

            10

        )

        await query.answer(

            "🎉 إجابة صحيحة! ⭐ +10",

            show_alert=True

        )

        await missing_game(
            query
        )

        return


    if data == "missing_wrong":

        await query.answer(

            "😊 حاول مرة أخرى",

            show_alert=True

        )

        return


    # --------------------------------------------------------
    # إعادة التركيب
    # --------------------------------------------------------

    if data == "puzzle":

        await puzzle_game(
            query
        )

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

        await puzzle_game(
            query
        )

        return


    # --------------------------------------------------------
    # النجوم
    # --------------------------------------------------------

    if data == "score":

        await score_menu(
            query
        )

        return


# ============================================================
# تشغيل البوت
# ============================================================

def main():

    print(
        "🌈 عالم أطفال ليليان وريناد ومحمد يعمل الآن..."
    )

    app = (

        Application

        .builder()

        .token(
            BOT_TOKEN
        )

        .build()

    )


    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )


    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receive_photo

        )

    )


    app.add_handler(

        CallbackQueryHandler(

            button_handler

        )

    )


    app.run_polling(

        drop_pending_updates=True

    )


if __name__ == "__main__":

    main()
