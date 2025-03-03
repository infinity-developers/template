import os
import discord
import traceback
import platform
import importlib
import logging
from discord.ext import commands
from modules.ErrorHandling import handler,logger
from dotenv import load_dotenv


class Bot(commands.AutoShardedBot):
    def __init__(self):
        self.check_and_create_env()
        load_dotenv()

        self.COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')
        self.TOKEN = os.getenv('TOKEN')

        intents = discord.Intents.default()
        super().__init__(command_prefix=self.COMMAND_PREFIX, intents=intents, help_command=None)

        self.tree.on_error = self.on_tree_error
        self.on_command_error = self.on_command_error

    def check_and_create_env(self):
        if not os.path.exists('.env'):
            with open('.env', 'w') as env_file:
                env_file.write("COMMAND_PREFIX=!\n")
                env_file.write("TOKEN=replace-your-discord-bot-token-here\n")
                env_file.write("DB_HOST=127.0.0.1\n")
                env_file.write("DB_PORT=3306\n")
                env_file.write("DB_USERNAME=root\n")
                env_file.write("DB_PASSWORD=password\n")
                env_file.write("DB_NAME=database_name\n")
            logger.info(".env file created. Please update the TOKEN value.")
            quit()

    async def load_pyc_extension(self, cog_path, cog_name):
        try:
            spec = importlib.util.spec_from_file_location(cog_name, cog_path)
            if spec is None:
                raise ImportError(f"Could not load spec for {cog_name}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'setup'):
                await module.setup(self)
                logger.debug(f"{cog_name} cog has been loaded (pyc)")
            else:
                raise ImportError(f"No 'setup' function found in {cog_name}")
        
        except Exception:
            logger.error(f"Failed to load {cog_name}:\n{traceback.format_exc()}")

    async def cog_loader(self):
        cog_dir = './cogs'
        if not os.path.exists(cog_dir):
            logger.warning(f"{cog_dir} directory not found!")
            return

        cog_files = [f[:-3] for f in os.listdir(cog_dir) if f.endswith('.py')]

        for cog in cog_files:
            try:
                await self.load_extension(f'cogs.{cog}')
                logger.debug(f"{cog} cog has been loaded")
            except Exception:
                logger.error(f"Failed to load {cog}:\n{traceback.format_exc()}")

        cog_pyc_files = [f for f in os.listdir(cog_dir) if f.endswith('.pyc')]
        for cog_file in cog_pyc_files:
            cog_name = cog_file.split('.')[0]
            cog_path = os.path.join(cog_dir, cog_file)
            await self.load_pyc_extension(cog_path, cog_name)

        synced = await self.tree.sync()

        for command in synced:
            logger.debug(f"Command '{command.name}' synced")

    async def on_tree_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        await handler.error_handler(interaction, error)
    
    async def on_command_error(self, ctx: commands.Context, error: discord.app_commands.AppCommandError):
        await handler.on_command_error(ctx, error)

    async def on_ready(self):
        await self.cog_loader()
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="KKPP PVP Players",
                state="Let's get your guns"
            )
        )

        logger.info(f"Logged in as: {self.user} (ID: {self.user.id})")
        logger.info(f"Discord Version: {discord.__version__}")
        logger.info(f"Python Version: {platform.python_version()}")
        logger.info(f"Platform: {platform.platform()}")
        logger.info(f"System: {platform.system()} - {platform.machine()}")
        logger.info(f"Processor: {platform.processor()}")
        logger.info(f"Version: {platform.version()} - {platform.release()}")
        logger.info("The bot is ready to perform!")

    async def reload_cog(self, cog_name):
        try:
            await self.unload_extension(f"cogs.{cog_name}")
            await self.load_extension(f"cogs.{cog_name}")
            logging.debug(f"Cog {cog_name} reloaded successfully")
            return f"Cog `{cog_name}` has been reloaded successfully!"
        except Exception:
            logging.error(f"Failed to reload {cog_name}:\n{traceback.format_exc()}")
            return f"Failed to reload `{cog_name}`. Check logs for details."
        
    def run(self):
        super().run(self.TOKEN, reconnect=True,root_logger=logger)

bot = Bot()

@bot.command(name="reload", help="Reload a specific cog")
@commands.has_permissions(administrator=True)
async def reload(ctx:commands.Context, cog: str):
    result = await bot.reload_cog(cog)
    await ctx.send(result,delete_after=10)

@reload.error
async def reload_error(ctx:commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.",delete_after=30)
    else:
        logging.error(f"Error in reload command:\n{traceback.format_exc()}")
        await ctx.send("An error occurred while reloading the cog.",delete_after=30)

if __name__ == "__main__":
    bot.run()
