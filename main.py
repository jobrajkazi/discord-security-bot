import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Whitelist (Admins immune to bot)
WHITELIST = {YOUR_DISCORD_USER_ID_HERE}   # ← Change this

BAD_WORDS = ["badword1", "badword2", "fuck", "shit", "bitch"]  # Add more words

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot or message.author.id in WHITELIST:
        await bot.process_commands(message)
        return

    content = message.content.lower()

    # Profanity Filter
    if any(word in content for word in BAD_WORDS):
        await message.delete()
        try:
            await message.author.send(f"🚫 Your message was removed for prohibited content in **{message.guild.name}**.")
        except:
            pass
        return

    await bot.process_commands(message)

# Commands (Only Admins can use)
@bot.command()
@commands.has_permissions(administrator=True)
async def whitelist(ctx, user: discord.Member):
    WHITELIST.add(user.id)
    await ctx.send(f"✅ {user} added to whitelist.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user: discord.Member, *, reason="No reason given"):
    await user.ban(reason=reason)
    await ctx.send(f"✅ Banned {user} | Reason: {reason}")

# Add more commands later (kick, timeout, unban, etc.)

bot.run(os.getenv("TOKEN"))
