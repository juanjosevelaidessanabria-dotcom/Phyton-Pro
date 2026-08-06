"""Module"""
import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot_logic import gen_pass, gen_emodji, flip_coin

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configurar privilegios (intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Instanciar únicamente 'bot' con prefijo '$'
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    """Confirma el inicio de sesión."""
    print(f'Hemos iniciado sesión como {bot.user}')


@bot.event
async def on_message(message):
    """Maneja respuestas condicionales directas."""
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("Hi!")
    elif message.content.startswith('$bye'):
        await message.channel.send("\U0001f642")
    elif message.content.startswith('$gen pass'):
        await message.channel.send(gen_pass(8))
    elif message.content.startswith('$smile'):
        await message.channel.send(gen_emodji())
    elif message.content.startswith('$coin'):
        await message.channel.send(flip_coin())
    elif message.content.startswith('$deleteme'):
        msg = await message.channel.send('I will delete myself now...')
        await msg.delete()
        await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

    # LÍNEA CLAVE: Permite que discord.py procese los comandos como $repeat y $meme
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    """Se ejecuta automáticamente cuando se elimina un mensaje."""
    msg = f'{message.author} has deleted the message: {message.content}'
    await message.channel.send(msg)


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repite un mensaje el número de veces indicado."""
    for _ in range(times):
        await ctx.send(content)


@bot.command()
async def meme(ctx):
    """Envía una imagen local."""
    images = os.listdir("C:/Users/USUARIO/Desktop/Phyton Pro/M2L1/images")
    image = random.choice(images)
    with open(f'C:/Users/USUARIO/Desktop/Phyton Pro/M2L1/images/{image}', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


# Iniciar la instancia 'bot'
bot.run(TOKEN)
