'''
Created on Feb 23, 2018

@author: eliotkaplan
'''
import random
from ctf_director import *

class Random_Pacman(CTF_Director):
    
    '''
    Random bot - makes totally random moves. (Except that it doesn't make 180 degree turns.)
    '''
    
    def __init__(self, game):
        super().__init__(game)
        
    def start(self):
        # Set up your instance variables here.
        # In this case, keep track of the last movement direction of each agent so that
        # you don't turn around next turn.
        self.headings = [None for _ in range(len(self.get_my_agents()))]
        
    def get_move(self, agent_number):
        # Return the move for agent #agent_number, by returning a character from "nsew".
        # In this case, chooses randomly without turning all the way around.
        directions = {'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1)}
        opposites = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
        if self.headings[agent_number]:
            opp = opposites[self.headings[agent_number]]
        else:
            opp = None
        loc = self.get_my_agents()[agent_number]
        legal = []
        m = self.get_map()
        for d in directions:
            if d == opp: continue
            newLoc = (loc[0]+directions[d][0],loc[1]+directions[d][1])
            if 0 <= newLoc[0] < len(m) and 0 <= newLoc[1] < len(m):
                if m[newLoc[0]][newLoc[1]]:
                    legal.append(d)
        self.headings[agent_number] = random.choice(legal)
        return self.headings[agent_number]