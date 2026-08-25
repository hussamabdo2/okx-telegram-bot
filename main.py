import os
import asyncio
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


# ============================================================
# الإعدادات
# ============================================================

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN غير موجود في Railway Variables"
    )


# ============================================================
# صفحة عالم الأطفال
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>عالم الأطفال</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Tahoma, sans-serif;
    background: linear-gradient(
        135deg,
        #fff3b0,
        #c8f7ff
    );
    min-height: 100vh;
    color: #333;
}

header {
    text-align: center;
    padding: 25px 10px;
}

.logo {
    font-size: 65px;
}

h1 {
    font-size: 32px;
    margin: 5px;
}

.container {
    max-width: 950px;
    margin: auto;
    padding: 15px;
}

.top {
    background: white;
    border-radius: 25px;
    padding: 15px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    box-shadow: 0 5px 18px rgba(0,0,0,.12);
}

.stars {
    background: #fff0a0;
    border-radius: 20px;
    padding: 8px 15px;
}

.menu {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.card {
    border: 0;
    background: white;
    border-radius: 25px;
    min-height: 140px;
    padding: 20px;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(0,0,0,.12);
}

.card span {
    display: block;
    font-size: 50px;
    margin-bottom: 10px;
}

.page {
    display: none;
    background: white;
    border-radius: 25px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,.12);
}

.page.active {
    display: block;
}

.back {
    border: 0;
    padding: 12px 20px;
    border-radius: 15px;
    cursor: pointer;
}

.title {
    text-align: center;
    font-size: 28px;
    margin: 20px;
}

.center {
    text-align: center;
}

.big {
    font-size: 100px;
    margin: 20px;
    line-height: 1.5;
}

button {
    border: 0;
    border-radius: 16px;
    padding: 13px 20px;
    margin: 5px;
    font-size: 17px;
    cursor: pointer;
}

.green {
    background: #4caf50;
    color: white;
}

.blue {
    background: #2196f3;
    color: white;
}

.orange {
    background: #ff9800;
    color: white;
}

.red {
    background: #f44336;
    color: white;
}

#canvas {
    width: 100%;
    max-width: 800px;
    height: 450px;
    border: 4px solid #ddd;
    border-radius: 20px;
    display: block;
    margin: auto;
    background: white;
    touch-action: none;
}

.colors {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 15px;
}

.color {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 2px 7px rgba(0,0,0,.25);
    cursor: pointer;
}

.letter,
.number {
    font-size: 130px;
    font-weight: bold;
    text-align: center;
}

.letter {
    color: #ff7043;
}

.number {
    color: #2196f3;
}

.puzzle {
    max-width: 500px;
    margin: 20px auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
}

.piece {
    aspect-ratio: 1;
    background: #f5f5f5;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 45px;
    cursor: grab;
    user-select: none;
}

@media (max-width: 600px) {

    .menu {
        grid-template-columns: repeat(2, 1fr);
    }

    .card {
        font-size: 16px;
        min-height: 120px;
    }

    .card span {
        font-size: 38px;
    }

    #canvas {
        height: 350px;
    }

}

</style>

</head>

<body>

<header>

<div class="logo">🎨</div>

<h1>عالم الأطفال</h1>

<p>ارسم • لوّن • تعلّم • العب</p>

</header>

<div class="container">

<div class="top">

<div>
👋 مرحباً يا بطل!
</div>

<div class="stars">
⭐ <span id="stars">0</span>
</div>

</div>


<div id="home">

<div class="menu">

<button class="card" onclick="drawing()">
<span>🖍️</span>
الرسم والتلوين
</button>

<button class="card" onclick="category('nature')">
<span>🌳</span>
الطبيعة
</button>

<button class="card" onclick="category('animals')">
<span>🐶</span>
الحيوانات
</button>

<button class="card" onclick="category('objects')">
<span>🧰</span>
الأدوات والأشياء
</button>

<button class="card" onclick="letters()">
<span>🔤</span>
الحروف العربية
</button>

<button class="card" onclick="numbers()">
<span>🔢</span>
الأرقام
</button>

<button class="card" onclick="missing()">
<span>🧩</span>
أكمل الصورة
</button>

<button class="card" onclick="puzzle()">
<span>🔀</span>
إعادة تركيب الصورة
</button>

</div>

</div>


<div id="page" class="page">

<button class="back" onclick="home()">
🔙 العودة
</button>

<div id="content"></div>

</div>

</div>


<script>

let stars = Number(
    localStorage.getItem("kids_stars") || 0
);

function updateStars() {

    document.getElementById(
        "stars"
    ).textContent = stars;

}

function addStars(amount) {

    stars += amount;

    localStorage.setItem(
        "kids_stars",
        stars
    );

    updateStars();

}

updateStars();


function home() {

    document.getElementById(
        "home"
    ).style.display = "block";

    document.getElementById(
        "page"
    ).classList.remove("active");

}


function show(html) {

    document.getElementById(
        "home"
    ).style.display = "none";

    document.getElementById(
        "page"
    ).classList.add("active");

    document.getElementById(
        "content"
    ).innerHTML = html;

}


// ============================================================
// الرسم والتلوين
// ============================================================

let canvas = null;
let ctx = null;
let drawingNow = false;
let currentColor = "#ff0000";
let brush = 15;


function drawing() {

    show(`

    <div class="title">
        🖍️ الرسم والتلوين
    </div>

    <canvas
        id="canvas"
        width="900"
        height="600">
    </canvas>

    <div class="colors">

        <div
            class="color"
            style="background:#ff0000"
            onclick="color('#ff0000')">
        </div>

        <div
            class="color"
            style="background:#ff9800"
            onclick="color('#ff9800')">
        </div>

        <div
            class="color"
            style="background:#ffeb3b"
            onclick="color('#ffeb3b')">
        </div>

        <div
            class="color"
            style="background:#4caf50"
            onclick="color('#4caf50')">
        </div>

        <div
            class="color"
            style="background:#2196f3"
            onclick="color('#2196f3')">
        </div>

        <div
            class="color"
            style="background:#9c27b0"
            onclick="color('#9c27b0')">
        </div>

        <div
            class="color"
            style="background:#e91e63"
            onclick="color('#e91e63')">
        </div>

        <div
            class="color"
            style="background:#000000"
            onclick="color('#000000')">
        </div>

    </div>

    <div class="center">

        <button onclick="brushSize(5)">
            🖊️ صغير
        </button>

        <button onclick="brushSize(15)">
            🖌️ متوسط
        </button>

        <button onclick="brushSize(30)">
            🖍️ كبير
        </button>

        <button onclick="clearCanvas()">
            🗑️ مسح
        </button>

        <button class="blue" onclick="saveDrawing()">
            💾 حفظ
        </button>

        <button class="green" onclick="finishDrawing()">
            ⭐ انتهيت
        </button>

    </div>

    `);

    canvas = document.getElementById("canvas");

    ctx = canvas.getContext("2d");

    ctx.fillStyle = "#ffffff";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    canvas.addEventListener(
        "pointerdown",
        startDrawing
    );

    canvas.addEventListener(
        "pointermove",
        drawLine
    );

    canvas.addEventListener(
        "pointerup",
        stopDrawing
    );

    canvas.addEventListener(
        "pointercancel",
        stopDrawing
    );

}


function getPosition(event) {

    const rect =
        canvas.getBoundingClientRect();

    return {

        x:
            (event.clientX - rect.left)
            * canvas.width
            / rect.width,

        y:
            (event.clientY - rect.top)
            * canvas.height
            / rect.height

    };

}


function startDrawing(event) {

    drawingNow = true;

    const position =
        getPosition(event);

    ctx.beginPath();

    ctx.moveTo(
        position.x,
        position.y
    );

}


function drawLine(event) {

    if (!drawingNow) {
        return;
    }

    const position =
        getPosition(event);

    ctx.lineWidth = brush;

    ctx.lineCap = "round";

    ctx.strokeStyle =
        currentColor;

    ctx.lineTo(
        position.x,
        position.y
    );

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(
        position.x,
        position.y
    );

}


function stopDrawing() {

    drawingNow = false;

}


function color(value) {

    currentColor = value;

}


function brushSize(value) {

    brush = value;

}


function clearCanvas() {

    ctx.fillStyle = "#ffffff";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

}


function saveDrawing() {

    const link =
        document.createElement("a");

    link.download =
        "kids-drawing.png";

    link.href =
        canvas.toDataURL(
            "image/png"
        );

    link.click();

}


function finishDrawing() {

    addStars(5);

    alert(
        "🎉 أحسنت!\n⭐ حصلت على 5 نجوم"
    );

}


// ============================================================
// الطبيعة والحيوانات والأدوات
// ============================================================

function category(type) {

    let title = "";
    let emojis = "";

    if (type === "nature") {

        title = "🌳 الطبيعة";

        emojis =
            "🌳 🌸 🌺 ☀️ 🌈 ☁️ 🌱";

    }

    if (type === "animals") {

        title = "🐶 الحيوانات";

        emojis =
            "🐶 🐱 🦁 🐘 🐰 🐼 🦋";

    }

    if (type === "objects") {

        title =
            "🧰 الأدوات والأشياء";

        emojis =
            "🚗 ✈️ 🏠 🎒 ✏️ ⚽ 🧸";

    }

    show(`

        <div class="center">

            <div class="title">
                ${title}
            </div>

            <div class="big">
                ${emojis}
            </div>

            <p>
                اختر النشاط الذي تريد.
            </p>

            <button
                class="green"
                onclick="drawing()">
                🖍️ ابدأ الرسم والتلوين
            </button>

        </div>

    `);

}


// ============================================================
// الحروف
// ============================================================

const lettersData = [

    ["أ", "أسد 🦁"],
    ["ب", "بطة 🦆"],
    ["ت", "تفاحة 🍎"],
    ["ث", "ثعلب 🦊"],
    ["ج", "جمل 🐪"],
    ["ح", "حصان 🐴"],
    ["خ", "خروف 🐑"],
    ["د", "دجاجة 🐔"],
    ["ذ", "ذئب 🐺"],
    ["ر", "رمان 🍎"],
    ["ز", "زرافة 🦒"],
    ["س", "سمكة 🐟"],
    ["ش", "شجرة 🌳"],
    ["ص", "صقر 🦅"],
    ["ض", "ضفدع 🐸"],
    ["ط", "طائرة ✈️"],
    ["ظ", "ظرف ✉️"],
    ["ع", "عصفور 🐦"],
    ["غ", "غزال 🦌"],
    ["ف", "فيل 🐘"],
    ["ق", "قمر 🌙"],
    ["ك", "كتاب 📖"],
    ["ل", "ليمون 🍋"],
    ["م", "موز 🍌"],
    ["ن", "نحلة 🐝"],
    ["هـ", "هلال 🌙"],
    ["و", "وردة 🌹"],
    ["ي", "يد ✋"]

];

let letterIndex = 0;


function letters() {

    letterIndex = 0;

    showLetter();

}


function showLetter() {

    const item =
        lettersData[letterIndex];

    show(`

        <div class="center">

            <div class="title">
                🔤 الحروف العربية
            </div>

            <div class="letter">
                ${item[0]}
            </div>

            <h2>
                ${item[1]}
            </h2>

            <button
                class="blue"
                onclick="nextLetter()">
                ➡️ الحرف التالي
            </button>

            <button
                class="green"
                onclick="learnedLetter()">
                ⭐ تعلمت الحرف
            </button>

        </div>

    `);

}


function learnedLetter() {

    addStars(5);

}


function nextLetter() {

    letterIndex++;

    if (
        letterIndex >=
        lettersData.length
    ) {

        letterIndex = 0;

        addStars(20);

        alert(
            "🎉 أكملت الحروف!"
        );

    }

    showLetter();

}


// ============================================================
// الأرقام
// ============================================================

const numbersData = [

    ["٠", "صفر"],
    ["١", "واحد"],
    ["٢", "اثنان"],
    ["٣", "ثلاثة"],
    ["٤", "أربعة"],
    ["٥", "خمسة"],
    ["٦", "ستة"],
    ["٧", "سبعة"],
    ["٨", "ثمانية"],
    ["٩", "تسعة"],
    ["١٠", "عشرة"]

];

let numberIndex = 0;


function numbers() {

    numberIndex = 0;

    showNumber();

}


function showNumber() {

    const item =
        numbersData[numberIndex];

    show(`

        <div class="center">

            <div class="title">
                🔢 الأرقام
            </div>

            <div class="number">
                ${item[0]}
            </div>

            <h2>
                ${item[1]}
            </h2>

            <button
                class="blue"
                onclick="nextNumber()">
                ➡️ الرقم التالي
            </button>

            <button
                class="green"
                onclick="learnedNumber()">
                ⭐ تعلمت الرقم
            </button>

        </div>

    `);

}


function learnedNumber() {

    addStars(5);

}


function nextNumber() {

    numberIndex++;

    if (
        numberIndex >=
        numbersData.length
    ) {

        numberIndex = 0;

        addStars(20);

        alert(
            "🎉 أكملت الأرقام!"
        );

    }

    showNumber();

}


// ============================================================
// أكمل الصورة
// ============================================================

function missing() {

    show(`

        <div class="center">

            <div class="title">
                🧩 أكمل الصورة
            </div>

            <div class="big">
                🐱
            </div>

            <h2>
                اختر الحيوان الصحيح:
            </h2>

            <button
                style="font-size:45px"
                onclick="correctMissing()">
                🐈
            </button>

            <button
                style="font-size:45px"
                onclick="wrongMissing()">
                🐘
            </button>

            <button
                style="font-size:45px"
                onclick="wrongMissing()">
                🦁
            </button>

        </div>

    `);

}


function correctMissing() {

    addStars(10);

    alert(
        "🎉 إجابة صحيحة!\n⭐ +10"
    );

}


function wrongMissing() {

    alert(
        "😊 حاول مرة أخرى"
    );

}


// ============================================================
// إعادة تركيب الصورة
// ============================================================

const puzzleItems = [

    "🌳",
    "🍎",
    "🐦",
    "☀️",
    "🌸",
    "🦋",
    "🌱",
    "☁️",
    "🏠"

];


function puzzle() {

    show(`

        <div class="center">

            <div class="title">
                🔀 إعادة تركيب الصورة
            </div>

            <p>
                رتب القطع ثم اضغط تحقق.
            </p>

        </div>

        <div
            id="puzzle"
            class="puzzle">
        </div>

        <div class="center">

            <button
                class="orange"
                onclick="shufflePuzzle()">
                🔀 خلط
            </button>

            <button
                class="green"
                onclick="checkPuzzle()">
                ⭐ تحقق
            </button>

        </div>

    `);

    createPuzzle();

}


function createPuzzle() {

    const box =
        document.getElementById(
            "puzzle"
        );

    box.innerHTML = "";

    puzzleItems.forEach(
        function(item, index) {

            const piece =
                document.createElement(
                    "div"
                );

            piece.className =
                "piece";

            piece.textContent =
                item;

            piece.dataset.correct =
                index;

            piece.draggable = true;

            box.appendChild(piece);

        }
    );

    enablePuzzleDrag();

}


function shufflePuzzle() {

    const box =
        document.getElementById(
            "puzzle"
        );

    const pieces =
        Array.from(
            box.children
        );

    pieces.sort(
        function() {
            return Math.random() - 0.5;
        }
    );

    pieces.forEach(
        function(piece) {
            box.appendChild(piece);
        }
    );

}


function enablePuzzleDrag() {

    const box =
        document.getElementById(
            "puzzle"
        );

    let dragged = null;

    box.addEventListener(
        "dragstart",
        function(event) {

            dragged =
                event.target;

        }
    );

    box.addEventListener(
        "dragover",
        function(event) {

            event.preventDefault();

        }
    );

    box.addEventListener(
        "drop",
        function(event) {

            event.preventDefault();

            const target =
                event.target;

            if (
                !target.classList.contains(
                    "piece"
                )
            ) {
                return;
            }

            if (
                !dragged ||
                target === dragged
            ) {
                return;
            }

            const pieces =
                Array.from(
                    box.children
                );

            const from =
                pieces.indexOf(
                    dragged
                );

            const to =
                pieces.indexOf(
                    target
                );

            if (from < to) {

                box.insertBefore(
                    dragged,
                    target.nextSibling
                );

            } else {

                box.insertBefore(
                    dragged,
                    target
                );

            }

        }
    );

}


function checkPuzzle() {

    const box =
        document.getElementById(
            "puzzle"
        );

    const pieces =
        Array.from(
            box.children
        );

    let correct = true;

    pieces.forEach(
        function(piece, index) {

            if (
                Number(
                    piece.dataset.correct
                ) !== index
            ) {

                correct = false;

            }

        }
    );

    if (correct) {

        addStars(15);

        alert(
            "🎉 ممتاز!\n" +
            "أكملت تركيب الصورة!\n" +
            "⭐ +15"
        );

    } else {

        alert(
            "😊 الصورة لم تكتمل بعد."
        );

    }

}

</script>

</body>

</html>
"""


# ============================================================
# Web server
# ============================================================

async def health(request):
    return web.Response(
        text="Kids Bot is running"
    )


async def kids_page(request):
    return web.Response(
        text=HTML,
        content_type="text/html",
        charset="utf-8"
    )


async def start_web_server():
    app = web.Application()

    app.router.add_get(
        "/",
        health
    )

    app.router.add_get(
        "/health",
        health
    )

    app.router.add_get(
        "/kids",
        kids_page
    )

    runner = web.AppRunner(app)

    await runner.setup()

    port = int(
        os.environ.get(
            "PORT",
            "8080"
        )
    )

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(
        f"Web server running on port {port}"
    )


# ============================================================
# Telegram Bot
# ============================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [

        [
            InlineKeyboardButton(
                "🎨 عالم الأطفال",
                callback_data="kids"
            )
        ],

        [
            InlineKeyboardButton(
                "🖍️ الرسم والتلوين",
                callback_data="drawing"
            )
        ],

        [
            InlineKeyboardButton(
                "🔤 الحروف والأرقام",
                callback_data="learning"
            )
        ],

        [
            InlineKeyboardButton(
                "🧩 الألعاب",
                callback_data="games"
            )
        ]

    ]

    await update.message.reply_text(
        "🌟 أهلاً بك في عالم الأطفال!\n\n"
        "🎨 ارسم ولوّن\n"
        "🔤 تعلّم الحروف\n"
        "🔢 تعلّم الأرقام\n"
        "🧩 حل الألعاب\n"
        "🔀 أعد تركيب الصور\n\n"
        "اختر نشاطاً:",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


def public_url():

    domain = os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN"
    )

    if domain:

        if domain.startswith("http://") or domain.startswith("https://"):
            return domain

        return "https://" + domain

    return ""


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    url = public_url()

    if query.data == "kids":

        if not url:

            await query.edit_message_text(
                "🎨 عالم الأطفال جاهز، "
                "لكن يجب إضافة Public Domain في Railway."
            )

            return

        keyboard = [[
            InlineKeyboardButton(
                "🎨 افتح عالم الأطفال",
                url=url + "/kids"
            )
        ]]

        await query.edit_message_text(
            "🌈 مرحباً بك في عالم الأطفال!\n\n"
            "الرسم والتلوين والألعاب التعليمية "
            "في انتظارك 🎨",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    elif query.data == "drawing":

        if not url:

            await query.edit_message_text(
                "افتح عالم الأطفال من Railway."
            )

            return

        keyboard = [[
            InlineKeyboardButton(
                "🖍️ ابدأ الرسم",
                url=url + "/kids"
            )
        ]]

        await query.edit_message_text(
            "🖍️ حان وقت الرسم والتلوين!",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    elif query.data == "learning":

        if not url:

            await query.edit_message_text(
                "افتح عالم الأطفال من Railway."
            )

            return

        keyboard = [[
            InlineKeyboardButton(
                "🔤 تعلّم والعب",
                url=url + "/kids"
            )
        ]]

        await query.edit_message_text(
            "🔤 الحروف والأرقام تنتظرك!",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    elif query.data == "games":

        if not url:

            await query.edit_message_text(
                "افتح عالم الأطفال من Railway."
            )

            return

        keyboard = [[
            InlineKeyboardButton(
                "🧩 ابدأ الألعاب",
                url=url + "/kids"
            )
        ]]

        await query.edit_message_text(
            "🧩 أكمل الصورة وأعد تركيبها!",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )


# ============================================================
# تشغيل البرنامج
# ============================================================

async def main():

    await start_web_server()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print(
        "🎨 Kids Telegram Bot started"
    )

    await application.initialize()

    await application.start()

    await application.updater.start_polling()

    try:

        await asyncio.Event().wait()

    finally:

        await application.updater.stop()

        await application.stop()

        await application.shutdown()


if __name__ == "__main__":

    asyncio.run(main())
