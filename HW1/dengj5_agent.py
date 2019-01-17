from re import *  # Loads the regular expression module.
import random


def main():
    print(introduce())
    while True:
        the_input = input('TYPE HERE:>> ')
        print(respond(the_input))


def introduce():
    result = ''
    result += "Hi, I am a happy fat boy who's hungry every day all the time \n"
    result += "My name is Peter Porker \n"
    result += "Besides sleeping, I am either eating or thinking about what to eat for my next meal \n"
    result += "please ask me questions about food or eat, that's everything I know \n"
    result += "I am programmed by Jie Deng you can contact him at dengj5@uw.edu \n"
    result += "Lets start talking \n"
    return result


def agentName():
    return "Peter Porker"


# user
# question 1
time_greet = ['morning', 'afternoon', 'evening']
general_greet = ['Hi', 'hi', 'Hello', 'hello']
general_greet_reply = ['Hi~~~~~~~', 'Hiiiiiiiiiii', 'Hello~~~~~~~~~', 'Helloooooooooo', 'Nice to meet you!!!!!!']

# question 2
favourite_food = ['hotpot', 'cheese burger', 'French fries', 'basil chicken', 'big mac', 'chicken nuggets', 'donuts',
                  'beef', 'sausage']
favourite_drink = ['sprite', 'Fanta', 'coke']
cyc_drink_list = ['wine', 'whiskey', 'cocktail', 'apple juice']
hate_food = ['']

foodquestion_1 = ['food', 'like']
foodquestion_2 = ['food', 'favourite']
foodquestion_3 = ['like', 'eat']

drinkquestion_1 = ['drink', 'like']
drinkquestion_2 = ['drink', 'favourite']
drinkquestion_3 = ['like', 'drink']

order_count = 0
food_quantity = [5, 6, 7, 8, 9]

greet = 0
user_major = ''
user_favourite_food = ''
user_favourite_drink = ''
drink_cyc_count = 0

order_pattern_count = 0

wrong_input_response = ['sorry I can not understand', 'can you rephrase it', 'that is beyond my intelligence']
wrong_input_count = 0

quantity_response = ['I\'m feeling starving right now, please get me ', 'I\'m super hungry, how about ',
                     'I haven\'t eat for an hour! So, I\'m gonna have ', 'my stomach is rambling, can I get ']
quantity_pattern = 0
order_food_pattern = 0
order_response_pattern = ['Today is a good day, maybe some ', 'Let me think about it, do you have ']


last_order = ''
not_on_list = []

ordered = []
order_questioning = ['i\'d like ', 'may I get ', 'and some ', 'i want ']
order_questioning_count = 0


def respond(the_input):
    the_input = the_input.lower()
    wordlist = split(' ', remove_punctuation(the_input))

    global order_count
    global greet
    global user_major
    global user_favourite_drink
    global user_favourite_food
    global drink_cyc_count
    global wrong_input_count
    global quantity_pattern
    global order_food_pattern
    global last_order
    global not_on_list
    global order_questioning_count

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
    if set(foodquestion_1) <= set(wordlist) or set(foodquestion_2) <= set(wordlist) or \
            set(foodquestion_3) <= set(wordlist):
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
    if set(drinkquestion_1) <= set(wordlist) or set(drinkquestion_2) <= set(wordlist) or \
            set(drinkquestion_3) <= set(wordlist):
        reply = ''
        reply += 'I drink iced coke everyday' + '\n'
        reply += 'and when I am down I drink beer' + '\n'

        # cyclic response 2
        # cyclic chosen a third favourite drink if asked repeatedly
        if drink_cyc_count == 4:
            drink_cyc_count = 0
        reply += 'sometimes I drink ' + cyc_drink_list[drink_cyc_count] + '\n'
        drink_cyc_count += 1

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

    # end
    # "memory" feature
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
        random_food = random.choice(favourite_food)
        while random_food in ordered:
            random_food = random.choice(favourite_food)

        ordered.append(random_food)
        last_order = random_food
        reply = 'do you serve ' + random_food        # order first food
        return reply

    # 2 food quantity
    if wordlist[0:2] == ['how', 'many']:
        if quantity_pattern >= 4:
            quantity_pattern = 0
            re_part1 = quantity_response[quantity_pattern]
        else:
            re_part1 = quantity_response[quantity_pattern]
            quantity_pattern += 1
        return re_part1 + str(random.choice(food_quantity))  # order random amount

    # 3 continue order
    continue_order = ['is', 'that', 'all']
    confirm = ['no', 'problem']
    if ('else' in wordlist) or ('next' in wordlist) or (set(continue_order) <= set(wordlist)) or \
            (set(confirm) <= set(wordlist)):
        reply = ''
        if order_questioning_count >= 3:
            order_questioning_count = 0
            order_start = order_questioning[order_questioning_count]
        else:
            order_start = order_questioning[order_questioning_count]
            order_questioning_count += 1
        if order_count == 4:
            reply += 'That\'s all'
        elif order_count == 3:
            random_drink = random.choice(favourite_drink)
            ordered.append(random_drink)
            reply += order_start + random_drink  # order one drink
        else:
            random_food = random.choice(favourite_food)
            while random_food in ordered:
                random_food = random.choice(favourite_food)
            ordered.append(random_food)
            last_order = random_food
            reply += order_start + random.choice(favourite_food)   # order four food
        order_count += 1

        return reply

    # 4 if order not in menu
    if 'sorry' in wordlist:
        ordered.append(last_order)
        not_on_list.append(last_order)
        order_count = max(0, order_count - 1)  # food not in menu, order failed
        reply = ''
        order_response = order_response_pattern[order_food_pattern]
        order_food_pattern = 1 - order_food_pattern

        if order_count == 3:
            reply += 'That\'s all, plz make my order fast, I am super hungry right now'
        elif order_count == 2:
            random_drink = random.choice(favourite_drink)
            while random_drink in ordered:
                random_drink = random.choice(favourite_drink)
            ordered.append(random_drink)
            last_order = random_drink
            reply += order_response + random.choice(favourite_drink)
        else:
            random_food = random.choice(favourite_food)
            while random_food in ordered:
                random_food = random.choice(favourite_food)
            last_order = random_food
            ordered.append(random_food)
            reply += order_response + random_food
        order_count += 1
        return reply

    # 5 total price verify
    if 'ordered' in wordlist and 'correct' in wordlist:
        reply = 'Yes. Thank you very much.'
        if len(not_on_list) != 0:
            random_suggestion = random.choice(not_on_list)
            reply += 'by the way, I suggest you add ' + random_suggestion + ' to your menu, I really love it'
        return reply

    # 6 final order confirmation
    if 'sure' in wordlist:
        return 'yes'

    # 7 confirmed
    if 'total' in wordlist:
        return 'Thanks'

    # cyclic response 2
    if wrong_input_count == 3:
        wrong_input_count = 0
    reply = wrong_input_response[wrong_input_count]
    wrong_input_count += 1
    return reply + ', please say something else'  # invalid input


def remove_punctuation(text):
    return sub(punctuation_pattern, '', text)


def stringify(wordlist):
    return ' '.join(wordlist)


punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

# introduce()
# main() # Launch the program.


