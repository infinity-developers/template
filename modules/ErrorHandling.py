import datetime
import discord
import logging
import sys
from discord.ext import commands

def now():
    nw = datetime.datetime.today().__format__("%Y-%m-%d %H:%M:%S")
    return nw

class Logger:
    def __init__(self, log_file="bot.log"):
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.DEBUG)

        self.log_format = "%(asctime)s - %(levelname)s - %(message)s"

        file_handler = logging.FileHandler(log_file, mode='+w')
        file_formatter = logging.Formatter(self.log_format)
        file_handler.setFormatter(file_formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

logger = Logger().get_logger()

class ErrorHandling:
    def __init__(self):
        logger.info("Error handing activated")

    async def send_reply(self, interaction: discord.Interaction, msg: str):
        embed=discord.Embed(title="Error",description=f"### {msg}",color=discord.Color.red())
        try:
            await interaction.response.send_message(
                f"{interaction.user.mention}",
                ephemeral=True,
                embed=embed,
                delete_after=15
            )
        except discord.errors.InteractionResponded:
            try:
                await interaction.followup.send(
                    f"{interaction.user.mention}",
                    embed=embed,
                    ephemeral=True
                )
            except discord.errors.HTTPException:
                try:
                    await interaction.channel.send(
                        f"{interaction.user.mention}",
                        embed=embed,
                        delete_after=15
                    )
                except discord.errors.Forbidden:
                    pass

    async def error_handler(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await self.send_reply(interaction, "An error occurred while executing the command.")
        
        elif isinstance(error, (discord.app_commands.errors.TransformerError, 
                                discord.app_commands.errors.TranslationError)):
            await self.send_reply(interaction, "I didn't understand your input. Please try again.")

        elif isinstance(error, discord.app_commands.errors.NoPrivateMessage):
            await self.send_reply(interaction, "This command cannot be used in DMs.")

        elif isinstance(error, (discord.app_commands.errors.MissingRole,
                                discord.app_commands.errors.MissingAnyRole, 
                                discord.app_commands.errors.MissingPermissions)):
            await self.send_reply(interaction, "You don't have permission to use this command.")

        elif isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await self.send_reply(interaction, "This command is on cooldown. Please wait before using it again.")

        elif isinstance(error, discord.app_commands.errors.CommandNotFound):
            await self.send_reply(interaction, "Unknown command. Use `/help` to see available commands.")

        elif isinstance(error, discord.errors.NotFound):
            pass

        elif isinstance(error, discord.errors.Forbidden):
            await self.send_reply(interaction, "I don't have permission to perform this action.")

        elif isinstance(error, discord.errors.HTTPException):
            await self.send_reply(interaction, "A network error occurred. Please try again.")

        elif isinstance(error, commands.ExtensionError):
            await self.send_reply(interaction, "An error occurred with an extension/module.")

        elif isinstance(error, discord.errors.InteractionResponded):
            pass

        else:
            logger.error(error)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Handles errors for text-based commands."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.", delete_after=10)

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have the necessary permissions to execute this command.", delete_after=10)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required arguments. Use `!help <command>` for details.", delete_after=10)

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Try again in {round(error.retry_after, 2)} seconds.", delete_after=10)

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command. Use `!help` to see available commands.", delete_after=10)

        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input.", delete_after=10)

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You cannot use this command in the current context.", delete_after=10)

        else:
            logger.error(error)

handler = ErrorHandling()
