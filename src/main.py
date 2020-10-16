import discord
from discord.ext import commands
import requests
from constants import TOKEN

bot = commands.Bot(command_prefix='z!')


def create_link(display, name):
    return '[' + display + ']' + '(https://www.twitch.tv/' + name + ')'


async def get_data():
    response = requests.get('https://zevent.fr/api/data.json')
    json = response.json()
    return json


@bot.event
async def on_ready():
    print('the bot is up and running !')
    print('username : {}'.format(bot.user.name))
    print('user id : {}'.format(bot.user.id))


@bot.command()
async def online(ctx):
    data = await get_data()
    connected = ''
    for element in data['live']:
        if (element['online'] == True):
            connected += create_link(element['display'],
                                     element['twitch']) + ' | '
    embed = discord.Embed(title='ONLINE STREAMERS',
                          description=connected, color=0x4bba30)
    await bot.get_channel(ctx.message.channel.id).send(embed=embed)


bot.run(TOKEN)
