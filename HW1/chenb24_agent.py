from re import *  # Loads the regular expression module.
import random

def main():
    while True:
        the_input = input('TYPE HERE:>> ')
        print(respond(the_input))


def introduce():
    return ("Hi, I am Donald Mcsale, a McDonald's clerk \n"
            "I am programmed by Chen Bai whose NetID is 1560405 and you can contacted him by chenb@uw.edu \n"
            "What do you want today?")


def agentName():
    return "Donald Mcsale"


# invariant
time_p = ["morning", "afternoon", "evening"]
intro = [["i", "am"], ["hi", "i", "am"], ["my", "name", "is"], ["hi", "my", "name", "is"]]
hello = ["hello", "hi"]
menu = ["cheese", "burger", "big", "mac", "chicken", "nuggets", "french", "fries", "coke", "sprite", "fanta"]
menu_real = ["cheese burger", "big mac", "chicken nuggets", "french fries", "coke", "sprite", "fanta"]
price = {"cheese burger": 10, "big mac": 20, "chicken nuggets": 10, "french fries": 5,
         "coke": 3, "sprite": 3, "fanta": 3}
end = ["that", "s", "all"]
confirm = ["Ok, got you. Is that all?", "Nice Choice, what's next", "Anything else?"]
uncertain = ["Sorry, we don't serve that today.", "Sorry, we don't have that.", "Sorry, this is sold out."]
leave = {"bye": "bye bye", "goodbye": "see you", "have a nice day": "you too", "thanks": "you're welcome"}
sorry = ["No problem", "That's fine", "Never mind"]

# global variable
order = {"cheese burger": 0, "big mac": 0, "chicken nuggets": 0, "french fries": 0, "coke": 0, "sprite": 0, "fanta": 0}
y_step = 0  # 0: nothing
n_step = 0
more_less = 0
conf = 0
uncert = 0
last_food = ""
greeted = 0
order_repeat = 0


def respond(the_input):
    wordlist = prepare_wordlist(split(' ', remove_punctuation(the_input.lower())))
    global y_step
    global n_step
    global order
    global more_less
    global conf
    global uncert
    global last_food
    global greeted
    global  order_repeat
    # 1. when user want to end the dialog
    if wordlist[0] in leave:
        return

    greet_reply = ""
    if_greet = 0
    for word in wordlist:
        if word in hello:
            greet_reply += word.capitalize() + " \n"
            if_greet = 1
            greeted = update_greeted(greeted)
        if "good" in wordlist and word in time_p:
            greet_reply += "Good " + word + "\n"
            if_greet = 1
            greeted = update_greeted(greeted)
    greet_reply += ('Today we offer cheese burger, big mac, chicken nuggets, french fries, sprite, fanta and coke \n'
                    'Please make your order slowly and one choice after one.')

    if if_greet == 1:
        if greeted == 1:        # 2. first time greeting
            return greet_reply
        elif greeted == 2:      # 3. repeat greeting
            return "Greeting again, what should I do for you now?"

    if wordlist[0] == '':  # 4. empty input from user
        return "Sorry, I can't hear you"

    if (wordlist[0:2] in intro) or (wordlist[0:3] in intro):  # 5. response to introduction
        return "Nice to meet you!"

    if wordlist[0:3] == end or ("all" or "it") in wordlist:  # 6. when user indicates finished order
        return "Are you sure that's all for today? Yes(y)/No(n)"

    if wordlist[0] == "y" or wordlist[0] == "yes":  # 7. when user confirms certain question
        total = sum_price()
        if total == 0:  # Nothing ordered
            return "You ordered nothing. Please reorder"
        elif order_repeat == 0:  # repeat order - Doing memory
            order_repeat = 1
            n_step = 1
            return "You ordered " + stringify(make_final_order()) + ". Is that correct? Yes(y)/No(n)"
        else:  # confirm end order - Doing memory
            return "Thanks for your order. Your total is $" + str(total) + " Please wait for your meal there."

    if wordlist[0] == "n" or wordlist[0] == "no":  # 8. when user denies certain question
        if n_step == 0:
            return "Do you want more or reorder?"
        elif n_step == 1:
            order_repeat = 0
            n_step = 0
            clear_order()
            return "Well, please order again!"

    if ("reorder" or "again") in wordlist:  # 9. when user want to reorder
        clear_order()
        more_less = 0
        return "Ok, the order is now clear, you can now do reorder"

    if "more" in wordlist:  # 10. when user want to order more
        more_less = 0
        return "Then, let's continue."

    count = 0
    for word in wordlist:
        if word in order.keys():
            food = word
            last_food = food
            count += 1
            if count >= 2:
                last_food = ""
                return "Please, I am new here, so, tell me your choice one by one."  # 11. when user tells more than one

    for word in wordlist:   # 12. adding food to order - Doing cycle
        if any(char.isdigit() for char in word):
            num = int(word)
            order[last_food] += num
            last_food = ""
            if conf == 3:
                conf = 0
            reply = confirm[conf]
            conf += 1
            return reply

    if last_food != "":  # 13. asking for amount
        return "How much " + last_food + " do you want?"

    if "sorry" in wordlist:
        return sorry[random.randint(0, 2)]  # 14. response to apologize - Doing random

    return uncertain[random.randint(0, 2)]  # 15. default response - Doing random


def prepare_wordlist(wordlist):
    if ("cheese" and "burger") in wordlist:
        wordlist.append("cheese burger")

    if ("big" and "mac") in wordlist:
        wordlist.append("big mac")

    if ("chicken" and "nuggets") in wordlist:
        wordlist.append("chicken nuggets")

    if ("french" and "fries") in wordlist:
        wordlist.append("french fries")

    return wordlist


def remove_punctuation(text):
    # Returns a string without any punctuation. improved from original
    table = str.maketrans("!-()[]{};:'\"\,<>./?@#$%^&*_~", 28 * " ")
    # print(text.translate(table))
    return text.translate(table)


def make_final_order():
    final_order = []
    for f in order:
        if order[f] >= 1:
            final_order.append(str(order[f]))
            final_order.append(f)
    return final_order


def clear_order():
    for f in order:
        order[f] = 0


def sum_price():
    total = 0
    for f in order:
        total += order[f] * price[f]
    return total


def stringify(wordlist):
    return ' '.join(wordlist)


def update_greeted(greet_num):
    if greet_num == 0:
        greet_num = 1
    elif greet_num == 1:
        greet_num = 2
    return greet_num

main() # Launch the program.


