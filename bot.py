import discord # pycord
import secrets
import poll as pollModule

bot = discord.Bot()

#when the bot is connected
@bot.event
async def on_ready():
    await log(f"We have logged in as {bot.user}")
    # bot.add_view(pollModule.View()) #remember that poll views are persistent


#slash commands
@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")

#poll command
@bot.slash_command()
async def poll(ctx, 
        question: discord.Option(str, "The question being asked", required = True, default = ''),
        option_a: discord.Option(str, "An answer to the question", required = False, default = ''),
        option_b: discord.Option(str, "An answer to the question", required = False, default = ''),
        option_c: discord.Option(str, "An answer to the question", required = False, default = ''),
        option_d: discord.Option(str, "An answer to the question", required = False, default = ''),
        option_e: discord.Option(str, "An answer to the question", required = False, default = ''),
    ):
    await ctx.respond("Poll: ", view=pollModule.View())

@bot.slash_command()
async def about(ctx):
    await ctx.respond("""Hi, I am a bot written in python by Johannes (Joey) Nicholas <@282428409685213184>. 
Joey takes all responsibility for my actions. 
Contact: johannes.nicholas@utas.edu.au. 
View my source code: https://github.com/JohannesNicholas/RoboJoey""")

#used to log everything
async def log(message):
    print("Log: " + message)
    await bot.get_channel(994423152924966932).send(message)


#run the bot
bot.run(secrets.botToken)