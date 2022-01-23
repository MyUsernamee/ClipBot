import discord


async def send_fancy_message(ctx, message, title=None, footer=None, color=0x444444):
    """
    Sends a fancy message to the specified channel.
    """
    embed = discord.Embed(title=title, description=message, color=color)
    embed.set_footer(text=footer)
    await ctx.channel.send(embed=embed)
