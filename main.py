import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F # Ajoute cet import en haut
import sys
from database import init_db, get_or_create_user

# Remplace par ton vrai Token obtenu via @BotFather
TOKEN = "8459019089:AAEIIvSHsKdOmTkyoS0Lh5HdRWTIoUWhye8"
# L'URL où sera hébergée ton interface de scan (ex: GitHub Pages ou ton VPS)
WEB_APP_URL = "https://mrredal.github.io/kikoll/web_app/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Création du bouton clavier qui ouvre la Mini App (la caméra)
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🚀 SCANNER MON IDENTITÉ", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f"Bienvenue {message.from_user.first_name} !\n\n"
        "Pour obtenir ton pseudo exclusif et entrer dans la base de données, "
        "clique sur le bouton 'SCANNER MON IDENTITÉ' en bas de ton écran pour démarrer le scan biométrique.",
        reply_markup=markup
    )

# Ce handler reçoit les données envoyées par tg.sendData() de ton HTML
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    data = message.web_app_data.data # C'est le JSON envoyé par le JS
    print(f"Données reçues : {data}")
    
    # Récupérer ou créer l'utilisateur dans la base de données
    mon_pseudo = get_or_create_user(message.from_user.id)
    
    await message.answer(
        f"✅ **Scan Biométrique Confirmé !**\n\n"
        f"Identité sécurisée dans la base de données.\n"
        f"Ton pseudo exclusif est : `{mon_pseudo}`\n\n"
        "*(Pour info : Ton pseudo a été pioché dans les célèbres listes de mots de passe Open Source de Kali Linux, comme rockyou.txt !)*\n\n"
        "Félicitations, tu fais maintenant partie de l'élite."
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    init_db() # Initialisation de la BDD
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
