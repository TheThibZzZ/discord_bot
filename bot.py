import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Liste des mots à censurer
censored_words = ["pd", "tg", "fdp"]  # Ajoutez d'autres mots au besoin

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté au serveur suivant :\n{GUILD}')

@bot.command(name='site', help='Affiche une liste de sites pour le poker en ligne en France')
async def site(ctx: Context):
    sites_list = [
        "https://www.pokerstars.fr/",
        "https://www.winamax.fr/",
        "https://www.betclic.fr/poker/",
        "https://www.unibet.fr/poker",
        "https://www.partypoker.fr/",
        # Ajoutez d'autres sites au besoin
    ]

    response = "Voici les sites de Poker en ligne autorisés en France :\n"
    response += "\n".join([f"`{site}`" for site in sites_list])

    await ctx.send(response)

@bot.command(name='outils', help='Affiche une liste de sites utiles avec des descriptions')
async def outils(ctx: Context):
    sites_info = {
        "https://gtowizard.com/": "GTO Solution",
        "https://fr.sharkscope.com/": "Statistique sur les joueurs",
    }

    response = "Des outils pour s'améliorer :\n"
    for site, description in sites_info.items():
        response += f"**{site}:** {description}\n"

    await ctx.send(response)

@bot.event
async def on_message(message):
    # Vérifier si le message contient des mots censurés
    for word in censored_words:
        if word in message.content.lower():
            # Cacher le mot avec des astérisques
            censored_message = '*' * len(message.content)
            await message.channel.send(f"Attention, le message de {message.author.mention} a été censuré : {censored_message}")
            await message.delete()
            break  # Arrêter la recherche après le premier mot trouvé

    # Appeler le gestionnaire d'événements par défaut pour les autres fonctionnalités du bot
    await bot.process_commands(message)

# Démarrer le bot
bot.run(TOKEN)
