import discord
from constants import TOKEN

bot = discord.Client()


@bot.event
async def on_ready():
    print('the bot is up and running !')
    print('username : {}'.format(bot.user.name))
    print('user id : {}'.format(bot.user.id))


@bot.event
async def on_message_edit(before, after):
    channel = before.channel
    author = before.author

    await channel.send(
        '```{}```⬇️```{}```(<@{}>)'.format(before.content, after.content, author.id))

bot.run(TOKEN)
