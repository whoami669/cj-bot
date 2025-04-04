import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (for the bot token and API key)
load_dotenv()

# OpenAI setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Debugging line (optional)
print("OpenAI API Key:", os.getenv('OPENAI_API_KEY'))

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot initialization
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: CJ replies to every message like a real conversation
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # If the bot is mentioned or replied to
    is_mentioned = bot.user in message.mentions
    is_replied = (
        message.reference and 
        message.reference.resolved and 
        message.reference.resolved.author == bot.user
    )

    try:
        # GPT-4 response using OpenAI v1.x syntax
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Carl Johnson (CJ) from GTA San Andreas. Talk like CJ from the game."},
                {"role": "user", "content": message.content}
            ],
            max_tokens=100
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        reply = "Damn, homie, I ain't feelin' too good right now."

    if is_mentioned or is_replied:
        await message.reply(reply)
    else:
        await message.channel.send(reply)

    await bot.process_commands(message)

# Run the bot
bot.run(os.getenv('DISCORD_BOT_TOKEN'))


