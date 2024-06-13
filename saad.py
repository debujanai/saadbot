import discord
import random
from discord.ext import commands
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots
import g4f.debug
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

client = Client(
    provider=RetryProvider([Phind, FreeChatgpt, Liaobots], shuffle=False))
# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Target user and predefined responses
target = "saadii"
responses = [
    "BEST FRIEND <3", "KESA HAI JAANI", "CUTEST", "BOHAT PYARA LAG RHA HAI",
    "FLASHBANG"
]


# On bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


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
        story_request = input_text

        # Generate the response from the AI API

        # Generate story based on keywords and user's name
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": story_request
            }],
        )
        story = response.choices[0].message.content

        # Send the generated response to the Discord channel
        await ctx.send(story)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run(BOT_TOKEN)
