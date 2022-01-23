#Simple Discord bot to take images and classify them with clip as a emoji

# Imports
import importlib
import json

import discord.ext
import discord.ext.commands as commands
import numpy as np
import torch
import clip
import os
import sqlite3
from PIL import Image
from gpt_j.Basic_api import simple_completion
from dotenv import load_dotenv
from statics import *
from image_utilities import *

load_dotenv()
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
bot = commands.Bot(command_prefix=".")

# Load the add_commands function from every file in the commands folder
for file in os.listdir("./commands"):
    if file.endswith(".py"):
        importlib.import_module("commands." + file[:-3]).add_commands(bot, cursor, connection, model, preprocess, device)


#Login
bot.run(os.getenv('DISCORD_TOKEN'))