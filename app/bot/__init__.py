import discord
import os
import logging

from discord.ext import commands

class Bot(commands.Bot):
    
    def __init__(self):
        
        intents = discord.Intents.all()

        super().__init__(
            intents=intents,
            command_prefix="?."
        )

    
    def run(self):
        """
        Method that is run to start the bot
        """

        token = os.environ.get("DISCORD_TOKEN")


        # Running the bot
        super().run(
            token=token, 
            root_logger=True,
            reconnect=True,
            log_handler=None
        )


    async def on_ready(self):
        """
        Function is called whever bot is ready
        it's an event function, defaulted by parent
        """
        logger = logging.getLogger('\t    bot.initialize')

        # await self.manager.load_extensions(self, logger)

        # Changes bot's status
        activity = discord.Streaming(
            name="Working", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        await super().change_presence(status=discord.Status.idle, activity=activity)

        logger.info(f" Bot is ready!")

bot = Bot()