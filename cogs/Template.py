from discord.ext import commands
import discord

class Presence(commands.GroupCog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        
    @discord.app_commands.command(name="setstatus", description="Set the bot's status and activity")
    @discord.app_commands.choices(
        status=[
            discord.app_commands.Choice(name="Online", value="online"),
            discord.app_commands.Choice(name="Idle", value="idle"),
            discord.app_commands.Choice(name="Do Not Disturb", value="dnd"),
            discord.app_commands.Choice(name="Invisible", value="invisible")
        ],
        activity_type=[
            discord.app_commands.Choice(name="Playing", value="playing"),
            discord.app_commands.Choice(name="Listening", value="listening"),
            discord.app_commands.Choice(name="Watching", value="watching")
        ]
    )
    async def setstatus(
        self,
        interaction: discord.Interaction, 
        status: discord.app_commands.Choice[str],
        activity_type: discord.app_commands.Choice[str],
        activity: str,
        state:str=None
    ):
        discord_status = getattr(discord.Status, status.value)
        
        if activity_type.value == "playing":
            discord_activity = discord.Game(name=activity)
        elif activity_type.value == "listening":
            discord_activity = discord.Activity(type=discord.ActivityType.listening, name=activity,state=state)
        elif activity_type.value == "watching":
            discord_activity = discord.Activity(type=discord.ActivityType.watching, name=activity,state=state)
        else:
            discord_activity = None

        await self.bot.change_presence(status=discord_status, activity=discord_activity)
        
        await interaction.response.send_message(
            f"Status updated to: {status.name}, {activity_type.name} {activity}"
        )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Presence(bot))
    await bot.tree.sync()
