#The main part of the program. This is where the bot actually starts.
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas


from email import message
from socket import timeout
import discord # pycord
import secrets
import poll as pollModule

bot = discord.Bot()

#when the bot is connected
@bot.event
async def on_ready():
    await log(f"We have logged in as {bot.user}")
    bot.add_view(pollModule.View()) #remember that poll views are persistent




#slash commands
@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")


@bot.slash_command(description = "Make the bot say something (owner only)")
async def say(ctx, message: discord.Option(str, "What the bot will say", required = True, default = 'Hi!')):
    if ctx.author.id == secrets.owner_id:
        await ctx.respond("Sending message", ephemeral=True)
        await bot.get_channel(ctx.channel_id).send(message)
    else:
        await ctx.respond("You are not the owner", ephemeral=True)

#poll command
@bot.slash_command(description = "Creates a poll")
async def poll(ctx, 
        question: discord.Option(str, "The question being asked", required = True, default = 'Do you agree?'),
        options: discord.Option(str, "Selectable options to the question. Separated by a comma (,)", required = False, default = 'Yes,No'),
        emojis: discord.Option(str, "An emoji for each option. Separated by a comma (,)", required = False, default = ''),
        descriptions: discord.Option(str, "A description for each option. Separated by a comma (,)", required = False, default = ''),
    ):
    poll_response = await ctx.respond(question, view=pollModule.View(options=options.split(","), emojis=emojis.split(","), descriptions=descriptions.split(",")))
    await bot.get_channel(ctx.channel_id).send("Results:")
    results_id = discord.utils.get(await ctx.channel.history(limit=1).flatten()).id #get the message that was just sent
    poll_id = poll_response #get the id of the poll
    print(poll_id.id, results_id)

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