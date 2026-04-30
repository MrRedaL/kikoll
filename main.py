import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F # Ajoute cet import en haut

# Remplace par ton vrai Token obtenu via @BotFather
TOKEN = "8459019089:AAEIIvSHsKdOmTkyoS0Lh5HdRWTIoUWhye8"
# L'URL où sera hébergée ton interface de scan (ex: GitHub Pages ou ton VPS)
WEB_APP_URL = "https://kikoll.github.io/kikoll_v4/web_app/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Création du bouton qui ouvre la Mini App (la caméra)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 SCANNER MON IDENTITÉ", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ])
    
    await message.answer(
        f"Bienvenue {message.from_user.first_name} !\n\n"
        "Pour obtenir ton pseudo exclusif et entrer dans la base de données, "
        "clique sur le bouton ci-dessous pour démarrer le scan biométrique.",
        reply_markup=markup
    )

# Ce handler reçoit les données envoyées par tg.sendData() de ton HTML
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    data = message.web_app_data.data # C'est le JSON envoyé par le JS
    print(f"Données reçues : {data}")
    
    # Logique de récompense (Idée 1 : Pseudo exclusif)
    # Ici on peut imaginer une liste de pseudos "Cyber"
    import random
    pseudos_exclusifs = ["Neon_Wraith", "Cyber_Ronin", "Data_Ghost", "Silicon_Pulse"]
    mon_pseudo = random.choice(pseudos_exclusifs)
    
    await message.answer(
        f"✅ **Scan Biométrique Confirmé !**\n\n"
        f"Identité sécurisée dans la base de données.\n"
        f"Ton pseudo exclusif est : `{mon_pseudo}`\n\n"
        "Félicitations, tu fais maintenant partie de l'élite."
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())