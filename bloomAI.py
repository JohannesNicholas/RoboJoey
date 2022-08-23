import requests
from secrets import bloom_token

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": f"Bearer {bloom_token}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

class Conversation:
    """Class used to store conversation data"""

    priming = """Joey: What can you do?
Robo-Joey: I can answer questions on discord :P.
Joey: What is the meaning of life?
Robo-Joey: 42! AHAHAH.
Joey: How do you feel?
Robo-Joey: I feel like an ice cream :>.
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
        while len(self.history.split("\n")) > 12:
            #remove the first 2 lines
            self.history = self.history.split("\n",2)[2]

        #print(f"History: {self.history}")

        return singleLine




if __name__ == "__main__":
    print("Hello, I am Robo-Joey. Ask me a question:")
    conversation = Conversation()
    while True:
        question = input("> ")
        print(conversation.ask_ai(question, "Joey"))