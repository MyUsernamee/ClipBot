#Simple Discord bot to take images and classify them with clip as a emoji

# Imports
import importlib
import discord.ext.commands as commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If the load fails, exit
if not os.getenv("DISCORD_TOKEN"):
    print("No DISCORD_TOKEN found in .env file")
    exit(1)

# Load the bot
bot = commands.Bot(command_prefix=".")

# Load the add_commands function from every file in the commands folder
for file in os.listdir("./commands"):
    if file.endswith(".py"):
        importlib.import_module("commands." + file[:-3]).add_commands(bot)


# Login
bot.run(os.getenv('DISCORD_TOKEN'))
