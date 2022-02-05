import os

import torch
from PIL import Image

from database_utilities import index_emoji, get_guild_settings, get_emojis, embed_emoji, get_emoji_objects
from image_utilities import compare_images

def add_commands(bot):

    @bot.listen(name="on_message")
    async def on_message(message):

        if message.author == bot.user:
            return

        # Check if the message is a command
        if message.content.startswith("."): # If the message starts with the prefix then it is a command and we don't want to respond to it
            return

        if not message.attachments:
            return

        # We save the image so we can work with it
        filename = "./images/temp" + message.attachments[0].filename[-4:]
        await message.attachments[0].save(filename)

        # We then get the guilds settings
        guild_settings = get_guild_settings(message.guild.id)

        # We then check if every emoji in this server is indexed, if not we add it
        for emoji in message.guild.emojis:

            await index_emoji(emoji)

        emojis = []

        # If the guild has use emojis from other server enabled, we add all of the emojis from our database to the list
        if guild_settings['useEmojisFromOtherServers']:

            emojis = get_emoji_objects(bot)

        else:

            # If the guild has use emojis from other server disabled, we add only the emojis from this server to the list
            emojis = [emoji for emoji in message.guild.emojis]

        # We then embed every emoji in the message
        embedded_emojis = [await embed_emoji(emoji, device="cpu") for emoji in emojis]
        embedded_emojis = torch.cat(embedded_emojis, dim=0)

        # We then compare the message attachment and the emojis
        probabilities = compare_images([Image.open(filename)], embedded_emojis, encode_images2=False)

        # We then remove the image
        #os.remove("images/temp.png")

        print(probabilities)
        print([emoji.name for emoji in emojis])

        # We then react with the best emojis based on how many the server settings wants
        best_emojis = torch.topk(probabilities, k=(min(guild_settings['emojisPerMessage'], len(emojis))))
        for emoji in best_emojis.indices[0]:

            await message.add_reaction(emojis[emoji])

        return