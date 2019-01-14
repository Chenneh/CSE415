# Shrink3.py
# A conversational "doctor" simulation modelled loosely
# after J. Weizenbaum's ELIZA.
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version of the program runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

from re import *  # Loads the regular expression module.


def Shrink():
    # Shrink is the top-level function, containing the main loop.
    print('They call me the Shrink.')
    print('With all due respect, I am not ELIZA.')
    print('Welcome to my sofa!')
    print('So what is your problem?')
    while True:
        the_input = input('TYPE HERE:>> ')
        if match('bye', the_input):
            print('Goodbye!')
            return
        wordlist = split(' ', remove_punctuation(the_input))
        # undo any initial capitalization:
        # wordlist[0] = wordlist[0].lower()
        [item.lower() for item in wordlist]
        mapped_wordlist = you_me_map(wordlist)
        mapped_wordlist[0] = mapped_wordlist[0].capitalize()
        respond(the_input, wordlist, mapped_wordlist)


def introduce():
    return '''Hi, I am ...'''
    #I am programmed by Chen Bai whom can be contacted by chenb@uw.edu.
    #What can I do for you?'''


def agentName():
    return "Shrink"


def respond(the_input):
    if match('bye', the_input):
        print('Goodbye!')
        return
    wordlist = split(' ', remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0] = wordlist[0].lower()
    # [item.lower() for item in wordlist]
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()
    if wordlist[0] == '':
        return ("Please say something.")

    if wordlist[0:2] == ['i', 'am']:
        return ("Please tell me why you are " + \
              stringify(mapped_wordlist[2:]) + '.')

    if wpred(wordlist[0]):
        return ("You tell me " + wordlist[0] + ".")

    if wordlist[0:2] == ['i', 'have']:
        return ("How long have you had " + \
              stringify(mapped_wordlist[2:]) + '.')

    if wordlist[0:2] == ['i', 'feel']:
        return ("I sometimes feel the same way.")

    if 'because' in wordlist:
        return ("Is that really the reason?")

    if 'yes' in wordlist:
        return ("How can you be so sure?")

    if wordlist[0:2] == ['you', 'are']:
        return ("Oh yeah, I am " + \
              stringify(mapped_wordlist[2:]) + '.')

    if verbp(wordlist[0]):
        return ("Why do you want me to " + \
              stringify(mapped_wordlist) + '?')

    if wordlist[0:3] == ['do', 'you', 'think']:
        return ("I think you should answer that yourself.")

    if wordlist[0:2] == ['can', 'you'] or wordlist[0:2] == ['could', 'you']:
        return ("Perhaps I " + wordlist[0] + ' ' + \
              stringify(mapped_wordlist[2:]) + '.')

    if 'dream' in wordlist:
        return ("For dream analysis see Freud.")

    if 'love' in wordlist:
        return ("All's fair in love and war.")

    if 'no' in wordlist:
        return ("Don't be so negative.")

    if 'maybe' in wordlist:
        return ("Be more decisive.")

    if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        return (stringify(mapped_wordlist) + '.')

    return punt()


def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)


# punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")


def remove_punctuation(text):
    # Returns a string without any punctuation. improved from original
    # return sub(punctuation_pattern, '', text)
    table = str.maketrans("!()-[]{};:'\"\,<>./?@#$%^&*_~", 28 * " ")
    print(text.translate(table))
    return text.translate(table)


def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when', 'why', 'where', 'how'])


def dpred(w):
    'Returns True if w is an auxiliary verb.'
    return (w in ['do', 'can', 'should', 'would'])


PUNTS = ['Please go on.',
         'Tell me more.',
         'I see.',
         'What does that indicate?',
         'But why be concerned about it?',
         'Just tell me how you feel.']

punt_count = 0


def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]


CASE_MAP = {'i': 'you', 'I': 'you', 'me': 'you', 'you': 'me',
            'my': 'your', 'your': 'my',
            'yours': 'mine', 'mine': 'yours', 'am': 'are'}


def you_me(w):
    # Changes a word from 1st to 2nd person or vice-versa.
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result


def you_me_map(wordlist):
    # Applies YOU-ME to a whole sentence or phrase.
    return [you_me(w) for w in wordlist]


def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])


# Shrink()  # Launch the program.
