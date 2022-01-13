#Simple Discord bot to take images and classify them with clip as a emoji

# Imports
import discord
import os
import sys
import torch
import clip
import emoji
from PIL import Image
from gpt_j.Basic_api import simple_completion
from dotenv import load_dotenv

load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

default_emojis = []

with open("emojis.txt", "r") as f:
    #Convert file to default_emojis array
    default_emojis = [line.strip() for line in f.readlines()]

default_emojispruned = []

#Prune the emoji list
for i in range(len(default_emojis)):
    myemoji = default_emojis[i]
    if emoji.emojize(myemoji) != myemoji:
        default_emojispruned.append(myemoji)

default_emojis = default_emojispruned
print(default_emojis)

#Check to make sure the list isn't too long
if len(default_emojis) > 256:
    print("Error: Emoji list is too long")
    sys.exit()

#Create the bot
client = discord.Client()

#Now we detect if a image is posted
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.continue'):

        arguments = message.content.split(" ")
        if len(arguments) < 2:
            await message.channel.send(embed=discord.Embed(title="Usage:", description="`.continue [t=temperature] [p=top_p] <prompt>`"))
            return

        #Get the arguments
        temperature = 1.0
        top_p = 0.9
        prompt = ""
        for i in range(1, len(arguments)):
            if arguments[i].startswith("t="):
                temperature = float(arguments[i][2:])
            elif arguments[i].startswith("p="):
                top_p = float(arguments[i][2:])
            else:
                prompt = prompt + " " + arguments[i]

        #Check to make sure the prompt is valid
        if prompt == "":
            await message.channel.send(embed=discord.Embed(title="Error:", description="Prompt cannot be empty"))
            return

        #Send a request to openai
        response = simple_completion(prompt, length=100, temp=top_p, top=temperature) # Topp and temperature are flipped.

        #Send the response
        await message.channel.send(embed=discord.Embed(title="Response:", description=prompt + " " + response))

    if message.content.startswith(".emoji"):

        with open("emojis.txt", "a") as f:
            #Write the new emoji to the file
            f.write("\n:" + message.content[7:] + ":")
            default_emojis.append(":" + message.content[7:] + ":")

        #Send the new emoji to the channel
        await message.channel.send("Added: " + emoji.emojize(":" + message.content[7:] + ":"))

    if message.attachments.__len__() > 0:

        #Get the image
        image = message.attachments[0]
        image_url = image.url
        image_name = image.filename

        #Download the image
        await image.save("images/" + image_name)
        image = preprocess(Image.open("images/" + image_name)).unsqueeze(0).to(device)
        guildemojis = [emoji.name for emoji in message.guild.emojis]
        guildemojis = guildemojis + default_emojis
        guildemojis = [name.replace(":", "") for name in guildemojis]

        text = clip.tokenize(guildemojis).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)

            logits_per_image, logits_per_text = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        #Get the top emoji
        emoji_index = probs.argmax()
        top_emoji = message.guild.emojis[emoji_index] if emoji_index < len(message.guild.emojis) else emoji.emojize(":" + guildemojis[emoji_index] + ":")

        #Delete the image
        os.remove("images/" + image_name)

        #Create a debug message with the emoji's and their probabilities
        debug_message = ""
        for i in range(len(probs[0])):
            debugEmoji = guildemojis[i]
            debug_message += (debugEmoji) + ": " + str(probs[0][i]) + "\n"

        print(debug_message)
        await message.add_reaction(top_emoji)







#Login
client.run(os.getenv('DISCORD_TOKEN'))