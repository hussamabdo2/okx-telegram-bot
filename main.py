import os
import random
import io
from aiohttp import web
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


BOT_TOKEN = os.environ["BOT_TOKEN"]


# ============================================================
# 🎨 صفحة الأطفال
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,initial-scale=1.0">

<title>🎨 عالم الأطفال</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Tahoma, sans-serif;
    background: linear-gradient(135deg,#fff4b8,#c9f5ff);
    min-height: 100vh;
    color: #333;
}

header {
    text-align: center;
    padding: 25px 10px;
}

header .logo {
    font-size: 60px;
}

header h1 {
    margin: 5px;
    font-size: 32px;
}

header p {
    margin: 5px;
}

.container {
    max-width: 950px;
    margin: auto;
    padding: 15px;
}

.top {
    background: white;
    padding: 15px 20px;
    border-radius: 25px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 5px 18px rgba(0,0,0,.12);
}

.stars {
    background: #fff0a0;
    border-radius: 20px;
    padding: 8px 15px;
}

.menu {
    display: grid;
    grid-template-columns: repeat(2,1fr);
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
    touch-action: none;
    display: block;
    margin: auto;
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
    grid-template-columns: repeat(3,1fr);
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
}

@media(max-width:600px) {

    .menu {
        grid-template-columns: repeat(2,1fr);
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

<div>👋 مرحباً يا بطل!</div>

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

let stars =
Number(localStorage.getItem("kids_stars") || 0);

function updateStars() {
    document.getElementById("stars").textContent = stars;
}

function addStars(n) {
    stars += n;
    localStorage.setItem("kids_stars",stars);
    updateStars();
}

updateStars();


function home() {

    document.getElementById("home").style.display = "block";

    document.getElementById("page")
        .classList.remove("active");
}


function show(html) {

    document.getElementById("home").style.display = "none";

    document.getElementById("page")
        .classList.add("active");

    document.getElementById("content")
        .innerHTML = html;
}


// ============================================================
// 🖍️ الرسم
// ============================================================

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
style="background:red"
onclick="color('#ff0000')"></div>

<div class="color"
style="background:orange"
onclick="color('#ff9800')"></div>

<div class="color"
style="background:yellow"
onclick="color('#ffeb3b')"></div>

<div class="color"
style="background:green"
onclick="color('#4caf50')"></div>

<div class="color"
style="background:blue"
onclick="color('#2196f3')"></div>

<div class="color"
style="background:purple"
onclick="color('#9c27b0')"></div>

<div class="color"
style="background:pink"
onclick="color('#e91e63')"></div>

<div class="color"
style="background:black"
onclick="color('#000000')"></div>

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

<button class="blue"
onclick="save()">
💾 حفظ
</button>

<button class="green"
onclick="finish()">
⭐ انتهيت
</button>

</div>

`);

canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");

ctx.fillStyle = "white";
ctx.fillRect(0,0,canvas.width,canvas.height);

canvas.addEventListener("pointerdown",start);
canvas.addEventListener("pointermove",drawLine);
canvas.addEventListener("pointerup",stop);
canvas.addEventListener("pointercancel",stop);
}


function pos(e) {

const r = canvas.getBoundingClientRect();

return {
x:(e.clientX-r.left)*canvas.width/r.width,
y:(e.clientY-r.top)*canvas.height/r.height
};

}


function start(e) {

drawingNow = true;

const p = pos(e);

ctx.beginPath();

ctx.moveTo(p.x,p.y);
}


function drawLine(e) {

if(!drawingNow) return;

const p = pos(e);

ctx.lineWidth = brush;
ctx.lineCap = "round";
ctx.strokeStyle = currentColor;

ctx.lineTo(p.x,p.y);
ctx.stroke();

ctx.beginPath();
ctx.moveTo(p.x,p.y);
}


function stop() {
drawingNow = false;
}


function color(c) {
currentColor = c;
}


function brushSize(n) {
brush = n;
}


function clearCanvas() {

ctx.fillStyle = "white";

ctx.fillRect(
0,
0,
canvas.width,
canvas.height
);

}


function save() {

const a = document.createElement("a");

a.download = "kids-drawing.png";

a.href = canvas.toDataURL("image/png");

a.click();

}


function finish() {

addStars(5);

alert("🎉 أحسنت!\n⭐ حصلت على 5 نجوم");

}


// ============================================================
// 🌳 🐶 🧰
 // ============================================================

function category(type) {

let title;
let emojis;

if(type === "nature") {

title = "🌳 الطبيعة";

emojis = "🌳 🌸 🌺 ☀️ 🌈 ☁️";

}

if(type === "animals") {

title = "🐶 الحيوانات";

emojis = "🐶 🐱 🦁 🐘 🐰 🐼 🦋";

}

if(type === "objects") {

title = "🧰 الأدوات والأشياء";

emojis = "🚗 ✈️ 🏠 🎒 ✏️ ⚽ 🧸";

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
اختر الرسم وابدأ التلوين 🎨
</p>

<button class="green"
onclick="drawing()">
🖍️ ابدأ التلوين
</button>

</div>

`);

}


// ============================================================
// 🔤 الحروف
// ============================================================

const lettersData = [

["أ","أسد 🦁"],
["ب","بطة 🦆"],
["ت","تفاحة 🍎"],
["ث","ثعلب 🦊"],
["ج","جمل 🐪"],
["ح","حصان 🐴"],
["خ","خروف 🐑"],
["د","دجاجة 🐔"],
["ذ","ذئب 🐺"],
["ر","رمان 🍎"],
["ز","زرافة 🦒"],
["س","سمكة 🐟"],
["ش","شجرة 🌳"],
["ص","صقر 🦅"],
["ض","ضفدع 🐸"],
["ط","طائرة ✈️"],
["ظ","ظرف ✉️"],
["ع","عصفور 🐦"],
["غ","غزال 🦌"],
["ف","فيل 🐘"],
["ق","قمر 🌙"],
["ك","كتاب 📖"],
["ل","ليمون 🍋"],
["م","موز 🍌"],
["ن","نحلة 🐝"],
["هـ","هلال 🌙"],
["و","وردة 🌹"],
["ي","يد ✋"]

];

let letterIndex = 0;


function letters() {

letterIndex = 0;

showLetter();

}


function showLetter() {

const x = lettersData[letterIndex];

show(`

<div class="center">

<div class="title">
🔤 الحروف العربية
</div>

<div class="letter">
${x[0]}
</div>

<h2>
${x[1]}
</h2>

<button class="blue"
onclick="nextLetter()">
➡️ التالي
</button>

<button class="green"
onclick="addStars(5)">
⭐ تعلمت الحرف
</button>

</div>

`);

}


function nextLetter() {

letterIndex++;

if(letterIndex >= lettersData.length) {

letterIndex = 0;

addStars(20);

alert("🎉 أكملت الحروف!");

}

showLetter();

}


// ============================================================
// 🔢 الأرقام
// ============================================================

const numbersData = [
["٠","صفر"],
["١","واحد"],
["٢","اثنان"],
["٣","ثلاثة"],
["٤","أربعة"],
["٥","خمسة"],
["٦","ستة"],
["٧","سبعة"],
["٨","ثمانية"],
["٩","تسعة"],
["١٠","عشرة"]
];

let numberIndex = 0;


function numbers() {

numberIndex = 0;

showNumber();

}


function showNumber() {

const x = numbersData[numberIndex];

show(`

<div class="center">

<div class="title">
🔢 الأرقام
</div>

<div class="number">
${x[0]}
</div>

<h2>
${x[1]}
</h2>

<button class="blue"
onclick="nextNumber()">
➡️ التالي
</button>

<button class="green"
onclick="addStars(5)">
⭐ تعلمت الرقم
</button>

</div>

`);

}


function nextNumber() {

numberIndex++;

if(numberIndex >= numbersData.length) {

numberIndex = 0;

addStars(20);

alert("🎉 أكملت الأرقام!");

}

showNumber();

}


// ============================================================
// 🧩 أكمل الصورة
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
ما الجزء الناقص؟
</h2>

<button
style="font-size:40px"
onclick="correctMissing()">
🐈
</button>

<button
style="font-size:40px"
onclick="wrongMissing()">
👂
</button>

<button
style="font-size:40px"
onclick="wrongMissing()">
👁️
</button>

</div>

`);

}


function correctMissing() {

addStars(10);

alert("🎉 إجابة صحيحة!\n⭐ +10");

}


function wrongMissing() {

alert("😊 حاول مرة أخرى");

}


// ============================================================
// 🔀 إعادة تركيب الصورة
// ============================================================

const puzzleItems = [
"🌳","🍎","🐦",
"☀️","🌸","🦋",
"🌱","☁️","🏠"
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

<div id="puzzle"
class="puzzle">
</div>

<div class="center">

<button class="orange"
onclick="shuffle()">
🔀 خلط
</button>

<button class="green"
onclick="checkPuzzle()">
⭐ تحقق
</button>

</div>

`);

createPuzzle();

}


function createPuzzle() {

const box =
document.getElementById("puzzle");

box.innerHTML = "";

puzzleItems.forEach((x,i)=>{

const p =
document.createElement("div");

p.className = "piece";

p.textContent = x;

p.dataset.correct = i;

p.draggable = true;

box.appendChild(p);

});

dragPuzzle();

}


function shuffle() {

const box =
document.getElementById("puzzle");

const pieces =
Array.from(box.children);

pieces.sort(
()=>Math.random()-.5
);

pieces.forEach(
p=>box.appendChild(p)
);

}


function dragPuzzle() {

const box =
document.getElementById("puzzle");

let dragged = null;


box.addEventListener(
"dragstart",
e=>{
dragged=e.target;
}
);


box.addEventListener(
"dragover",
e=>{
e.preventDefault();
}
);


box.addEventListener(
"drop",
e=>{

e.preventDefault();

const target=e.target;

if(
target.classList.contains("piece")
&&
dragged
&&
target!==dragged
){

const all =
Array.from(box.children);

const a =
all.indexOf(dragged);

const b =
all.indexOf(target);

if(a<b){

box.insertBefore(
dragged,
target.nextSibling
);

}else{

box.insertBefore(
dragged,
target
);

}

}

}
);

}


function checkPuzzle() {

const box =
document.getElementById("puzzle");

const pieces =
Array.from(box.children);

let ok = true;

pieces.forEach((p,i)=>{

if(
Number(p.dataset.correct)!==i
){

ok=false;

}

});


if(ok){

addStars(15);

alert(
"🎉 ممتاز!\n"
+
"أكملت تركيب الصورة!\n"
+
"⭐ +15"
);

}else{

alert(
"😊 لم تكتمل الصورة بعد، حاول مرة أخرى."
);

}

}

</script>

</body>
</html>
"""


# ============================================================
# 🌐 Web Server
# ============================================================

async def kids_web(request):

    return web.Response(
        text=HTML,
        content_type="text/html",
        charset="utf-8",
    )


async def health(request):

    return web.Response(
        text="Kids Bot is running"
    )


# ============================================================
# 🤖 Telegram
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
                callback_data="draw"
            )
        ],

        [
            InlineKeyboardButton(
                "🧩 الألعاب التعليمية",
                callback_data="games"
            )
        ],

    ]

    await update.message.reply_text(
        "🌟 أهلاً بك في عالم الأطفال!\n\n"
        "اختر النشاط الذي تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    if query.data == "kids":

        url = get_public_url()

        keyboard = [[
            InlineKeyboardButton(
                "🎨 افتح عالم الأطفال",
                url=url + "/kids"
            )
        ]]

        await query.edit_message_text(
            "🎨 عالم الأطفال\n\n"
            "ارسم ولوّن وتعلم والعب! 🌈",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )


    elif query.data == "draw":

        url = get_public_url()

        await query.edit_message_text(
            "🖍️ الرسم والتلوين متاح داخل عالم الأطفال.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "🎨 افتح الرسم",
                    url=url + "/kids"
                )
            ]])
        )


    elif query.data == "games":

        url = get_public_url()

        await query.edit_message_text(
            "🧩 الألعاب التعليمية:\n\n"
            "🔤 الحروف\n"
            "🔢 الأرقام\n"
            "🧩 أكمل الصورة\n"
            "🔀 إعادة تركيب الصورة",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "🎮 ابدأ اللعب",
                    url=url + "/kids"
                )
            ]])
        )


# ============================================================
# 🔗 رابط Railway
# ============================================================

def get_public_url():

    domain = os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN"
    )

    if domain:

        if domain.startswith("http"):

            return domain

        return "https://" + domain


    return "https://YOUR-RAILWAY-DOMAIN"


# ============================================================
# 🚀 تشغيل
# ============================================================

async def run_web():

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
        kids_web
    )

    runner =
        web.AppRunner(app)

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
        f"Kids web server running on port {port}"
    )


async def main():

    await run_web()

    application =
        Application.builder().token(
            BOT_TOKEN
        ).build()


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

    import asyncio

    asyncio.run(main())
