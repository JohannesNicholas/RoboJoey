#The main part of the program. This is where the bot actually starts.
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import random
import discord # pycord
import secrets
import poll as pollModule
import quiz as quizModule
import db_handler as db
import zat113_check_in as checkIn


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)
db.setup()



#when the bot is connected
@bot.event
async def on_ready():
    await log(f"We have logged in as {bot.user}")

    quizzes = db.get_all_quiz_ids()
    for quiz in quizzes:
        bot.add_view(quizModule.View(bot=bot), message_id=quiz) #remember that poll views are persistent

    polls = db.get_all_poll_ids()
    for poll in polls:
        bot.add_view(pollModule.View(bot=bot), message_id=poll) #remember that poll views are persistent




class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Student id", placeholder="123456"))

    async def callback(self, interaction: discord.Interaction):
        print(self.children[0].value)
        await interaction.response.send_message("Thank you!", ephemeral=True)

class View(discord.ui.View):
    @discord.ui.button(label="Enter student ID", style=discord.ButtonStyle.primary) # Create a button
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Enter student ID"))


#when someone sends a message, any message
@bot.event
async def on_message(message):
    await checkIn.message(message)





#ping command
@bot.slash_command(description = "The delay from the discord server to the bot")
async def ping(ctx):
    await ctx.respond(str(int(bot.latency * 1000))+ "ms")


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
    await pollModule.createPoll(bot, ctx, question, options, emojis, descriptions)

#quiz command
@bot.slash_command(description = "Creates a multiple choice quiz")
async def quiz(ctx, 
            question: discord.Option(str, "The question being asked", required = True, default = 'Is this true?'),
            options: discord.Option(str, "Selectable options to the question. Separated by a comma (,)", required = False, default = 'Yes,No'),
            correct: discord.Option(int, "The correct index (starting at 0)", required = True, default = 0),
            emojis: discord.Option(str, "An emoji for each option. Separated by a comma (,)", required = False, default = ''),
            descriptions: discord.Option(str, "A description for each option. Separated by a comma (,)", required = False, default = ''),
        ):
    await quizModule.createQuiz(bot, ctx, question, correct, options, emojis, descriptions)
    


#Colors for programming club
@bot.slash_command(description = "Change your colour!",  guild_ids = [secrets.debug_guild, secrets.programming_club_guild], guild_only = True)
async def change_color(ctx : discord.ApplicationContext, color : discord.Option(str, "The color you want to change to eg: Colors.green()", required = True, default = ' ')):
    colour_roles = [role for role in ctx.guild.roles if role.name.startswith("Colors.")] # all the color roles

    #if the user has chosen an available color
    if color in [role.name for role in colour_roles]:

        #remove old colors
        for role in colour_roles:
            await ctx.author.remove_roles(role)

        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=color))
        await ctx.respond("Colour changed!", ephemeral=True)

    else:
        await ctx.respond("`" + color + "` is not available. Here are the available colors: \n" \
            + "\n".join(["`" + role.name + "`" for role in colour_roles]), ephemeral=True)

#Colorize the programming club
@bot.slash_command(description = "Assign a random color of the available 'Color.' roles uncolored members. (Admin Only)",  guild_ids = [secrets.debug_guild, secrets.programming_club_guild], guild_only = True, administrator = True)
async def colorize(ctx : discord.ApplicationContext):
    await ctx.respond("colorizing...")

    colour_roles = [role for role in ctx.guild.roles if role.name.startswith("Colors.")] # all the color roles
    members = ctx.guild.members #all members in the guild

    counter = 0
    #for all the members that dont have a color role
    async for member in ctx.guild.fetch_members(limit=150):
        print(member.name)

        if not any(role.name.startswith("Colors.") for role in member.roles):
            #assign a radom color role
            await member.add_roles(discord.utils.get(ctx.guild.roles, name=random.choice(colour_roles).name))
            await ctx.respond("Added color to " + member.name, ephemeral=True)
            counter += 1

    await ctx.channel.send(f"Done! {counter} members colorized! 🥳")


#Check_ins command
@bot.slash_command(description = "Get a CSV of all the check ins. (Staff only)",  guild_ids = [secrets.debug_guild, secrets.zat113_guild], guild_only = True)
async def check_ins(ctx : discord.ApplicationContext):

    await ctx.defer(ephemeral=True)

    #guard if the user is not staff
    if ctx.author.id not in secrets.zat113_staff:
        await ctx.respond("You are not a staff member.", ephemeral=True)
        return
        
    #send the file privately
    file = await checkIn.get_check_ins(ctx.channel_id, bot=bot)
    print(file.fp)
    await ctx.respond("check ins:", file=file, ephemeral=True)

#Manually set a students ID
@bot.slash_command(description = "Manually set a students ID in the database. (Staff only)",  guild_ids = [secrets.debug_guild, secrets.zat113_guild], guild_only = True)
async def set_student_id(ctx : discord.ApplicationContext, 
    discord_id: discord.Option(str, "The students Discord ID", required = True, default = ""),
    student_id: discord.Option(str, "The students ID", required = True, default = ""),
    ):
    if ctx.author.id not in secrets.zat113_staff:
        await ctx.respond("You are not a staff member.", ephemeral=True)
        return

    if not discord_id.isdigit():
        await ctx.respond("discord id must be an integer, right click the user and select copy ID.", ephemeral=True)
        return

    if not student_id.isdigit():
        await ctx.respond("student id must be an integer", ephemeral=True)
        return

    db.set_student_id(int(discord_id), int(student_id))
    await ctx.respond("Saved!.", ephemeral=True)
    





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