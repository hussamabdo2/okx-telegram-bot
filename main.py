import os
import asyncio
import html
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN غير موجود في Railway Variables")


# =========================================================
# بيانات الأنشطة
# =========================================================

CATEGORIES = {
    "trees": {
        "name": "🌳 الأشجار والطبيعة",
        "items": [
            ("🌳", "شجرة"),
            ("🌲", "شجرة صنوبر"),
            ("🌴", "نخلة"),
            ("🌵", "صبار"),
            ("🌻", "زهرة"),
            ("🌷", "زهرة"),
            ("🌹", "وردة"),
            ("🌱", "نبتة"),
            ("🍀", "برسيم"),
            ("🌈", "قوس قزح"),
            ("☀️", "الشمس"),
            ("☁️", "السحابة"),
            ("🌙", "القمر"),
            ("⭐", "نجمة"),
        ],
    },
    "animals": {
        "name": "🐾 الحيوانات",
        "items": [
            ("🐶", "كلب"),
            ("🐱", "قطة"),
            ("🐭", "فأر"),
            ("🐰", "أرنب"),
            ("🦊", "ثعلب"),
            ("🐻", "دب"),
            ("🐼", "باندا"),
            ("🐨", "كوالا"),
            ("🐯", "نمر"),
            ("🦁", "أسد"),
            ("🐮", "بقرة"),
            ("🐷", "خنزير"),
            ("🐸", "ضفدع"),
            ("🐵", "قرد"),
            ("🐔", "دجاجة"),
            ("🐧", "بطريق"),
            ("🐦", "عصفور"),
            ("🦋", "فراشة"),
            ("🐝", "نحلة"),
            ("🐢", "سلحفاة"),
            ("🐍", "ثعبان"),
            ("🦖", "ديناصور"),
        ],
    },
    "sea": {
        "name": "🌊 عالم البحر",
        "items": [
            ("🐟", "سمكة"),
            ("🐠", "سمكة ملونة"),
            ("🐡", "سمكة منتفخة"),
            ("🦈", "قرش"),
            ("🐬", "دولفين"),
            ("🐳", "حوت"),
            ("🐙", "أخطبوط"),
            ("🦀", "سلطعون"),
            ("🦐", "روبيان"),
            ("🐚", "صدفة"),
            ("🌊", "موجة"),
        ],
    },
    "food": {
        "name": "🍎 الفواكه والطعام",
        "items": [
            ("🍎", "تفاحة"),
            ("🍐", "كمثرى"),
            ("🍊", "برتقالة"),
            ("🍋", "ليمونة"),
            ("🍌", "موزة"),
            ("🍉", "بطيخ"),
            ("🍇", "عنب"),
            ("🍓", "فراولة"),
            ("🍒", "كرز"),
            ("🍑", "خوخ"),
            ("🥭", "مانجو"),
            ("🍍", "أناناس"),
            ("🥝", "كيوي"),
            ("🥕", "جزرة"),
            ("🌽", "ذرة"),
            ("🥦", "بروكلي"),
            ("🍅", "طماطم"),
            ("🥒", "خيار"),
            ("🍕", "بيتزا"),
            ("🍰", "كعكة"),
            ("🍦", "مثلجات"),
        ],
    },
    "vehicles": {
        "name": "🚗 المركبات",
        "items": [
            ("🚗", "سيارة"),
            ("🚕", "تاكسي"),
            ("🚌", "حافلة"),
            ("🚓", "سيارة شرطة"),
            ("🚑", "سيارة إسعاف"),
            ("🚒", "سيارة إطفاء"),
            ("🚜", "جرار"),
            ("🚲", "دراجة"),
            ("🛴", "سكوتر"),
            ("✈️", "طائرة"),
            ("🚁", "طائرة مروحية"),
            ("🚀", "صاروخ"),
            ("🚢", "سفينة"),
            ("🚂", "قطار"),
        ],
    },
    "school": {
        "name": "📚 المدرسة والأدوات",
        "items": [
            ("✏️", "قلم رصاص"),
            ("🖊️", "قلم"),
            ("📕", "كتاب"),
            ("📗", "دفتر"),
            ("📚", "كتب"),
            ("📏", "مسطرة"),
            ("✂️", "مقص"),
            ("🎒", "حقيبة"),
            ("🖍️", "ألوان"),
            ("🖌️", "فرشاة"),
            ("🧮", "عداد"),
            ("🔍", "عدسة"),
            ("📐", "مثلث هندسي"),
        ],
    },
    "toys": {
        "name": "🧸 الألعاب",
        "items": [
            ("🧸", "دبدوب"),
            ("⚽", "كرة"),
            ("🏀", "كرة سلة"),
            ("🏈", "كرة قدم أمريكية"),
            ("🎾", "كرة تنس"),
            ("🪁", "طائرة ورقية"),
            ("🎈", "بالون"),
            ("🎁", "هدية"),
            ("🎲", "نرد"),
            ("🪀", "يويو"),
            ("🧩", "أحجية"),
        ],
    },
    "space": {
        "name": "🚀 الفضاء",
        "items": [
            ("🚀", "صاروخ"),
            ("👨‍🚀", "رائد فضاء"),
            ("🌍", "الأرض"),
            ("🌎", "الأرض"),
            ("🌕", "القمر"),
            ("⭐", "نجمة"),
            ("🌟", "نجمة لامعة"),
            ("☄️", "مذنب"),
            ("🪐", "كوكب"),
            ("🌌", "الفضاء"),
        ],
    },
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
# HTML
# =========================================================

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>عالم أطفال ليليان وريناد ومحمد</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Tahoma, Arial, sans-serif;
    background:
        linear-gradient(135deg,#fff4b8,#c8f7ff,#e3d0ff);
    min-height: 100vh;
    color: #333;
}

header {
    text-align: center;
    padding: 25px 12px;
}

.logo {
    font-size: 65px;
}

h1 {
    font-size: 31px;
    margin: 5px;
    color: #6a1b9a;
}

header p {
    font-size: 18px;
}

.container {
    width: 95%;
    max-width: 1100px;
    margin: auto;
    padding-bottom: 40px;
}

.top {
    background: white;
    border-radius: 25px;
    padding: 15px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    box-shadow: 0 6px 20px rgba(0,0,0,.12);
}

.stars {
    background: #fff0a0;
    border-radius: 20px;
    padding: 8px 15px;
    font-weight: bold;
}

.menu {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 15px;
}

.card {
    border: 0;
    background: white;
    border-radius: 25px;
    min-height: 145px;
    padding: 18px;
    font-size: 19px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(0,0,0,.12);
    transition: .2s;
}

.card:hover {
    transform: translateY(-4px);
}

.card span {
    display: block;
    font-size: 52px;
    margin-bottom: 8px;
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

.title {
    text-align: center;
    font-size: 29px;
    margin: 15px;
    color: #6a1b9a;
}

.center {
    text-align: center;
}

.back {
    border: 0;
    padding: 12px 20px;
    border-radius: 15px;
    cursor: pointer;
    background: #eee;
}

button {
    border: 0;
    border-radius: 16px;
    padding: 12px 18px;
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

.items {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 12px;
}

.item {
    background: #fffaf0;
    border: 2px solid #eee;
    border-radius: 20px;
    padding: 12px;
    cursor: pointer;
    min-height: 130px;
}

.item .emoji {
    font-size: 58px;
    display: block;
}

.item strong {
    font-size: 16px;
}

#canvas {
    width: 100%;
    max-width: 900px;
    height: 500px;
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
    gap: 9px;
    margin: 15px;
}

.color {
    width: 43px;
    height: 43px;
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 2px 7px rgba(0,0,0,.25);
    cursor: pointer;
}

.big {
    font-size: 110px;
    line-height: 1.4;
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
    max-width: 600px;
    margin: 20px auto;
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 6px;
}

.piece {
    aspect-ratio: 1;
    background: #f4f4f4;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 55px;
    cursor: grab;
    user-select: none;
}

.missing-box {
    max-width: 550px;
    margin: 20px auto;
    padding: 25px;
    border-radius: 25px;
    background: #f5fbff;
    text-align: center;
}

.missing-picture {
    font-size: 90px;
}

@media(max-width:800px) {

    .menu {
        grid-template-columns: repeat(2,1fr);
    }

    .items {
        grid-template-columns: repeat(2,1fr);
    }

}

@media(max-width:500px) {

    .menu {
        grid-template-columns: repeat(2,1fr);
    }

    .card {
        font-size: 15px;
        min-height: 120px;
    }

    .card span {
        font-size: 40px;
    }

    .items {
        grid-template-columns: repeat(2,1fr);
    }

    #canvas {
        height: 380px;
    }

}

</style>
</head>

<body>

<header>

<div class="logo">🎨🌈</div>

<h1>عالم أطفال ليليان وريناد ومحمد</h1>

<p>
✨ نرسم ونلوّن ونتعلم ونلعب ✨
</p>

</header>

<div class="container">

<div class="top">

<div>
👋 أهلاً يا أبطال!
</div>

<div class="stars">
⭐ <span id="stars">0</span>
</div>

</div>

<div id="home">

<div class="menu">

<button class="card" onclick="drawing()">
<span>🖍️</span>
الرسم الحر
</button>

<button class="card" onclick="category('trees')">
<span>🌳</span>
الأشجار والطبيعة
</button>

<button class="card" onclick="category('animals')">
<span>🐶</span>
الحيوانات
</button>

<button class="card" onclick="category('sea')">
<span>🐠</span>
عالم البحر
</button>

<button class="card" onclick="category('food')">
<span>🍎</span>
الفواكه والطعام
</button>

<button class="card" onclick="category('vehicles')">
<span>🚗</span>
المركبات
</button>

<button class="card" onclick="category('school')">
<span>📚</span>
المدرسة والأدوات
</button>

<button class="card" onclick="category('toys')">
<span>🧸</span>
الألعاب
</button>

<button class="card" onclick="category('space')">
<span>🚀</span>
الفضاء
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
🔙 الرئيسية
</button>

<div id="content"></div>

</div>

</div>


<script>

let stars = Number(
    localStorage.getItem("kids_stars") || 0
);

function updateStars() {
    document.getElementById("stars").textContent = stars;
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


// ========================================================
// التصنيفات
// ========================================================

const data = {
trees: [
["🌳","شجرة"],
["🌲","صنوبر"],
["🌴","نخلة"],
["🌵","صبار"],
["🌻","زهرة"],
["🌷","زهرة"],
["🌹","وردة"],
["🌱","نبتة"],
["🍀","برسيم"],
["🌈","قوس قزح"],
["☀️","الشمس"],
["☁️","السحابة"],
["🌙","القمر"],
["⭐","نجمة"]
],

animals: [
["🐶","كلب"],
["🐱","قطة"],
["🐭","فأر"],
["🐰","أرنب"],
["🦊","ثعلب"],
["🐻","دب"],
["🐼","باندا"],
["🐨","كوالا"],
["🐯","نمر"],
["🦁","أسد"],
["🐮","بقرة"],
["🐷","حيوان"],
["🐸","ضفدع"],
["🐵","قرد"],
["🐔","دجاجة"],
["🐧","بطريق"],
["🐦","عصفور"],
["🦋","فراشة"],
["🐝","نحلة"],
["🐢","سلحفاة"],
["🐍","ثعبان"],
["🦖","ديناصور"]
],

sea: [
["🐟","سمكة"],
["🐠","سمكة ملونة"],
["🐡","سمكة"],
["🦈","قرش"],
["🐬","دولفين"],
["🐳","حوت"],
["🐙","أخطبوط"],
["🦀","سلطعون"],
["🦐","روبيان"],
["🐚","صدفة"],
["🌊","موجة"]
],

food: [
["🍎","تفاحة"],
["🍐","كمثرى"],
["🍊","برتقالة"],
["🍋","ليمونة"],
["🍌","موز"],
["🍉","بطيخ"],
["🍇","عنب"],
["🍓","فراولة"],
["🍒","كرز"],
["🍑","خوخ"],
["🥭","مانجو"],
["🍍","أناناس"],
["🥝","كيوي"],
["🥕","جزرة"],
["🌽","ذرة"],
["🥦","بروكلي"],
["🍅","طماطم"],
["🥒","خيار"],
["🍕","بيتزا"],
["🍰","كعكة"],
["🍦","مثلجات"]
],

vehicles: [
["🚗","سيارة"],
["🚕","تاكسي"],
["🚌","حافلة"],
["🚓","شرطة"],
["🚑","إسعاف"],
["🚒","إطفاء"],
["🚜","جرار"],
["🚲","دراجة"],
["🛴","سكوتر"],
["✈️","طائرة"],
["🚁","مروحية"],
["🚀","صاروخ"],
["🚢","سفينة"],
["🚂","قطار"]
],

school: [
["✏️","قلم رصاص"],
["🖊️","قلم"],
["📕","كتاب"],
["📗","دفتر"],
["📚","كتب"],
["📏","مسطرة"],
["✂️","مقص"],
["🎒","حقيبة"],
["🖍️","ألوان"],
["🖌️","فرشاة"],
["🧮","عداد"],
["🔍","عدسة"],
["📐","مثلث"]
],

toys: [
["🧸","دبدوب"],
["⚽","كرة"],
["🏀","كرة سلة"],
["🏈","كرة"],
["🎾","تنس"],
["🪁","طائرة ورقية"],
["🎈","بالون"],
["🎁","هدية"],
["🎲","نرد"],
["🪀","يويو"],
["🧩","أحجية"]
],

space: [
["🚀","صاروخ"],
["👨‍🚀","رائد فضاء"],
["🌍","الأرض"],
["🌕","القمر"],
["⭐","نجمة"],
["🌟","نجمة"],
["☄️","مذنب"],
["🪐","كوكب"],
["🌌","الفضاء"]
]
};


function category(type) {

    const names = {
        trees:"🌳 الأشجار والطبيعة",
        animals:"🐾 الحيوانات",
        sea:"🌊 عالم البحر",
        food:"🍎 الفواكه والطعام",
        vehicles:"🚗 المركبات",
        school:"📚 المدرسة والأدوات",
        toys:"🧸 الألعاب",
        space:"🚀 الفضاء"
    };

    let cards = "";

    data[type].forEach(function(item) {

        cards += `
        <button
            class="item"
            onclick="drawPicture('${item[0]}','${item[1]}')">

            <span class="emoji">
                ${item[0]}
            </span>

            <strong>
                ${item[1]}
            </strong>

        </button>
        `;

    });

    show(`

        <div class="title">
            ${names[type]}
        </div>

        <p class="center">
            اختاروا صورة ثم ابدأوا التلوين 🎨
        </p>

        <div class="items">
            ${cards}
        </div>

    `);
}


// ========================================================
// تلوين صورة
// ========================================================

function drawPicture(symbol, name) {

    show(`

        <div class="title">
            🎨 تلوين ${name}
        </div>

        <div class="center">

            <div
                style="
                font-size:170px;
                padding:20px;
                border:5px dashed #ddd;
                border-radius:30px;
                margin:20px;
                ">
                ${symbol}
            </div>

            <h2>
                ${name}
            </h2>

            <button
                class="green"
                onclick="drawing()">
                🖍️ لوّن الصورة
            </button>

            <button
                class="blue"
                onclick="addStars(5); alert('⭐ أحسنت! حصلت على 5 نجوم')">
                ⭐ أنجزت
            </button>

        </div>

    `);
}


// ========================================================
// الرسم الحر
// ========================================================

let canvas;
let ctx;
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

            <div class="color"
            style="background:#ff0000"
            onclick="setColor('#ff0000')"></div>

            <div class="color"
            style="background:#ff7f00"
            onclick="setColor('#ff7f00')"></div>

            <div class="color"
            style="background:#ffff00"
            onclick="setColor('#ffff00')"></div>

            <div class="color"
            style="background:#00a000"
            onclick="setColor('#00a000')"></div>

            <div class="color"
            style="background:#00bfff"
            onclick="setColor('#00bfff')"></div>

            <div class="color"
            style="background:#0000ff"
            onclick="setColor('#0000ff')"></div>

            <div class="color"
            style="background:#800080"
            onclick="setColor('#800080')"></div>

            <div class="color"
            style="background:#ff69b4"
            onclick="setColor('#ff69b4')"></div>

            <div class="color"
            style="background:#8b4513"
            onclick="setColor('#8b4513')"></div>

            <div class="color"
            style="background:#000000"
            onclick="setColor('#000000')"></div>

        </div>

        <div class="center">

            <button onclick="setBrush(5)">
                🖊️ صغير
            </button>

            <button onclick="setBrush(15)">
                🖌️ متوسط
            </button>

            <button onclick="setBrush(30)">
                🖍️ كبير
            </button>

            <button onclick="clearCanvas()">
                🗑️ مسح
            </button>

            <button
                class="blue"
                onclick="saveDrawing()">
                💾 حفظ
            </button>

            <button
                class="green"
                onclick="finishDrawing()">
                ⭐ انتهيت
            </button>

        </div>

    `);

    canvas =
        document.getElementById("canvas");

    ctx =
        canvas.getContext("2d");

    ctx.fillStyle = "#ffffff";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    canvas.addEventListener(
        "pointerdown",
        startDraw
    );

    canvas.addEventListener(
        "pointermove",
        drawLine
    );

    canvas.addEventListener(
        "pointerup",
        stopDraw
    );

    canvas.addEventListener(
        "pointercancel",
        stopDraw
    );
}


function position(event) {

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


function startDraw(event) {

    drawingNow = true;

    const p = position(event);

    ctx.beginPath();

    ctx.moveTo(
        p.x,
        p.y
    );
}


function drawLine(event) {

    if (!drawingNow) {
        return;
    }

    const p = position(event);

    ctx.lineWidth = brush;

    ctx.lineCap = "round";

    ctx.strokeStyle =
        currentColor;

    ctx.lineTo(
        p.x,
        p.y
    );

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(
        p.x,
        p.y
    );
}


function stopDraw() {
    drawingNow = false;
}


function setColor(color) {
    currentColor = color;
}


function setBrush(size) {
    brush = size;
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
        "lilian-renad-mohammed-drawing.png";

    link.href =
        canvas.toDataURL("image/png");

    link.click();
}


function finishDrawing() {

    addStars(5);

    alert(
        "🎉 أحسنتم!\n⭐ حصلتم على 5 نجوم"
    );
}


// ========================================================
// الحروف
// ========================================================

let letterIndex = 0;


function letters() {

    letterIndex = 0;

    showLetter();
}


function showLetter() {

    const item =
        LETTERS[letterIndex];

    show(`

        <div class="title">
            🔤 الحروف العربية
        </div>

        <div class="letter">
            ${item[0]}
        </div>

        <div class="center">

            <h2>
                ${item[1]}
            </h2>

            <button
                class="blue"
                onclick="nextLetter()">
                ➡️ التالي
            </button>

            <button
                class="green"
                onclick="addStars(5); alert('⭐ أحسنت!')">
                ⭐ تعلمت
            </button>

        </div>

    `);
}


function nextLetter() {

    letterIndex++;

    if (
        letterIndex >=
        LETTERS.length
    ) {

        letterIndex = 0;

        addStars(20);

        alert(
            "🎉 أحسنتم! أكملتم الحروف!"
        );
    }

    showLetter();
}


// ========================================================
// الأرقام
// ========================================================

let numberIndex = 0;


function numbers() {

    numberIndex = 0;

    showNumber();
}


function showNumber() {

    const item =
        NUMBERS[numberIndex];

    show(`

        <div class="title">
            🔢 الأرقام
        </div>

        <div class="number">
            ${item[0]}
        </div>

        <div class="center">

            <h2>
                ${item[1]}
            </h2>

            <button
                class="blue"
                onclick="nextNumber()">
                ➡️ التالي
            </button>

            <button
                class="green"
                onclick="addStars(5); alert('⭐ أحسنت!')">
                ⭐ تعلمت
            </button>

        </div>

    `);
}


function nextNumber() {

    numberIndex++;

    if (
        numberIndex >=
        NUMBERS.length
    ) {

        numberIndex = 0;

        addStars(20);

        alert(
            "🎉 أحسنتم! أكملتم الأرقام!"
        );
    }

    showNumber();
}


// ========================================================
// أكمل الصورة
// ========================================================

const missingQuestions = [

    {
        picture: "🐶 ?",
        question: "ما الذي يكمل الصورة؟",
        answers: [
            ["🐶","صحيح"],
            ["🍎","خطأ"],
            ["🚗","خطأ"]
        ]
    },

    {
        picture: "🌳 ?",
        question: "ماذا يناسب الشجرة؟",
        answers: [
            ["🌱","صحيح"],
            ["🚀","خطأ"],
            ["🐟","خطأ"]
        ]
    },

    {
        picture: "🐟 ?",
        question: "أين تعيش السمكة؟",
        answers: [
            ["🌊","صحيح"],
            ["☀️","خطأ"],
            ["🚗","خطأ"]
        ]
    },

    {
        picture: "🚗 ?",
        question: "ما الذي يناسب السيارة؟",
        answers: [
            ["🛣️","صحيح"],
            ["🐠","خطأ"],
            ["🌳","خطأ"]
        ]
    }

];

let missingIndex = 0;


function missing() {

    missingIndex = 0;

    showMissing();
}


function showMissing() {

    const q =
        missingQuestions[
            missingIndex
        ];

    let answers = "";

    q.answers.forEach(
        function(answer) {

            answers += `

                <button
                    style="font-size:50px"
                    onclick="
                    missingAnswer('${answer[1]}')">
                    ${answer[0]}
                </button>

            `;

        }
    );

    show(`

        <div class="title">
            🧩 أكمل الصورة
        </div>

        <div class="missing-box">

            <div class="missing-picture">
                ${q.picture}
            </div>

            <h2>
                ${q.question}
            </h2>

            ${answers}

        </div>

    `);
}


function missingAnswer(result) {

    if (result === "صحيح") {

        addStars(10);

        alert(
            "🎉 إجابة صحيحة!\n⭐ +10"
        );

        missingIndex++;

        if (
            missingIndex >=
            missingQuestions.length
        ) {

            missingIndex = 0;

            addStars(20);

            alert(
                "🏆 رائع! أكملتم جميع التحديات!"
            );
        }

        showMissing();

    } else {

        alert(
            "😊 حاولوا مرة أخرى"
        );
    }
}


// ========================================================
// إعادة تركيب الصورة
// ========================================================

const puzzleData = [
    "🌳",
    "☀️",
    "🐦",
    "🌸",
    "🏠",
    "🌱",
    "🦋",
    "☁️",
    "🌈"
];


function puzzle() {

    show(`

        <div class="title">
            🔀 إعادة تركيب الصورة
        </div>

        <p class="center">
            اسحب القطع ورتبها ثم اضغط تحقق.
        </p>

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

    puzzleData.forEach(
        function(item,index) {

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

            box.appendChild(
                piece
            );
        }
    );

    enablePuzzle();
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


function enablePuzzle() {

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
                dragged === target
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
        function(piece,index) {

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
            "🏆 ممتاز!\n" +
            "أكملتم تركيب الصورة!\n" +
            "⭐ +15"
        );

    } else {

        alert(
            "😊 حاولوا ترتيب القطع مرة أخرى."
        );
    }
}

</script>

</body>
</html>
"""


# =========================================================
# Web Server
# =========================================================

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
        f"Web server started on port {port}"
    )


# =========================================================
# Telegram
# =========================================================

def get_public_url():

    domain = os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN"
    )

    if not domain:
        return None

    domain = domain.strip()

    if domain.startswith("http://"):
        return domain

    if domain.startswith("https://"):
        return domain

    return "https://" + domain


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [

        [
            InlineKeyboardButton(
                "🎨 عالم أطفال ليليان وريناد ومحمد",
                callback_data="open_kids"
            )
        ],

        [
            InlineKeyboardButton(
                "🖍️ الرسم والتلوين",
                callback_data="drawing"
            ),
            InlineKeyboardButton(
                "🔤 الحروف",
                callback_data="letters"
            )
        ],

        [
            InlineKeyboardButton(
                "🔢 الأرقام",
                callback_data="numbers"
            ),
            InlineKeyboardButton(
                "🧩 الألعاب",
                callback_data="games"
            )
        ]

    ]

    await update.message.reply_text(

        "🌟 أهلاً بكم في عالم أطفال "
        "ليليان وريناد ومحمد! 🌈🎨\n\n"

        "🖍️ ارسموا ولوّنوا\n"
        "🌳 اكتشفوا الطبيعة\n"
        "🐾 تعرفوا على الحيوانات\n"
        "🍎 الفواكه والطعام\n"
        "🚗 المركبات\n"
        "🚀 الفضاء\n"
        "📚 المدرسة والأدوات\n"
        "🔤 تعلموا الحروف\n"
        "🔢 تعلموا الأرقام\n"
        "🧩 أكملوا الصور\n"
        "🔀 أعيدوا تركيب الصور\n\n"

        "✨ هيا نلعب ونتعلم ونبدع!\n\n"
        "اختاروا نشاطاً:",

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    url = get_public_url()

    if not url:

        await query.edit_message_text(

            "⚠️ لم يتم العثور على Public Domain.\n\n"

            "اذهب إلى Railway → Settings → "
            "Networking → Generate Domain.\n\n"

            "ثم أعد تشغيل الخدمة."

        )

        return


    if query.data == "open_kids":

        keyboard = [[

            InlineKeyboardButton(
                "🎨 افتح عالم أطفال ليليان وريناد ومحمد",
                url=url + "/kids"
            )

        ]]

        await query.edit_message_text(

            "🌈 مرحباً بكم في عالم أطفال "
            "ليليان وريناد ومحمد!\n\n"

            "🎨 الرسم والتلوين\n"
            "🐾 الحيوانات\n"
            "🌳 الطبيعة\n"
            "🍎 الطعام\n"
            "🚗 المركبات\n"
            "🚀 الفضاء\n"
            "🔤 الحروف\n"
            "🔢 الأرقام\n"
            "🧩 الألعاب\n\n"

            "اضغطوا على الزر للدخول:",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return


    if query.data == "drawing":

        keyboard = [[

            InlineKeyboardButton(
                "🖍️ ابدأ الرسم والتلوين",
                url=url + "/kids"
            )

        ]]

        await query.edit_message_text(

            "🖍️ حان وقت الإبداع!\n\n"
            "افتحوا عالم الأطفال وابدأوا الرسم.",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return


    if query.data == "letters":

        keyboard = [[

            InlineKeyboardButton(
                "🔤 تعلم الحروف",
                url=url + "/kids"
            )

        ]]

        await query.edit_message_text(

            "🔤 هيا نتعلم الحروف العربية!",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return


    if query.data == "numbers":

        keyboard = [[

            InlineKeyboardButton(
                "🔢 تعلم الأرقام",
                url=url + "/kids"
            )

        ]]

        await query.edit_message_text(

            "🔢 هيا نتعلم الأرقام!",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return


    if query.data == "games":

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


# =========================================================
# Main
# =========================================================

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
        "🌈 عالم أطفال ليليان وريناد ومحمد يعمل الآن"
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
