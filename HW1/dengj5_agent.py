from re import *  # Loads the regular expression module.
import random


def main():
    print(introduce())
    while True:
        the_input = input('TYPE HERE:>> ')
        print(respond(the_input))


def introduce():
    result = ''
    result += "Hi, I am a happy fat nerd who's hungry every day \n"
    result += "My name is Peter Porker \n"
    result += "Besides study, I am either eating or thinking about what to eat for my next meal \n"
    result += "please ask me questions about food or eat, that's everything I know \n"
    result += "I am programmed by Jie Deng you can contact him by dengj5@uw.edu \n"
    result += "Lets start talking \n"
    result += "you can ask me questions about food or study \n"
    return result


def agentName():
    return "Peter Porker"


# user
# question 1
time_greet = ['morning', 'afternoon', 'evening']
general_greet = ['Hi', 'hi', 'Hello', 'hello']
general_greet_reply = ['Hi~~~~~~~', 'Hiiiiiiiiiii', 'Hello~~~~~~~~~', 'Helloooooooooo', 'Nice to meet you!!!!!!']

# question 2
favourite_food = ['hotpot', 'cheese burger', 'French fries', 'basil chicken', 'big mac', 'chicken nuggets']
favourite_drink = ['sprite', 'doctor pepper', 'beer', 'Fanta', 'coke', 'milkshake']
hate_food = ['']

foodquestion_1 = ['food', 'like']
foodquestion_2 = ['food', 'favourite']
foodquestion_3 = ['like', 'eat']

drinkquestion_1 = ['drink', 'like']
drinkquestion_2 = ['drink', 'favourite']
drinkquestion_3 = ['like', 'drink']

order_count = 0

food_quantity = [5, 6, 7, 8, 9]


# partner(MCDonald's clerk)
time_p = ["morning", "afternoon", "evening"]
intro = [["I", "am"], ["hi", "I", "am"], ["my", "name", "is"], ["hi", "my", "name", "is"]]
hello = ["hello", "hi"]
menu = ["cheese", "burger", "big", "mac", "chicken", "nugget", "french", "fries", "coke"]
menu_real = ["cheese burger", "big mac", "chicken nugget", "french fries", "coke"]
end = ["that", "s", "all"]
confirm = ["Ok, got you", "Nice Choice", "Anything else?"]
uncertain = ["Sorry, I'm not sure, what do you mean.", "Pardon", "Would you make mind rephrase it?"]
leave = {"bye": "bye bye", "goodbye": "see you", "have a nice day": "you too"}
order = {"cheese burger": 0, "big mac": 0, "chicken nugget": 0, "french fries": 0, "coke": 0}
y_step = 0  # 0: nothing
n_step = 0
more_less = 0  # 0:more, 1: less # 2: not change
conf = 0
uncert = 0
price = {"cheese burger": 10, "big mac": 20, "chicken nugget" : 10, "french fries" : 5, "coke": 3}

greet = 0
user_major = ''
user_favourite_food = ''
user_favourite_drink = ''


def respond(the_input):
    the_input = the_input.lower()
    wordlist = split(' ', remove_punctuation(the_input))

    global order_count
    global greet
    global user_major
    global user_favourite_drink
    global user_favourite_food

    # 1 no input
    if wordlist[0] == '':  # empty input from user
        return "Can you say something plz"

    # 2 greeting
    if greet == 0:
        for i in range(0, 3):
            if time_greet[i] in wordlist:  # reply to greeting
                greet = 1
                return str('Good ' + time_greet[i] + '~~~~~~~~~~~~')

    if (wordlist[0] in general_greet) and greet == 0:
        greet = 1
        random_greeting = random.choice(general_greet_reply)
        return str(random_greeting)

    # 3 favourite food
    if set(foodquestion_1) <= set(wordlist) or set(foodquestion_2) <= set(wordlist) or set(foodquestion_3) <= set(wordlist):
        reply = ''
        favourite_foods = []
        for i in range(0, 3):
            favourite_foods.append(random.choice(favourite_food))

        reply += 'I like eating ' + favourite_foods[0] + '\n'
        reply += 'I also enjoy eating ' + favourite_foods[1] + '\n'
        reply += 'and I am a huge fan of ' + favourite_foods[2]
        print(reply)
        print('what is your favourite food? plz pnly enter one')
        user_favourite_food = input()
        return 'Nice! I like ' + user_favourite_food + ' as well'

    # 4 favourite drink
    if set(drinkquestion_1) <= set(wordlist) or set(drinkquestion_2) <= set(wordlist) or set(drinkquestion_3) <= set(wordlist):
        reply = ''
        reply += 'I drink iced coke everyday' + '\n'
        reply += 'and when I am down I drink beer' + '\n'
        print(reply)
        print('what do you drink most?')
        user_favourite_drink = input()

        return 'Nice! I like ' + user_favourite_drink + ' as well'

    # 5 hate food
    hate_food1 = ['don\'t', 'like']
    hate_food2 = ['do', 'not', 'like']
    hate_food3 = ['hate']
    if set(hate_food1) <= set(wordlist) or set(hate_food2) <= set(wordlist) or set(hate_food3) <= set(wordlist):
        reply = ''
        reply += 'I don\'t like tomatoes'
        return reply

    # 6 health discussion
    if ('health' or 'healthy') in wordlist:
        reply = 'Eat whatever you want' + '\n'
        reply += 'Drink whatever you want' + '\n'
        reply += 'Life is short and be merry!'
        return reply

    # 7 study discussion
    # what are you studying
    if 'studying' in wordlist or 'major' in wordlist:
        print('Electrical and computer engineering')
        print('what are you studying?')
        major_input = input()
        user_major = str(major_input)
        return 'oh, that\'s a nice one, I like that'

    # what are your favourite books?
    # what are you interested in?

    # 8 end
    if 'bye' in wordlist or (('see' in wordlist) and ('you' in wordlist)):
        reply = 'see u' + '\n'
        if user_major != '':
            reply += 'next time we can study ' + user_major + ' together' + '\n'
        if user_favourite_food != '':
            reply += 'next time we can eat ' + user_favourite_food + ' together' + '\n'
        if user_favourite_drink != '':
            reply += 'next time we can drink ' + user_favourite_drink + ' together' + '\n'

        reply += 'have a nice day'
        return reply


    # ###############################
    # conversation with another agent
    # 1 order first food
    if ('order' and 'make') in wordlist:
        order_count += 1
        reply = 'can I get ' + random.choice(favourite_food)        # order first food
        return reply

    # 2 food quantity
    if wordlist[0:2] == ['how', 'much']:
        return str(random.choice(food_quantity))                    # oder one food for a random amount

    # 3 continue order
    continue_order = ['is', 'that', 'all']
    if ('else' in wordlist) or ('next' in wordlist) or (set(continue_order) <= set(wordlist)):
        reply = ''
        if order_count == 5:
            reply += 'That\'s all'
        elif order_count == 4:
            reply += 'can I get ' + random.choice(favourite_drink)  # order one drink
        else:
            reply += 'can I get ' + random.choice(favourite_food)   # order four food
        order_count += 1

        return reply

    # 4 if order not in menu
    if 'sorry' in wordlist:
        order_count = max(0, order_count - 1)  # food not in menu, order failed
        reply = ''
        if order_count == 5:
            reply += 'That\'s all, plz make my order fast, I am super hungry right now'
        elif order_count == 4:
            reply += 'ok then, can I get ' + random.choice(favourite_drink)
        else:
            reply += 'ok then, can I get ' + random.choice(favourite_food)
        order_count += 1
        return reply

    # 5 total price verify
    if 'ordered' in wordlist and 'correct' in wordlist:
        reply = 'Yes. Thank you very much'           # confirm order
        return reply

    if 'total' in wordlist:
        return "Thanks"

    # 6 final order confirmation
    if 'sure' in wordlist:
        return 'yes'

    return 'please say something else, I can not really understand you'  # invalid input


def remove_punctuation(text):
    return sub(punctuation_pattern, '', text)


def stringify(wordlist):
    return ' '.join(wordlist)


punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")


introduce()
# main() # Launch the program.


