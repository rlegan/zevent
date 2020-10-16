import discord
from constants import TOKEN

bot = discord.Client()


@bot.event
async def on_ready():
    print('the bot is up and running !')
    print('username : {}'.format(bot.user.name))
    print('user id : {}'.format(bot.user.id))


bot.run(TOKEN)
