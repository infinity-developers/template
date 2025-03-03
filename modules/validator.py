import re
import discord
import requests
from PIL import Image
from io import BytesIO
from discord.ext import commands
from typing import Union
from .database import db

# Message
def is_valid_message_url(url: str) -> bool:
    pattern = r"^https://(ptb\.|canary\.)?discord\.com/channels/\d+/\d+/\d+$"

    if re.match(pattern, url):
        return True
    return False

async def is_valid_message(bot:commands.AutoShardedBot, channel:discord.TextChannel, message: Union[discord.Message,int]) -> Union[bool, discord.Message]:
    
    if isinstance(message, int):
        message = await channel.fetch_message(message)

    if message is None:
        return False
    return True

# Colors
def code_check(color_code: str):
    if len(color_code) != 7:
        return False
    
    elif color_code.startswith("#") and color_code[1:].isalnum():
        return True

    else:
        return False
    
# Image
def image_check(url):
    try:
        response = requests.get(url)
        Image.open(BytesIO(response.content))
        return url
    except:
        return None