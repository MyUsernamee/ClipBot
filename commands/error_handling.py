from discord.ext import commands
from discord_utilities import send_fancy_message


def add_commands(bot):

    # This function should never be called, but just in case
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandError) and not isinstance(error, commands.CommandNotFound):
            await send_fancy_message(ctx, "Sorry something happened and I can't perform the command you requested."
                                          "\n\n```{}```".format(error), title="Error")

