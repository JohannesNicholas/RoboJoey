#Handles most of the code for the checking in assignment in ZAT113 
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import discord # pycord
import db_handler as db
import asyncio


# When a message is sent anywhere
async def message(message):

    #ignore messages in other channels
    if message.channel.id not in [994167372942413906, 994121873816293407]:
        return

    #ignore messages from bots
    if message.author.bot:
        return

    #if we don't have the student id
    if db.get_student_id(message.author.id) == 0:
        #ask the user for their student id
        await message.channel.send(f"""Thank you <@{message.author.id}> for your check in!
I don't seem to have your student ID yet.""", 
        view=View(check_in_msg=message))

    else:
        await message.add_reaction('🎫')


#the view for the replies to the check in message
class View(discord.ui.View):
    check_in_msg = None

    #initialization
    def __init__(self, check_in_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_in_msg = check_in_msg

        supportButton = discord.ui.Button(label='What is my student ID?', style=discord.ButtonStyle.url, url='https://askus.utas.edu.au/app/answers/detail/a_id/1060/~/what-is-my-utas-student-id-number%3F')
        self.add_item(supportButton)

    @discord.ui.button(label="Enter student ID", style=discord.ButtonStyle.primary) # Create a button
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Enter student ID", check_in_msg=self.check_in_msg))



# the modal for entering student IDs
class MyModal(discord.ui.Modal):
    check_in_msg = None

    def __init__(self, check_in_msg, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.check_in_msg = check_in_msg
    
        self.add_item(discord.ui.InputText(label="Student id", placeholder="123456", min_length=6, max_length=6))

    async def callback(self, interaction: discord.Interaction):
        
        #check the student id
        sid = self.children[0].value
        if not sid.isdigit() or len(sid) != 6:
            #tell the user they entered an invalid student id
            await interaction.response.send_message(f"'{sid}' does not seem to be a student ID", ephemeral=True)
            return 


        db.set_student_id(interaction.user.id, int(sid))#save the student id
        await interaction.response.send_message(f"Thank you <@{interaction.user.id}> for your student ID", ephemeral=True)
        
        #if the user who checked in entered their student id
        if interaction.user.id == self.check_in_msg.author.id:
            await self.check_in_msg.add_reaction('🎫')
            await interaction.message.delete()

