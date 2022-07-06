import discord
import secrets

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[994167372090966016])
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run(secrets.botToken)