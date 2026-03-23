import time
import datetime
import requests
import schedule
import socket
import random
import feedparser
import os
import json
import threading
from flask import Flask

# 🔥 SERVIDOR PARA RENDER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def iniciar_web():
    t = threading.Thread(target=run_web)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = os.getenv("CANAL_ID")

if not BOT_TOKEN or not CANAL_ID:
    raise ValueError("❌ Falta BOT_TOKEN o CANAL_ID en variables de entorno")

CANAL_ID = int(CANAL_ID)

# --- TIMEZONE (🔥 CLAVE) ---
def hora_bolivia():
    return datetime.datetime.utcnow() - datetime.timedelta(hours=4)

# --- LINK FIJO DEL VIDEO ---
VIDEO_LINK = "https://youtu.be/F67qG_uoX4s"

# --- RSS YOUTUBE ---
YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCfzQjeCdi4cK_WREJJvwzoQ"

# --- ARCHIVO DE CONTROL ---
ARCHIVO_ESTADO = "estado_youtube.json"

def cargar_estado():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, "r") as f:
            return json.load(f)
    return {"ultimo": None, "fecha": ""}

def guardar_estado(data):
    with open(ARCHIVO_ESTADO, "w") as f:
        json.dump(data, f)

estado = cargar_estado()

# --- MENSAJES ---
mensajes_semana = {
    "08:00": """😃 ¡Buenos días! 👌

Empezamos operaciones

Puedes abrir tu cuenta para recibir las operaciones 👏

Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial)

Comenzamos! 🦾😎 💰💰""",

    "09:00": """🤩 Recuerda, el servicio de CopyTrade es GRATUITO 

Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial)

Ganancias de 5 a 17usd diarios

Escríbenos para habilitar tu cuenta y recibirás las operaciones todos los días en automático 🔥

¿Qué esperas...?🤓""",

    "10:00": """❗️ No pierdas la oportunidad de unirte a nuestros clientes que cada día disfrutan de ganancias consistentes de forma GRATUITA 😱

Nuestro Sistema Automatizado IA 🤖 se encarga de todo, analizando constantemente el mercado y realizando operaciones estratégicas.

¡Es hora de dar un paso hacia un futuro financiero, la Inteligencia Artificial! 🦾😎

⚙️ Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial)""",

    "11:00": """🤑 NUESTROS UNICOS PLANES

1️⃣ Depósito 50usd 
Ganancia diaria = 5 a 7usd ✅
2️⃣ Depósito 75usd 
Ganancia diaria = 7 a 10usd ✅
3️⃣ Depósito 100usd 
Ganancia diaria = 10 a 13usd ✅
4️⃣ Depósito 125usd 
Ganancia diaria = 13 a 15usd ✅
5️⃣ Depósito 150usd 
Ganancia diaria = 15 a 17usd ✅

💰 Si deseas operar Capitales más altos puedes ingresar al Fondo De Inversiones FDI con el 50% de Ganancia FIJA cada 5 dias! 👉https://t.me/inversioneess

Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial) 

HOY puedes recibir tus primeras ganancias ¿Qué esperas?🤓
""",

    "12:00": """💰 Utiliza el Código BQI667 al hacer tu Primer Depósito y obtén un Bono del 60% de tu capital. 🎁

Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial)

🟢 ¡Cuando haga su primer depósito escriba 👉 BQI667 y obtenga el 60% Gratis❗️""",

    "13:00": """También puedes utilizar el Copy Trade en tu cuenta personal SIN TENER QUE ABRIR UNA NUEVA CUENTA CON NOSOTROS 🙏

Gracias❗️ a los usuarios que están utilizando el #Servicio #Externo de #CopyTrade

Info Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial)""",

    "14:00_VIDEO": """🤖 Conector de señales Bot 

🔥 Este Robot IA copia las señales que se envían en CUALQUIER GRUPO O CANAL de Telegram y se ABREN Automáticamente en tu cuenta sin que tengas que hacer NADA, Automáticamente en mercado Normal y OTC 

UN SOLO PAGO SIN MENSUALIDADES 
Esto es Oro 🥇

¡¡Con el Conector de Señales NO pierdes ninguna señal enviada de tu grupo favorito!! 

😎 Funciona en Cualquier Broker en cuentas Demo y Real

Escríbeme ➡️ [🚀 Nano Bots](https://t.me/NanoMillenial)"""
}

mensajes_fin_semana = {
    "09:00": """¡Buenos días para todos! 😎

Hoy las operaciones con el robot del Copy Trade #No se realizan ya que #solo se opera de lunes a viernes

El robot de Fondo de Inversion #FDI #Si está operando normalmente por que #funciona los 7 dias de la semana

Mientras estamos disfrutando de nuestro Fin de Semana los Bots siguen operando en automático, enviando los pagos sin problemas

#Gracias a todos los usuarios que se van sumando a nuestros Bots

#NanoBots""",

    "12:00_VIDEO": mensajes_semana["14:00_VIDEO"]
}

# --- FUNCIONES ---
def internet_disponible():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

def enviar_mensaje(texto):
    while not internet_disponible():
        print("❌ Sin internet...", flush=True)
        time.sleep(10)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={
        "chat_id": CANAL_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    })

    print(f"📤 Mensaje enviado: {r.status_code}", flush=True)

def enviar_video(_, caption):
    mensaje = f"""{caption}

📺 Ver aquí 👉 {VIDEO_LINK}
"""
    enviar_mensaje(mensaje)

# --- YOUTUBE ---
def obtener_video_youtube():
    feed = feedparser.parse(YOUTUBE_RSS)
    if not feed.entries:
        return None
    videos = feed.entries[:15]
    video = random.choice(videos)
    return video.title, video.link

def publicar_video_youtube():
    global estado

    hoy = hora_bolivia().date().isoformat()

    if estado["fecha"] == hoy:
        print("⚠️ Ya se publicó hoy", flush=True)
        return

    for _ in range(5):
        data = obtener_video_youtube()
        if not data:
            return

        titulo, link = data

        if link != estado["ultimo"]:
            estado["ultimo"] = link
            estado["fecha"] = hoy
            guardar_estado(estado)

            mensaje = f"""🎬 {titulo}

📺 Ver aquí 👉 {link}
"""
            enviar_mensaje(mensaje)
            print("✅ YouTube publicado", flush=True)
            return

# --- TAREAS ---
def tarea_programada(hora):
    ahora = hora_bolivia()
    hoy = ahora.weekday()
    hora_actual = ahora.strftime("%H:%M")

    es_semana = hoy < 5
    mensajes = mensajes_semana if es_semana else mensajes_fin_semana

    key = f"{hora}_VIDEO" if f"{hora}_VIDEO" in mensajes else hora

    if hora == hora_actual and key in mensajes:
        print(f"⏰ Ejecutando {hora} (hora Bolivia)", flush=True)

        if "VIDEO" in key:
            enviar_video(None, mensajes[key])
        else:
            enviar_mensaje(mensajes[key])

def tarea_youtube_controlada():
    ahora = hora_bolivia()
    hoy = ahora.weekday()

    if hoy < 5 and ahora.hour == 16 and ahora.minute == 0:
        publicar_video_youtube()

    elif hoy >= 5 and ahora.hour == 14 and ahora.minute == 0:
        publicar_video_youtube()

# --- SCHEDULE (SE MANTIENE IGUAL) ---
horarios = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00"]

for h in horarios:
    schedule.every().minute.do(tarea_programada, h)

schedule.every().minute.do(tarea_youtube_controlada)

print("🤖 Bot activo en Render (AUTO TIMEZONE)", flush=True)

# 🔥 INICIAR SERVIDOR
iniciar_web()

# --- LOOP ---
while True:
    schedule.run_pending()
    time.sleep(5)
