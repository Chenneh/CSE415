#!/usr/bin/python3
'''Milestone_A_who_and_what.py
This runnable file will provide a representation of
answers to key questions about your project in CSE 415.

'''

# DO NOT EDIT THE BOILERPLATE PART OF THIS FILE HERE:

CATEGORIES = ['Baroque Chess Agent', 'Feature-Based Reinforcement Learning for the Rubik Cube Puzzle', \
              'Hidden Markov Models: Algorithms and Applications']


class Partner():
    def __init__(self, lastname, firstname, uwnetid):
        self.uwnetid = uwnetid
        self.lastname = lastname
        self.firstname = firstname

    def __lt__(self, other):
        return (self.lastname + "," + self.firstname).__lt__(other.lastname + "," + other.firstname)

    def __str__(self):
        return self.lastname + ", " + self.firstname + " (" + self.uwnetid + ")"


class Who_and_what():
    def __init__(self, team, option, title, approach, workload_distribution, references):
        self.team = team
        self.option = option
        self.title = title
        self.approach = approach
        self.workload_distribution = workload_distribution
        self.references = references

    def report(self):
        rpt = 80 * "#" + "\n"
        rpt += '''The Who and What for This Submission

Project in CSE 415, University of Washington, Winter, 2019
Milestone A

Team: 
'''
        team_sorted = sorted(self.team)
        # Note that the partner whose name comes first alphabetically
        # must do the turn-in.
        # The other partner(s) should NOT turn anything in.
        rpt += "    " + str(team_sorted[0]) + " (the partner who must turn in all files in Catalyst)\n"
        for p in team_sorted[1:]:
            rpt += "    " + str(p) + " (partner who should NOT turn anything in)\n\n"

        rpt += "Option: " + str(self.option) + "\n\n"
        rpt += "Title: " + self.title + "\n\n"
        rpt += "Approach: " + self.approach + "\n\n"
        rpt += "Workload Distribution: " + self.workload_distribution + "\n\n"
        rpt += "References: \n"
        for i in range(len(self.references)):
            rpt += "  Ref. " + str(i + 1) + ": " + self.references[i] + "\n"

        rpt += "\n\nThe information here indicates that the following file will need\n" + \
               "to be submitted (in addition to code and possible data files):\n"
        rpt += "    " + \
               {'1': "Baroque_Chess_Agent_Report", '2': "Rubik_Cube_Solver_Report", \
                '3': "Hidden_Markov_Models_Report"} \
                   [self.option] + ".pdf\n"

        rpt += "\n" + 80 * "#" + "\n"
        return rpt


# END OF BOILERPLATE.

# Change the following to represent your own information:

chumei = Partner("Yang", "Chumei", "chumeiy")
chen = Partner("Bai", "Chen", "chenb24")
team = [chumei, chen]

OPTION = '1'
# Legal options are 1, 2, and 3.

title = "Baroque Chess Agent"

approach = '''Our approach will be to read the spec thoroughly and understand
our tasks. We will do some research to first understand the rules.
We will then code our moves and develop a static evaluation function.
We will optimize our solution using alpha-beta pruning, Zobrist hashing, 
We will experiment differnet static evaluation functions to find the optimal one.'''

workload_distribution = '''Chumei will have primary responsibility for the 
static evaluation function and move generation, Chen will have primary responsibility for
the optimizations of alpha-beta pruning and Zobrist hashing. Both of us will participate
in developing a personality for the agent.'''

reference1 = '''Wikipedia article on Baroque Chess;
    URL: https://en.wikipedia.org/wiki/Baroque_chess (accessed Feb. 28, 2019)'''

reference2 = '''"Genetic Algorithms for Evolving Computer Chess Programs,
    available online at: https://arxiv.org/pdf/1711.08337.pdf'''

our_submission = Who_and_what(team, OPTION, title, approach, workload_distribution, [reference1, reference2])

# You can run this file from the command line by typing:
# python3 who_and_what.py

# Running this file by itself should produce a report that seems correct to you.
if __name__ == '__main__':
    print(our_submission.report())
