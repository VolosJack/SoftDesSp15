"""
Evolutionary algorithm, attempts to evolve a given message string.

Uses the DEAP (Distributed Evolutionary Algorithms in Python) framework,
http://deap.readthedocs.org

Usage:
    python evolve_text.py [goal_message]

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/evolutionary-algorithms
"""
from deap.tools import History
import matplotlib.pyplot as plt
import random
from random import randrange
import string

import numpy  # Used for statistics
from deap import algorithms
from deap import base
from deap import tools



# -----------------------------------------------------------------------------
# Global variables
#-----------------------------------------------------------------------------

# Allowable characters include all uppercase letters and space
# You can change these, just be consistent (e.g. in mutate operator)
VALID_CHARS = string.ascii_uppercase + " "

# Control whether all Messages are printed as they are evaluated
VERBOSE = True
history = History()

#-----------------------------------------------------------------------------
# Message object to use in evolutionary algorithm
#-----------------------------------------------------------------------------

class FitnessMinimizeSingle(base.Fitness):
    """
    Class representing the fitness of a given individual, with a single
    objective that we want to minimize (weight = -1)
    """
    weights = (-1.0, )


class Message(list):
    """
    Representation of an individual Message within the population to be evolved

    We represent the Message as a list of characters (mutable) so it can
    be more easily manipulated by the genetic operators.
    """

    def __init__(self, starting_string=None, min_length=4, max_length=30):
        """
        Create a new Message individual.

        If starting_string is given, initialize the Message with the
        provided string message. Otherwise, initialize to a random string
        message with length between min_length and max_length.
        """
        # Want to minimize a single objective: distance from the goal message
        self.fitness = FitnessMinimizeSingle()

        # Populate Message using starting_string, if given
        if starting_string:
            self.extend(list(starting_string))

        # Otherwise, select an initial length between min and max
        # and populate Message with that many random characters
        else:
            initial_length = random.randint(min_length, max_length)
            for i in range(initial_length):
                self.append(random.choice(VALID_CHARS))

    def __repr__(self):
        """Return a string representation of the Message"""
        # Note: __repr__ (if it exists) is called by __str__. It should provide
        #       the most unambiguous representation of the object possible, and
        #       ideally eval(repr(obj)) == obj
        # See also: http://stackoverflow.com/questions/1436703
        template = '{cls}({val!r})'
        return template.format(cls=self.__class__.__name__,  # "Message"
                               val=self.get_text())

    def get_text(self):
        """Return Message as string (rather than actual list of characters)"""
        return "".join(self)


#-----------------------------------------------------------------------------
# Genetic operators
#-----------------------------------------------------------------------------

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """

    class memodict(dict):
        def __init__(self, f):
            self.f = f

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret

    return memodict(f)


@memoize
def levenshtein_distance(s1, s2):
    """ Computes the Levenshtein distance between two input strings """
    if not s1: return len(s2)
    if not s2: return len(s1)
    if s1[0] == s2[0]: return levenshtein_distance(s1[1:], s2[1:])
    l1 = levenshtein_distance(s1, s2[1:])
    l2 = levenshtein_distance(s1[1:], s2)
    l3 = levenshtein_distance(s1[1:], s2[1:])
    return 1 + min(l1, l2, l3)


def evaluate_text(message, goal_text, verbose=VERBOSE):
    """
    Given a Message and a goal_text string, return the Levenshtein distance
    between the Message and the goal_text as a length 1 tuple.
    If verbose is True, print each Message as it is evaluated.
    """
    distance = levenshtein_distance(message.get_text(), goal_text)
    if verbose:
        print "{msg:60}\t[Distance: {dst}]".format(msg=message, dst=distance)
    return (distance, )  # Length 1 tuple, required by DEAP


def mutate_text(message, prob_ins=0.05, prob_del=0.05, prob_sub=0.05):
    """
    Given a Message and independent probabilities for each mutation type,
    return a length 1 tuple containing the mutated Message.

    Possible mutations are:
        Insertion:      Insert a random (legal) character somewhere into
                        the Message
        Deletion:       Delete one of the characters from the Message
        Substitution:   Replace one character of the Message with a random
                        (legal) character
    """
    index_value = randrange(0, len(message))
    random_value = random.random()

    if random_value < prob_ins:
        message[index_value:index_value] = random.choice(VALID_CHARS)

    if random_value < prob_del:
        del message[index_value]

    if random_value < prob_sub:
        message[index_value] = random.choice(VALID_CHARS)

    return (message, )  # Length 1 tuple, required by DEAP


#-----------------------------------------------------------------------------
# DEAP Toolbox and Algorithm setup
#-----------------------------------------------------------------------------

def get_toolbox(text):
    """Return DEAP Toolbox configured to evolve given 'text' string"""

    # The DEAP Toolbox allows you to register aliases for functions,
    # which can then be called as "toolbox.function"
    toolbox = base.Toolbox()

    # Creating population to be evolved
    toolbox.register("individual", Message)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Genetic operators
    toolbox.register("evaluate", evaluate_text, goal_text=text, verbose=True)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_text, prob_sub=.45, prob_ins=.35, prob_del=.25)
    toolbox.register("select", tools.selBest)

    # NOTE: You can also pass function arguments as you define aliases, e.g.
    #   toolbox.register("individual", Message, max_length=200)
    #   toolbox.register("mutate", mutate_text, prob_sub=0.18)
    toolbox.decorate("mate", history.decorator)
    toolbox.decorate("mutate", history.decorator)

    return toolbox


def evolve_string(text):
    """Use evolutionary algorithm (EA) to evolve 'text' string"""

    # Set random number generator initial seed so that results are repeatable.
    # See: https://docs.python.org/2/library/random.html#random.seed
    #      and http://xkcd.com/221
    random.seed(4)

    # Get configured toolbox and create a population of random Messages
    toolbox = get_toolbox(text)
    pop = toolbox.population(n=500)

    # Collect statistics as the EA runs
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Run simple EA
    # (See: http://deap.gel.ulaval.ca/doc/dev/api/algo.html for details)
    pop, log = algorithms.eaMuPlusLambda(pop,
                                         toolbox,
                                         mu=150,
                                         lambda_=700,
                                         cxpb=0.75,  # Prob. of crossover (mating)
                                         mutpb=0.25,  # Probability of mutation
                                         ngen=200,  # Num. of generations to run
                                         stats=stats)
    import networkx

    graph = networkx.DiGraph(history.genealogy_tree)
    graph = graph.reverse()  # Make the grah top-down
    colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    networkx.draw(graph, node_color=colors)
    plt.show()
    return pop, log


#-----------------------------------------------------------------------------
# Run if called from the command line
#-----------------------------------------------------------------------------

if __name__ == "__main__":

    # Get goal message from command line (optional)
    import sys
    import multiprocessing

    if len(sys.argv) == 1:
        # Default goal of the evolutionary algorithm if not specified.
        # Pretty much the opposite of http://xkcd.com/534
        goal = "SKYNET IS NOW ONLINE"
    else:
        goal = " ".join(sys.argv[1:])

    toolbox = get_toolbox(goal)
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    # Verify that specified goal contains only known valid characters
    # (otherwise we'll never be able to evolve that string)
    for char in goal:
        if char not in VALID_CHARS:
            msg = "Given text {goal!r} contains illegal character {char!r}.\n"
            msg += "Valid set: {val!r}\n"
            raise ValueError(msg.format(goal=goal, char=char, val=VALID_CHARS))

    # Run evolutionary algorithm
    pop, log = evolve_string(goal)



