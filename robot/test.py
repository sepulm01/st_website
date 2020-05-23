from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot('Terminal',read_only=True)

trainer = ListTrainer(bot)

trainer.train([
    "Quiero una bebida",
    "Cual marca te gustaría",
    ])
trainer.train([
    "Una Cocacola",
    "Quieres una Cocacola sabor original o Zero",
])

trainer.train([   
    "Una Fanta",
    "Muy bien, en camino una Fanta",])
trainer.train([
    "Una Pepsi",
    "Muy bien, va una Pepsi", ])
trainer.train([
    "Una Bilz"
    "Muy bien, una Bilz para ti" ])
trainer.train([
    "Una Pap",
    "Muy bien, una Pap entonces."

])


print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        user_input = input()

        bot_response = bot.get_response(user_input)

        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
