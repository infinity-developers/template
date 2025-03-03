import discord
from typing import List

async def get_user_messages(channel: discord.TextChannel, user: discord.User, count: int, reversed: bool = False, delete_rest_messages: bool = False) -> List[discord.Message]:
    messages = []
    
    try:
        async for message in channel.history(limit=1000):
            if message.author.id == user.id:
                if (len(messages) < count) and (not message.attachments):
                    messages.append(message)
                elif delete_rest_messages:
                    await message.delete()
        
    except:
        pass
    
    if len(messages)<count:
        while True:
            msg=await channel.send("__ Template __")
            messages.append(msg)
            if len(messages)==count:
                break

    if reversed:
        messages.reverse()

    return messages
