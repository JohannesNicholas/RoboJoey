import requests
from secrets import bloom_token, ai_chat_channels

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": f"Bearer {bloom_token}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

class Conversation:
    """Class used to store conversation data"""

    priming = """Human: Hello
Robo-Joey: Hello, how are you?
Human: I am good! Yourself?
Robo-Joey: I am doing quite well
Human: What is your favorite league of legends champion?
Robo-Joey: I like the champion called  Jinx
Human: What is your favorite movie?
Robo-Joey: Star Wars
Human: What is your favorite food?
Robo-Joey: pineapple pizza
Human: Who is the best F1 driver?
Robo-Joey: Lewis Hamilton.
Human: What is the quadratic equation?
Robo-Joey: ax^2 + bx + c = 0
Human: how do you write hello world in python?
Robo-Joey: print("Hello World")
Human: what is the difference between a variable and a constant?
Robo-Joey: a variable is a value that can be changed, a constant is a value that cannot be changed.
Human: robo joey do we live in a society?
Robo-Joey: yes we do.
Human: Robo-Joey what does "lol" mean
Robo-Joey: League of Legends or Laugh Out Loud
Human: Hi
Robo-Joey: Hello, how are you?
Human: I am Great!
Robo-Joey: That's fantastic!
""" #priming used in every conversation to keep style consistent

    history = "" #stores the conversation transcript history 

    
    def ask_ai(self, question, username):
        """Ask the bloom AI a question and return the answer"""

        prompt = self.priming + self.history + username + ": "+ question + "\nRobo-Joey: " #text sent to ai


        #print(f"Prompt: {prompt}")
        output = query({  "inputs": prompt, }) #get AIs response

        #extract the answer from the output
        generated = output[0]['generated_text'].replace(prompt, "") #text on the end of the 

        #prune any extra generated lines
        if "\n" in generated:
            singleLine = generated.split("\n")[0]
        else:
            singleLine = generated

        self.history += username + ": "+ question + "\nRobo-Joey: " + singleLine + "\n" #add the response to the conversation history


        #remove repetitions to stop bot from getting stuck in a loop
        if len(set(self.history.split("\n"))) < len(self.history.split("\n")): #if there are any repetitions
            self.history = "" #Wipe the history

        #limit the length of history to one response
        while len(self.history.split("\n")) > 8:
            #remove the first 2 lines
            self.history = self.history.split("\n",2)[2]

        #print(f"History: {self.history}")

        return singleLine



    def handle_message(self, message):
        """Handle a message to see if it is a question for the AI"""

        if message.channel.id not in ai_chat_channels: #if the channel is not in the list of channels to listen to
            return None

        #ignore messages from bots
        if message.author.bot:
            return None
        
        return self.ask_ai(message.content, "Human") #ask the AI the question


if __name__ == "__main__":
    print("Hello, I am Robo-Joey. Ask me a question:")
    conversation = Conversation()
    while True:
        question = input("> ")
        print(conversation.ask_ai(question, "Joey"))