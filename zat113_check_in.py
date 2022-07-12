#Handles most of the code for the checking in assignment in ZAT113 
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import discord # pycord


# When a message is sent anywhere
async def message(message):

    #ignore messages in other channels
    if message.channel.id not in [994167372942413906, 994121873816293407]:
        return

    #ignore messages from bots
    if message.author.bot:
        return

    #ask the user for their student id
    await message.channel.send(f"""Thank you <@{message.author.id}> for your check in! 
I don't seem to have you student ID yet.""", view=View(check_in_msg=message))


#the view for the replies to the check in message
class View(discord.ui.View):
    check_in_msg = None

    #initialization
    def __init__(self, check_in_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_in_msg = check_in_msg

    @discord.ui.button(label="Enter student ID", style=discord.ButtonStyle.primary) # Create a button
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Enter student ID", check_in_msg=self.check_in_msg))

# the modal for entering student IDs
class MyModal(discord.ui.Modal):
    check_in_msg = None

    def __init__(self, check_in_msg, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.check_in_msg = check_in_msg
    
        self.add_item(discord.ui.InputText(label="Student id", placeholder="123456"))

    async def callback(self, interaction: discord.Interaction):
        print(self.children[0].value)
        await self.check_in_msg.add_reaction('🎫')
        await interaction.response.send_message("Thank you!", ephemeral=True)

