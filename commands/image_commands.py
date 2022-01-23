from PIL import Image

from image_utilities import compare_images
from discord_utilities import send_fancy_message

def add_commands(bot):

    @bot.command(name='compare', help='Compare two images', usage='(image1 included as attachment) (image2 included as attachment)')
    async def compare(ctx):

        if len(ctx.message.attachments) < 2:
            await ctx.send('You need to attach two images to compare.')
            return

        image1 = ctx.message.attachments[0]
        image2 = ctx.message.attachments[1]

        await image1.save('images/image1' + image1.filename[-4:])
        await image2.save('images/image2' + image2.filename[-4:])

        result = compare_images([Image.open('images/image1' + image1.filename[-4:])], [Image.open('images/image2' + image2.filename[-4:])], return_distances=True)

        await send_fancy_message(ctx, 'The images are ' + str(int(result[0].item())) + '% similar.', title="Image Comparison")