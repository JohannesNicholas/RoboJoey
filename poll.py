#Handles most of the code for polling 
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas


import discord
import db_handler as db

#the view for a poll message
class View(discord.ui.View):
    selectOptions = []# the list of options from which users can choose, a required field
    bot=None#the bot

    #initialization
    def __init__(self, options=["yes", "no"], emojis=[], descriptions=[], bot=None):
        self.selectOptions.clear()

        for i in range(len(options)):
            option = options[i]

            emoji = None
            if i < len(emojis):
                emoji = emojis[i].strip()
            if emoji == "":
                emoji = None

            description = None
            if i < len(descriptions):
                description = descriptions[i]
            
            self.selectOptions.append(
                discord.SelectOption(
                    label=option, 
                    value=str(i),
                    description=description,
                    emoji=emoji
                )
            )
        super().__init__(timeout=None) #persistent view


    @discord.ui.select(# the decorator that lets you specify the properties of the select menu
        placeholder = "Select", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = selectOptions,
        custom_id="select-1"
    )
    
    async def select_callback(self, select, interaction: discord.Interaction): # the function called when the user is done selecting options
        await interaction.response.send_message("Thank you for your selection!", ephemeral=True)
        db.save_poll_result(interaction.message.id, interaction.user.id, select.values[0])

        results_id, results = db.get_poll_results(int(interaction.message.id))
        results_msg = await interaction.channel.fetch_message(results_id)

        lines = results_msg.content.split("\n")
        for i in range(len(lines)): #for each line in the message
            line_end = lines[i].split(" - ")[1] if " - " in lines[i] else lines[i] #get the end of the line
            bar = "" #the bar to be added to the line
            if i < len(results):
                for j in range(results[i]): #for each vote
                    bar += "█"
                bar += " " + str(results[i])
            else:
                bar = "0"

            lines[i] = bar + " - " + line_end #update the line


        

        await results_msg.edit(content="\n".join(lines))


async def createPoll(bot, ctx, question, options, emojis, descriptions):
    """Creates a poll"""
    
    await ctx.respond(question, view=View(options=options.split(","), emojis=emojis.split(","), descriptions=descriptions.split(","), bot=bot))
    
    results_text = ""
    for i in range(len(options.split(","))):
        results_text += "0 - "
        if i < len(emojis.split(",")): #emoji if there is one
            results_text += emojis.split(",")[i] + ""

        results_text += options.split(",")[i] + "\n"
        

    await bot.get_channel(ctx.channel_id).send(results_text)

    messages = await ctx.channel.history(limit=2).flatten() #get those two sent messages

    poll_id = messages[1].id #the message id of the poll sent by the bot
    results_id = messages[0].id #the message of the results, directly after the poll

    db.save_poll(poll_id, results_id)
    await log(f"Created poll {poll_id}, results {results_id}")

        
        


