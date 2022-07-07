import datetime
import discord

#the view for a poll message
class View(discord.ui.View):
    selectOptions = []# the list of options from which users can choose, a required field

    #initialization
    def __init__(self, options=["yes", "no"], emojis=[], descriptions=[]):
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
                    value=i,
                    description=description,
                    emoji=emoji
                )
            )
        super().__init__(timeout=None) #persistent view


    @discord.ui.select(# the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = selectOptions,
        custom_id="select-1"
    )
    
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")
