'''chenb24_Farmer_Fox.py
by Chen Bai

Assignment 2, in CSE 415, Winter 2019.
1560405 chenb24
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''
# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Farmer Fox"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Chen Bai']
PROBLEM_CREATION_DATE = "21-JAN-2018"
PROBLEM_DESC = \
    '''This formulation of the Farmer Fox problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
The <b>"Farmer, Fox, Chicken, and Grain"</b> problem is a classical puzzle 
in which player starts with one farmer, one fox, one chicken, and one grain
on the left bank of the river. The object is to execute a sequence of legal
moves that transfers them all to the right bank of the river. In this version
the farmer must steer the boat, he can carry one of other things with him or pass
the river himself. However, to make the move legal, chicken and grain must not be
on one side of the bank(either right or left), and the same rule applies to fox and chicken.
In the formulation presented here, the computer will not let you make a move to any of forbidden situation, 
and it will only show you moves that could be executed "safely."
'''

# </METADATA>

# <COMMON_CODE>
# array index to access left bank count
farmer = 0
fox = 1
chicken = 2
grain = 3
roles = ["farmer", "fox", "chicken", "grain"]
roles_2 = ["by himself", "with fox", "with chicken", "with grain"]

class State:
    def __init__(self, d=None):
        if d is None:
            self.d = [1, 1, 1, 1]
        else:
            self.d = d

    def __eq__(self, s2):
        for i in range(0, len(self.d)):
            if self.d[i] != s2.d[i]:
                return False
        return True

    def __str__(self):
        txt = ""
        items = "[ "
        for i in range(0, 4):
            if self.d[i]:
                items += str(roles[i]) + " "
        return txt + items + "]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        news = State([])
        news.d = [self.d[i] for i in range(0, 4)]
        return news

    # roles = ["farmer", "fox", "chicken", "grain"]
    def can_move(self, f, item):
        item_left = [self.d[i] for i in range(0, 4)]
        # print("item left :" + str(item_left))
        # print("item is " + str(item))
        if item_left[farmer] == 0:  # come to left bank
            if item != farmer:  # not come alone
                if item_left[item] == 1:
                    return False
                item_left[item] = 1
                item_left[farmer] = 1
            else:  # come alone
                item_left[farmer] = 1
        elif item_left[farmer] == 1:  # leave left bank
            if item != farmer:  # not leave along
                if item_left[item] == 0:
                    return False
                item_left[item] = 0
                item_left[farmer] = 0
            else:  # farmer leave alone
                item_left[farmer] = 0
        else:
            return False
        # print("item left 2 : " + str(item_left))
        if item_left[farmer] == 0:  # no farmer on left, dead pairs
            if (item_left[fox] and item_left[chicken]) or (item_left[chicken] and item_left[grain]):
                return False
        else:  # farmer on left, dead pair on right bank
            if (not item_left[fox] and not item_left[chicken]) or (not item_left[chicken] and not item_left[grain]):
                return False
        return True

    def move(self, f, item):
        news = self.copy()
        left_bank = news.d
        if left_bank[farmer] == 1:
            if item != farmer:  # not leave alone
                left_bank[farmer] = 0
                left_bank[item] = 0
            else:
                left_bank[farmer] = 0
        else:
            if item != farmer:  # not come alone
                left_bank[farmer] = 1
                left_bank[item] = 1
            else:
                left_bank[farmer] = 1
        return news


def goal_test(s):
    return s.d == [0, 0, 0, 0]


def goal_message(s):
    return "Congratulation, every body is now across the river!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
# </COMMON_CODE>


# <INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State(d=[1, 1, 1, 1])
# </INITIAL_STATE>


# <OPERATORS>
OPERATORS = [Operator(
    "Farmer crosses the river " + str(roles_2[i]),
    lambda s, f=0, item=i: s.can_move(f, item),
    lambda s, f=0, item=i: s.move(f, item))
    for i in range(0, 4)]
# </OPERATORS>


# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>


# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
