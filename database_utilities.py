
import sqlite3
import os

import numpy
import torch
from PIL import Image

import image_utilities

import discord


db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def getConnection():
    return conn

def getCursor():
    return cursor

def closeConnection():
    conn.close()

def getGuild(guild_id):

    cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()
    return result

def getEmojis():

    cursor.execute("SELECT * FROM emojis")
    result = cursor.fetchall()
    return result

def getEmojiByName(emoji_name):

    cursor.execute("SELECT * FROM emojis WHERE emoji_name = ?", (emoji_name,))
    result = cursor.fetchone()
    return result

def getEmojiByID(emoji_id):

    cursor.execute("SELECT * FROM emojis WHERE emoji_id = ?", (emoji_id,))
    result = cursor.fetchone()
    return result

def getEmoji(emoji_name_or_id):

    cursor.execute("SELECT * FROM emojis WHERE emoji_name = ? OR emoji_id = ?", (emoji_name_or_id, emoji_name_or_id))
    result = cursor.fetchone()
    return result

def indexEmoji(emoji, embed=True):

    if not getEmoji(emoji.name):

        if embed:
            embedding = embedEmoji(emoji) # We embed the emoji

        cursor.execute("INSERT INTO emojis (emoji_name, emoji_id) VALUES (?, ?, ?)", (emoji.name, emoji.id, embed))
        conn.commit()

def asEmoji(bot, emoji_tuple):

    emoji_id = emoji_tuple[1]

    emoji = bot.get_emoji(emoji_id)
    return emoji

def embedEmoji(emoji, force=False):

    embedding = None

    if not force or getEmoji(emoji.name)[2] == 0:
        # First we save the emoji's image
        image_name = emoji.name + '.png'
        image_path = os.path.join(os.path.dirname(__file__), 'images', image_name)
        emoji.save(image_path)

        # We then embed the emoji's image
        embedding = image_utilities.embedImage(Image.open(image_path))
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
