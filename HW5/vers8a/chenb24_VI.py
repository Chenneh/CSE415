'''chenb24_VI.py by chenb24(1560405)

Value Iteration for Markov Decision Processes.
'''

import math


# Edit the returned name to ensure you get credit for the assignment.
def student_name():
    return "Bai, Chen"  # For an autograder.


Vkplus1 = {}
Q_Values_Dict = {}


def one_step_of_VI(S, A, T, R, gamma, Vk):
    ''' S is list of all the states defined for this MDP.
   A is a list of all the possible actions.
   T is a function representing the MDP's transition model.
   R is a function representing the MDP's reward function.
   gamma is the discount factor.
   The current value of each state s is accessible as Vk[s].
   '''

    '''Your code should fill the dictionaries Vkplus1 and Q_Values_dict
   with a new value for each state, and each q-state, and assign them
   to the state's and q-state's entries in the dictionaries, as in
       Vkplus1[s] = new_value
       Q_Values_Dict[(s, a)] = new_q_value

   Also determine delta_max, which we define to be the maximum
   amount that the absolute value of any state's value is changed
   during this iteration.
   '''
    global Q_Values_Dict
    delta_max = 0
    for s in S:
        local_max = -math.inf
        for a in A:
            sum_q = 0
            for sp in S:
                sum_q += T(s, a, sp) * (R(s, a, sp) + gamma * Vk[sp])
            Q_Values_Dict[(s, a)] = sum_q
            local_max = max(local_max, sum_q)
        Vkplus1[s] = local_max
        delta_temp = abs(local_max - Vk[s])
        delta_max = max(delta_max, delta_temp)

    return Vkplus1, delta_max
    # return (Vk, 0)  # placeholder


def return_Q_values(S, A):
    '''Return the dictionary whose keys are (state, action) tuples,
   and whose values are floats representing the Q values from the
   most recent call to one_step_of_VI. This is the normal case, and
   the values of S and A passed in here can be ignored.
   However, if no such call has been made yet, use S and A to
   create the answer dictionary, and use 0.0 for all the values.
   '''
    if not Q_Values_Dict:
        for s in S:
            for a in A:
                Q_Values_Dict[(s, a)] = 0.0
    return Q_Values_Dict  # placeholder


Policy = {}


def extract_policy(S, A):
    '''Return a dictionary mapping states to actions. Obtain the policy
   using the q-values most recently computed.  If none have yet been
   computed, call return_Q_values to initialize q-values, and then
   extract a policy.  Ties between actions having the same (s, a) value
   can be broken arbitrarily.
   '''
    global Policy
    Policy = {}
    # print("the Q is: " + str(Q_Values_Dict))
    if Q_Values_Dict:
        for s in S:
            q_max = -math.inf
            action = None
            for a in A:
                if (s, a) in Q_Values_Dict:
                    q_temp = Q_Values_Dict[(s, a)]
                    if q_temp > q_max:
                        q_max = q_temp
                        action = a
            Policy[s] = action
    return Policy


def apply_policy(s):
    '''Return the action that your current best policy implies for state s.'''
    global Policy
    best = Policy[s]
    return best  # placeholder
