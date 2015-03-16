#!/usr/bin/python
#
#   namegen.py
#
#   Author: John McCardle
#   Purpose: generate words (namely, sci-fi alien names) based on lists of other names using a Markov Chain.
#   License: MIT

import random
import sys
from collections import Counter, defaultdict
if sys.version_info[0] == 3:
    raw_input = input
    xrange = range

class MarkovState:
    def __init__(self):
        self.transitions = Counter()    #allows unknown keys to default to zero; simplifies incrementing.
        
    def __repr__(self):
        return str(self.transitions)
        
    def increment(self, ch):
        self.transitions[ch] += 1
        
    def transition(self):
        if len(self.transitions) == 0:
            return None
        if len(self.transitions) == 1:
            return list(self.transitions.keys())[0]
        count = sum([self.transitions[key] for key in self.transitions.keys()])
        r = random.uniform(0, count)
        t = 0
        for s in self.transitions:
            if t + self.transitions[s] > r:
                return s
            t += self.transitions[s]

class MarkovChain:
    def __init__(self, haltstate='\n', between=''):
        self.haltstate = haltstate
        self.states = defaultdict(MarkovState) #allows unknown keys to default to a blank state; simplifies linking.
        self.states[haltstate] = None #Why no state? We need to get an error if we try to transition from the halt state.
        self.init = MarkovState()
        self.between = between

    def DEBUG_printStates(self):
        for i, j in self.states.items():
            print(i)
            for l, k in j.transitions.items():
                print("   {}, {}".format(l, k))
                
    def randomWalk(self, maxlength=None):
        MIN_LENGTH = 3
        state = self.init.transition()
        output = []
        while state != self.haltstate:
            output.append(state)
            if maxlength and len(output) >= maxlength:
                break
            nextstate = self.states[state].transition()
            if nextstate == None:
                print(state)
                exit()
            state = nextstate
        return self.between.join((str(i) for i in output)) if len(output) > MIN_LENGTH else self.randomWalk()

    def addLink(self, linkstate, targetstate):
        self.states[linkstate].increment(targetstate)

    def addWord(self, word, terminate=False):  #Adds each letter pair in the word to the markov chain
        word = word.lower()
        self.init.increment(word[0])
        for n in xrange(0, len(word)-1):
            self.addLink(word[n], word[n+1])
        if terminate:
            self.addLink(word[-1], self.haltstate)

    def addWords(sentence): #Adds each word pair in the sentence to the markov chain
        pass
        
if __name__ == '__main__':
    mc = MarkovChain()
    wordcount = 0

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            for line in f:
                wordcount += 1
                mc.addWord(line)
    else:
        print("Enter words, provide blank input to end:")
        while True:
            txt = raw_input() + "\n"
            if txt == "\n":
                break
            wordcount += 1
            mc.addWord(txt)
    t_total = sum([len(mc.states[s].transitions) for s in mc.states if mc.states[s]])
    print("States: {}\n\nTotal Transitions: {}\nAverage Transitions per state: {}"
        .format(len(mc.states), t_total, (float(t_total)) / len(mc.states)))
    for n in xrange(20):
        print(mc.randomWalk().strip('\n'))