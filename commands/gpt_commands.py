
from gpt_j.Basic_api import simple_completion
from discord_utilities import send_fancy_message

def add_commands(bot):

    @bot.command(name='continue', help='Trys to continue the text using gpt-j', aliases=['c'], usage='<text> [t=<temperature>] [p=top_p]')
    async def completion(ctx, *text):

        if not text:
            await ctx.channel.send('Please provide some text to continue.')
            return

        final_text = ""
        temperature = 0.5
        top_p = 0.9

        for word in text:

            if word.startswith('t='):
                temperature = float(word[2:])
            elif word.startswith('p='):
                top_p = float(word[2:])
            else:
                final_text = final_text + word + " "

        final_text = final_text.strip()

        completion = ""

        try:
            completion = simple_completion(prompt=final_text, length=64, temp=top_p, top=temperature)

        except Exception as e:
            await send_fancy_message(ctx, "Error: " + str(e), color=0xaa8888)
            return

        await send_fancy_message(ctx, completion) # Temp and top_p are flipped
