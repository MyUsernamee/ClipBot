import discord

from discord_utilities import send_fancy_message
from database_utilities import get_guild_settings, index_guild, update_guild_settings
from statics import default_settings, type_values


def add_commands(bot):

    @bot.command(name="settings", aliases=["set"], usage="<setting> <value>", description="Sets a setting for the current guild.")
    async def setting(ctx, *args):

        if len(args) == 0: # Send possible settings and usage
            embed = discord.Embed(title="Settings", description="The following settings are available:")

            for setting in default_settings:
                embed.add_field(name=setting, value="Default Value: " + str(default_settings[setting]), inline=False)

            embed.set_footer(text="Use `settings <setting> <value>` to set a setting.")

            await ctx.channel.send(embed=embed)
            return

        if len(args) == 1:
            await send_fancy_message(ctx, "Please specify a value to set.", title="Error")

        key = args[0]
        values = args[1:]
        values = list(values)

        index_guild(ctx.guild.id) # Make sure the guild is indexed

        if not key in default_settings:
            await send_fancy_message(ctx, "That key does not exist.", title="Error")
            return

        guild_settings = get_guild_settings(ctx.guild.id)

        if type_values[type(default_settings[key])] != False and not values[0] in type_values[type(default_settings[key])]:
            #If the value is not in the list of values, return an error
            await send_fancy_message(ctx, "That value is not valid. Possible values are " + str(type_values[type(default_settings[key])]), title="Error")
            return

        elif type_values[type(default_settings[key])] == False:

            # Try to cast the value to the correct type
            try:
                values[0] = type(default_settings[key])(values[0])
            except ValueError:
                await send_fancy_message(ctx, "That value is not valid.", title="Error")
                return

        else:

            # If the value is in the list of values, cast it to the correct type
            values[0] = type_values[type(default_settings[key])][values[0]]

        guild_settings[key] = values[0]
        update_guild_settings(ctx.guild.id, guild_settings)
        await send_fancy_message(ctx, "Set " + key + " to " + str(values[0]), title="Success")
