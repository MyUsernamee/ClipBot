import discord

from discord_utilities import send_fancy_message
from database_utilities import get_guild_settings, index_guild, update_guild_settings, get_guild_permissions, \
    get_admin_level, update_guild_permissions
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

    @bot.command(name="add_permission", aliases=["add_perm"], usage="<permission>",
                 description="Adds a permission to the current guild.")
    async def add_permission(ctx, *args):

        if len(args) == 0:
            await send_fancy_message(ctx, "Please specify a permission to add.", title="Error")
            return

        # Check if the user that sent the message is allowed to use this command
        user_permission = get_admin_level(ctx.author.id)

        if user_permission is None or user_permission < 9:
            await send_fancy_message(ctx, "You do not have permission to use this command.", title="Error")
            return

        permission = args[0]

        update_guild_permissions(ctx.guild.id, get_guild_permissions(ctx.guild.id) + [permission])

        await send_fancy_message(ctx, "Added " + permission + " to the list of permissions.", title="Success")

    @bot.command("check_user_permissions", aliases=["check_user_perm", "cp"], usage="<user>",
                 decription="Checks the permissions of a user.")
    async def check_user_permissions(ctx, *args):

        user = None

        if len(args) == 0:
            user = ctx.author
        else:
            user = ctx.guild.get_member_named(args[0])

        if not user:
            await send_fancy_message(ctx, "That user does not exist.", title="Error")
            return

        permissions = get_admin_level(user.id)

        if permissions is None:
            permissions = 0

        await send_fancy_message(ctx, "User " + user.name + " has a admin level of " + str(permissions), title="Success")


