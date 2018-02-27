class CTF_Director(object):
    '''
    The class that you write should extend CTF_Director. This will give you all
    the methods you need for accessing the world state. The start() function is
    called automatically at the start of the game and the get_move() function
    is called to get the move you want to make, so be sure to override those methods.
    
    You may NEVER access self.game except indirectly by calling one of the methods
    defined below.
    '''
    
    def __init__(self, game):
        '''
        Your class needs to have the a generic __init__ function - copy
        the one from random_pacman.
        '''
        self.game = game
        game.add_director(self)
        
    def start(self):
        '''
        This function is called immediately before the game starts. It is called after
        the world is created, so all the functions will work. Do your initial setup here.
        '''
        pass
    
    def get_move(self, agent_number):
        '''
        This function is called every turn, and should return a one character string for
        the cardinal direction in which the agent should move - 'n', 's', 'e', 'w'. If you try
        to move into a wall or return anything other than one of "nsew", the agent will not move
        at all. (If you want the agent to stay still, I recommend returning None or not returning
        at all.)
        The agent that will move is indicated by agent_number, which will be 0, 1 or 2.
        You can find the position of this agent by checking the agent_number-th index in
        the list returned by get_my_agents.
        '''
        return None
        
    def get_number(self):
        '''
        This returns your number, which will be 1 or 2. This is used to figure out which squares
        are safe squares on the map.
        '''
        return self.game.get_number(self)
    
    def get_map(self):
        '''
        Returns the map as a 2D list of integers 0, 1 or 2. 0 indicates a wall, 1 indicates a square
        that is safe for player #1 and 2 indicates a square that is safe for player #2. While on
        squares that match your number, you can catch enemy agents, but you need to go to the other
        team's squares to eat dots and score points.
        NOTE: If you use an integer in an if statement, python treats 0 as False and all other values
        as True. So you can say
            if self.get_map()[0][0]:
        And it will perform the body of the if statement if the upper-left corner of the map (0,0) is 
        a corridor (is not a wall.)
        '''
        return self.game.get_passages()
    
    def get_dots_to_eat(self):
        '''
        Returns a list of tuples representing the coordinates of all the dots that you still
        need to eat, in (row, col) format.
        '''
        return self.game.get_dots(self.get_number())
    
    def get_dots_to_protect(self):
        '''
        Returns a list of tuples representing the coordinates of all the dots that your opponent
        still needs to eat, in (row, col) format.
        '''
        return self.game.get_dots(3 - self.get_number())

    def get_my_agents(self):
        '''
        Returns a list of tuples representing the coordinates of all your agents in (row, col) format.
        '''
        return self.game.get_agents(self.get_number())
    
    def get_enemy_agents(self):
        '''
        Returns a list of tuples representing the coordinates of all your enemy's agents
        in (row, col) format. A given enemy will be listed as None if they are too far away to see.
        '''
        return self.game.get_enemy_agents(self.get_number())
    
    def radar(self, agent_number):
        '''
        Returns a list of how far away each enemy is from one of your agents. The friendly agent
        taking the distance reading is provided by the agent_number argument. The distance is given
        as a noisy distance, which is +-6 of the actual value. All possible distances that are within
        6 of the correct manhattan distance are equally likely to be given.
        '''
        return self.game.radar(self.get_number(), agent_number)
    
    def get_eaten_dots(self):
        '''
        Returns a list of 3 integers indicating the number of dots currently being held by each of your
        three agents. A given agent's dot count will reset to 0 upon being caught by the enemy or
        returning to friendly territory and scoring points.
        '''
        return [len(x) for x in self.game.eaten_dots[self.get_number() - 1]]
    
    def get_turns_left(self):
        '''
        Returns the number of moves left in the game total across all agents. By default, this will be
        1800 before any agent makes a move. (300 moves per agent over 6 agents.)
        '''
        return self.game.turn_limit - self.game.turn
