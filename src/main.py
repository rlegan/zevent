import discord
from discord.ext import commands
import requests
from constants import TOKEN

bot = commands.Bot(command_prefix='z!')


async def get_data():
    response = requests.get('https://zevent.fr/api/data.json')
    json = response.json()
    return json


def create_link(display, name, game):
    return '[' + display + ']' + '(https://www.twitch.tv/' + name + ')' + '  -> 🎮 ' + game


def create_goal(goal, donation_amout):
    icon = '✅' if donation_amout > goal['amountRequired']['number'] else '❌'
    return goal['amountRequired']['formatted'] + ' -> ' + icon + ' ' + goal['title']


def check_streamer_name(data, streamer):
    for element in data['live']:
        if (element['display'].lower() == streamer.lower() or element['twitch'].lower() == streamer.lower()):
            return element
    return None


@bot.event
async def on_ready():
    print('the bot is up and running !')
    print('username : {}'.format(bot.user.name))
    print('user id : {}'.format(bot.user.id))


@bot.command()
async def total(ctx):
    data = await get_data()
    total = data['donationAmount']['formatted']
    desc = 'ZEVENT 2020 HAS NOW RAISED ***' + total + '*** !'
    embed = discord.Embed(title='TOTAL DONATIONS',
                          description=desc, color=0x4bba30)
    await bot.get_channel(ctx.message.channel.id).send(embed=embed)


@bot.command()
async def goal(ctx, arg):
    data = await get_data()
    streamer = check_streamer_name(data, arg)
    goal = ''

    if (streamer != None):
        totalDonationNumber = streamer['donationGoal']['donationAmount']['number']
        totalDonationFormatted = streamer['donationGoal']['donationAmount']['formatted']

        goal += '\nCURRENTLY AT ***' + totalDonationFormatted + \
            '***  ON ' + streamer['display'] + " STREAM\n\n"

        for element in streamer['donationGoal']['goals']:
            goal += create_goal(element, int(totalDonationNumber)) + '\n'

        embed = discord.Embed(title='DONATIONS GOALS FOR : ' + streamer['display'],
                              description=goal, color=0x4bba30)
        await bot.get_channel(ctx.message.channel.id).send(
            embed=embed)

    elif (streamer != None and len(streamer['donationGoal']) == 0):
        await bot.get_channel(ctx.message.channel.id).send(
            streamer['display'] + 'has no donation goals setupped on the ZEVENT site.')

    else:
        await bot.get_channel(ctx.message.channel.id).send(
            'Please provide a streamer that is present to the ZEVENT 2020 or check the name you provided.')


@bot.command()
async def online(ctx):
    data = await get_data()
    connectedStreamers = ''
    for element in data['live']:
        if (element['online'] == True):
            connectedStreamer = create_link(element['display'],
                                            element['twitch'], element['game']) + '\n'
            if (len(connectedStreamers) + len(connectedStreamer) >= 2048 and '\t' not in connectedStreamers):
                connectedStreamers += '\t'
            connectedStreamers += connectedStreamer

    if (len(connectedStreamers.split('\t')) > 1):
        embed = discord.Embed(title='ONLINE STREAMERS 1/2',
                              description=connectedStreamers.split('\t')[0], color=0x4bba30)
        await bot.get_channel(ctx.message.channel.id).send(embed=embed)
        embed = discord.Embed(title='ONLINE STREAMERS 2/2',
                              description=connectedStreamers.split('\t')[1], color=0x4bba30)
        await bot.get_channel(ctx.message.channel.id).send(embed=embed)
    else:
        embed = discord.Embed(title='ONLINE STREAMERS',
                              description=connectedStreamers, color=0x4bba30)
        await bot.get_channel(ctx.message.channel.id).send(embed=embed)


bot.run(TOKEN)
