import discord
import random
from discord.ext import commands
from g4f.client import Client
from g4f.Provider import RetryProvider, FreeGpt, TalkAi, Koala

import g4f.debug
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

client = Client(RetryProvider([FreeGpt]))

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Ensure we can access member data
intents.voice_states = True  # Ensure we can access voice state data
bot = commands.Bot(command_prefix="!", intents=intents)

# Authorized users for the !move command
AUTHORIZED_USERS = {
    'mwkcr7': 'thoromir3679',
    'thoromir3679': 'mwkcr7'
}

# Target user and predefined responses
target = "saadii"
responses = [
    "BEST FRIEND <3",
    "KESA HAI JAANI",
    "CUTEST",
    "BOHAT PYARA LAG RHA HAI",
    "FLASHBANG",
]

# On bot ready event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# On message event
@bot.event
async def on_message(message):
    authorID = str(message.author)
    content = str(message.content)
    print(authorID)
    if message.author == bot.user:
        return
    if authorID == target and content == "!saad":
        return
    if authorID == target:
        await message.reply(responses[random.randint(0, 4)])
    await bot.process_commands(message)

# Define the !saad command
@bot.command()
async def saad(ctx):
    await ctx.send("I am only SAADE KA DOST!")

# Define the !ai command
@bot.command()
async def ai(ctx, *, input_text: str):
    try:
        # Define the request to the AI model
        story_request = f"You are a discord bot and your name is SAADE KA DOST and you are a big simp,and you must not reply in chinese,now reply to this input by a user '{input_text}'"

        # Generate the response from the AI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": story_request}],
        )
        story = response.choices[0].message.content

        # Define the maximum length for each message
        max_length = 2000

        # Divide the story into parts if it's longer than max_length
        parts = [story[i: i + max_length] for i in range(0, len(story), max_length)]

        # Send each part of the story to the Discord channel
        for part in parts:
            await ctx.send(part)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Define the !move command
@bot.command()
async def move(ctx, *, channel_name: str = None):
    # Check if the command is used in the specific text channel named "command"
    if ctx.channel.name != "command":
        await ctx.send('This command can only be used in the #command channel.')
        return

    if str(ctx.author) not in AUTHORIZED_USERS:
        await ctx.send('You are not authorized to use this command.')
        return

    target_username = AUTHORIZED_USERS[str(ctx.author)]
    target_member = discord.utils.get(ctx.guild.members, name=target_username)

    if not target_member:
        await ctx.send(f'User {target_username} not found in the server.')
        return

    if not target_member.voice or not target_member.voice.channel:
        await ctx.send(f'{target_member.name} is not in a voice channel.')
        return

    if channel_name:
        channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
        if not channel:
            await ctx.send(f'Channel {channel_name} not found.')
            return
    else:
        voice_channels = [channel for channel in ctx.guild.voice_channels if channel != target_member.voice.channel]
        if not voice_channels:
            await ctx.send('No other voice channels found in the server.')
            return
        channel = random.choice(voice_channels)

    await target_member.move_to(channel)
    await ctx.send(f'Moved {target_member.mention} to {channel.name}')

# Run the bot with the actual bot token
bot.run(BOT_TOKEN)
