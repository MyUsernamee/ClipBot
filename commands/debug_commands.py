from database_utilities import get_emoji, as_emoji
from discord_utilities import send_fancy_message

def add_commands(bot):

    @bot.command(name="emoji_info", usage="<emoji name>", description="Get information about an emoji. (DEBUG)"
                 , aliases=["ei", "einfo", "emojiinfo"])
    async def emoji_info(ctx, emoji_name: str):
        """

        :param ctx:
        :param emoji_name:
        :return:
        """

        emoji = get_emoji(emoji_name)
        if emoji is None:
            await send_fancy_message(ctx, "Emoji not found.")
            return

        emoji_object = as_emoji(bot, emoji)

        await send_fancy_message(ctx,
                                 f"Name: {emoji_object.name}\n"
                                 f"ID: {emoji_object.id}\n"
                                 f"URL: {emoji_object.url}\n"
                                 f"Animated: {emoji_object.animated}\n"
                                 f"Emoji Tuple: {emoji}", title="Emoji Info", color=0x00ff00)

    @bot.command(name="react", usage="<emoji name>", description="React to a message with an emoji. (DEBUG)"
                 , aliases=["re"])
    async def react(ctx, emoji_name: str):
        """

        :param ctx:
        :param emoji_name:
        :return:
        """

        emoji = get_emoji(emoji_name)
        if emoji is None:
            await send_fancy_message(ctx, "Emoji not found.")
            return

        emoji_object = as_emoji(bot, emoji)
        if emoji_object is None:
            await send_fancy_message(ctx, "Emoji not found.")
            return

        await ctx.message.add_reaction(emoji_object)

