from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.spanish.greetings",
    "chatterbot.corpus.spanish.IA"
)

# Get a response to the input text 'I would like to book a flight.'
response = chatbot.get_response('Hola buenos días')

print(response)
