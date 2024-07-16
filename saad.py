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
AUTHORIZED_USERS = ['mwkcr7', 'thoromir3679']

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
async def move(ctx, member: discord.Member):
    if str(ctx.author) not in AUTHORIZED_USERS:
        await ctx.send('You are not authorized to use this command.')
        return

    if not member.voice or not member.voice.channel:
        await ctx.send('The mentioned user is not in a voice channel.')
        return

    voice_channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.VoiceChannel)]
    if not voice_channels:
        await ctx.send('No voice channels found in the server.')
        return

    random_channel = random.choice(voice_channels)
    await member.move_to(random_channel)
    await ctx.send(f'Moved {member.mention} to {random_channel.name}')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')
