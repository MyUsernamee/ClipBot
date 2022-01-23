import json
import sqlite3
import os

import numpy
import torch
from PIL import Image

import image_utilities

from statics import default_settings

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def get_connection():
    return conn


def get_cursor():
    return cursor


def close_connection():
    conn.close()


def get_guild(guild_id):
    cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()
    return result

def get_guild_settings(guild_id):

    guild_settings = get_guild(guild_id)
    guild_settings = json.loads(guild_settings[1])

    return guild_settings

def index_guild(guild_id):

    if not get_guild(guild_id): # If the guild is not in the database yet then we add it with the default settings
        cursor.execute("INSERT INTO guilds (guild_id) VALUES (?, ?)", (guild_id, json.dumps(default_settings)))
        conn.commit()


def update_guild_settings(guild_id, settings):
    cursor.execute("UPDATE guilds SET settings = ? WHERE guild_id = ?", (json.dumps(settings), guild_id))
    conn.commit()


def get_emojis():
    cursor.execute("SELECT * FROM emojis")
    result = cursor.fetchall()
    return result


def get_emoji_by_name(emoji_name):
    cursor.execute("SELECT * FROM emojis WHERE emoji_name = ?", (emoji_name,))
    result = cursor.fetchone()
    return result


def get_emoji_by_id(emoji_id):
    cursor.execute("SELECT * FROM emojis WHERE emoji_id = ?", (emoji_id,))
    result = cursor.fetchone()
    return result


def get_emoji(emoji_name_or_id):
    cursor.execute("SELECT * FROM emojis WHERE emoji_name = ? OR emoji_id = ?", (emoji_name_or_id, emoji_name_or_id))
    result = cursor.fetchone()
    return result


def index_emoji(emoji, embed=True):
    if not get_emoji(emoji.name):

        if embed:
            embedding = embed_emoji(emoji)  # We embed the emoji

        cursor.execute("INSERT INTO emojis (emoji_name, emoji_id) VALUES (?, ?, ?)", (emoji.name, emoji.id, embed))
        conn.commit()


def as_emoji(bot, emoji_tuple):
    emoji_id = emoji_tuple[1]

    emoji = bot.get_emoji(emoji_id)
    return emoji


def embed_emoji(emoji, force=False):
    embedding = None

    if not force or get_emoji(emoji.name)[2] == 0:
        # First we save the emoji's image
        image_name = emoji.name + '.png'
        image_path = os.path.join(os.path.dirname(__file__), 'images', image_name)
        emoji.save(image_path)

        # We then embed the emoji's image
        embedding = image_utilities.embed_image(Image.open(image_path))
        numpy.save(embedding.numpy(), image_path[:-4] + '.npy')

        # We then delete the image
        os.remove(image_path)

        # We then update the database
        cursor.execute("UPDATE emojis SET embedding = ? WHERE emoji_name = ?", (True, emoji.name))

        conn.commit()

    else:

        embedding = torch.tensor(numpy.load(os.path.join(os.path.dirname(__file__), 'images', emoji.name + '.npy')))

    # We then return the embedding
    return embedding
