# First we git pull
git pull

# Then we stop the screen running our bot
screen -S bot -X quit

# Then we start the bot
screen -dmS bot python3 main.py
