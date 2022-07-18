#Handles most of the code for quizzes 
#Check .git for creation and updates history and information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import discord
import db_handler as db



async def createQuiz(bot, ctx, question, correct : int, options, emojis, descriptions):
    """Creates a quiz"""

    await ctx.respond(question, view=View(options=options.split(","), emojis=emojis.split(","), descriptions=descriptions.split(","), bot=bot))
    
    results_text = "People who got the correct answer first go:"
        

    await bot.get_channel(ctx.channel_id).send(results_text)

    messages = await ctx.channel.history(limit=2).flatten() #get those two sent messages

    quiz_id = messages[1].id #the message id of the poll sent by the bot
    results_id = messages[0].id #the message of the results, directly after the poll

    db.save_quiz(quiz_id, results_id, correct=correct)
    print(f"Created quiz {quiz_id}, results {results_id}")

 
 
#the view for a quiz message
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
        correct:int = db.get_quiz_answer(interaction.message.id)

        #respond to the user depending on if they got the correct answer
        print(f"{interaction.user.id} got {select.values[0]} correct is {correct}") 
        if int(select.values[0]) == int(correct):
            await interaction.response.send_message("Correct!", ephemeral=True)
        else:
            await interaction.response.send_message("Incorrect, try again", ephemeral=True) 


        db.save_quiz_result(interaction.message.id, interaction.user.id, select.values[0]) #save the result

        results_id, winners = db.get_quiz_results(int(interaction.message.id)) #get the results of the quiz

        results_msg = await interaction.channel.fetch_message(results_id) #get the message of the results

        results_text = "People who got the correct answer first go:\n"
        for winner in winners:
            results_text += f"<@{winner}> "

        await results_msg.edit(content=results_text)
        