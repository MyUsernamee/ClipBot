
def add_commands(bot):

    @bot.command()
    def spam(ctx, *args):

        sentence = ' '.join(args[1:])

        for i in range(0, int(args[0])):
            await ctx.channel.send(sentence)


