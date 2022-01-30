
def add_commands(bot):

    @bot.command(name='ping')
    async def ping(ctx):
        await ctx.send('Pong!')
