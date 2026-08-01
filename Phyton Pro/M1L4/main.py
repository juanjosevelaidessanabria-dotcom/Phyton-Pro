"""Module"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot_logic import gen_pass, gen_emodji, flip_coin

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()
# Activar el privilegio de lectura de mensajes
intents.message_content = True
# Crear un bot en la variable cliente y transferirle los privilegios
client = discord.Client(intents=intents)

intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    """Function """
    print(f'Hemos iniciado sesión como {client.user}')

@client.event
async def on_message(message):
    """Function"""
    if message.author == client.user:
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
    # --- Nueva función: !deleteme ---
    elif message.content.startswith('$deleteme'):
        # Envía un mensaje y lo borra inmediatamente
        msg = await message.channel.send('I will delete myself now...')
        await msg.delete()

        # Envía un mensaje que se borra automáticamente después de 3 segundos
        await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)
    else:
        # Reenvía cualquier otro mensaje recibido
        await message.channel.send(message.content)

@client.event
async def on_message_delete(message):
    """Nueva función: Se ejecuta automáticamente cuando alguien borra un mensaje."""
    msg = f'{message.author} has deleted the message: {message.content}'
    await message.channel.send(msg)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for _ in range(times):
        await ctx.send(content)

# Inicia el bot (reemplaza con tu token real)
client.run(TOKEN)
