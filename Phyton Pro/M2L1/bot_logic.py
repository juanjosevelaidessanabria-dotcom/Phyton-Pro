"""Module providing a funtion to Discord bot."""
import random

def gen_pass(pass_length):
    """Function creating a password."""
    elements = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789+-/*!&$#?=@<>"
    password = ""

    for _ in range(pass_length):
        password += random.choice(elements)

    return password

def gen_emodji():
    """Function sending a emoji."""
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emodji)

def flip_coin():
    """Function flipping a coin."""
    flip = random.randint(0, 2)
    if flip == 0:
        return "Cara"
    else:
        return "Sello"
