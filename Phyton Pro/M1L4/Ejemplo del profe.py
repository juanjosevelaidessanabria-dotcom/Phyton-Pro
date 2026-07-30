"""Module"""
import random
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# 1. Configuración de permisos básicos (Intents)
intents = discord.Intents.default()
intents.message_content = True  # Necesario para que el bot lea mensajes y comandos

# 2. Creación del bot con el prefijo "!"
bot = commands.Bot(command_prefix="!", intents=intents)


# Evento que confirma cuando el bot está listo y conectado
@bot.event
async def on_ready():
    """Function"""
    print(f"¡Bot listo! Conectado como {bot.user}")

# COMANDO 1: Generador de contraseñas
# Ejemplo de uso en Discord: !password 10
@bot.command()
async def password(ctx, longitud: int = 8):
    """Function"""
    # Caracteres posibles para la contraseña
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"

    # Selecciona caracteres al azar según la longitud pedida
    nueva_clave = "".join(random.choice(caracteres) for _ in range(longitud))

    # Responde al usuario en el chat
    await ctx.send(f"🔑 Tu contraseña es: `{nueva_clave}`")


# COMANDO 2: Lanzador de moneda
# Ejemplo de uso en Discord: !moneda
@bot.command()
async def moneda(ctx):
    """Function"""
    opciones = ["Cara 🪙", "Cruz 🪙"]
    resultado = random.choice(opciones)

    await ctx.send(f"Lanzando la moneda... ¡Salió **{resultado}**!")


# COMANDO 3: Emoji aleatorio
# Ejemplo de uso en Discord: !emoji
@bot.command()
async def emoji(ctx):
    """Function"""
    # Lista chiquita de emojis
    emojis = ["🔥", "🚀", "🍕", "🎮", "🐍", "😎"]
    emoji_azar = random.choice(emojis)

    await ctx.send(emoji_azar)


# 3. Arrancar el bot con su TOKEN (reemplaza esto con el token de tu bot)
bot.run("TU_TOKEN_AQUI")
