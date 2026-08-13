"""Module"""
import random
import os
import discord
import requests
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
    """Envía un meme con sistema de rarezas."""

    rarezas = ['Comun', 'Raro', 'Legendario']
    probabilidades = [0.70, 0.25, 0.05]
    rareza_elegida = random.choices(rarezas, weights=probabilidades, k=1)[0]

    # Usamos f-string para enviar UNA SOLA ruta completa a os.listdir
    folder_path = f"C:/Users/USUARIO/OneDrive/Desktop/Phyton Pro/M2L1/images/{rareza_elegida}"
    images = os.listdir(folder_path)

    selected_image = random.choice(images)

    with open(f"{folder_path}/{selected_image}", 'rb') as f:
        picture = discord.File(f)
        await ctx.send(content=f"**Meme {rareza_elegida}**", file=picture)

def get_duck_image_url():
    """Busca una imagen"""   
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def tips(ctx):
    """Envía tips de cuidado ambiental"""
    enviroment_tips = [" Cierra la llave mientras te cepillas los dientes y repara fugas.",
                " Apaga luces y aparatos que no uses, y usa bombillas LED.",
                " Clasifica los residuos entre aprovechables, orgánicos y no reciclables.",
                "Lleva siempre tus propias bolsas de tela y botellas reutilizables.",
                "Prefiere caminar, usar la bicicleta o el transporte público en lugar del carro.",
                " Compra productos cercanos y de temporada para disminuir la huella de carbono."]
    await ctx.send(random.choice(enviroment_tips))

@bot.command()
async def memedioambiente(ctx):
    """Envía un meme con sistema de rarezas."""

    rarezas = ['Comun', 'Raro', 'Legendario']
    probabilidades = [0.70, 0.25, 0.05]
    rareza_elegida = random.choices(rarezas, weights=probabilidades, k=1)[0]

    # Usamos f-string para enviar UNA SOLA ruta completa a os.listdir
    folder_path = f"C:/Users/USUARIO/OneDrive/Desktop/Phyton Pro/M2L2/images/ambiente/{rareza_elegida}"
    images = os.listdir(folder_path)

    selected_image = random.choice(images)

    with open(f"{folder_path}/{selected_image}", 'rb') as f:
        picture = discord.File(f)
        await ctx.send(content=f"**Meme {rareza_elegida}**", file=picture)

# Iniciar la instancia 'bot'
bot.run(TOKEN)
