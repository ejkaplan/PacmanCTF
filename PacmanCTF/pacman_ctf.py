from copy import deepcopy
import random
import time
from location import *
from maze_gen import maze_gen
from random_pacman import Random_Pacman

class Pacman_CTF_Game(object):
    
    '''
    This is the class for making a game! Scroll to the bottom to see how to run a game.
    '''
    
    def __init__(self, size=31, turn_limit=1800, time_limit=1, log=False, seed=None):
        '''
        Create a new game object. Takes 5 arguments:
        size - the board is always a square - what are the side lengths?
        turn_limit - how many turns before the game is over?
        time_limit - how long in seconds does a bot have to decide what to do?
            (The director will have 8 turns worth of time for setup code.)
        log - should a log file be created for eventual replay?
        seed - do you want to seed the random number generator? (mostly used to ensure that
            the same map is generated over multiple runs.)
        '''
        if size % 2 == 0:
            size -= 1
        if not seed:
            seed = random.random()
        self.seed = seed
        random.seed(self.seed)
        self.turn = 0
        self.turn_limit = turn_limit
        self.time_limit = time_limit
        # Build the maze
        self.passages = maze_gen(size, size, 20, 4, 6)
        red_cells = [Location(r, c) for r in range(len(self.passages)) for c in range(len(self.passages[r])) if self.passages[r][c] == 1]
        random.shuffle(red_cells)
        n_dots = round(len(red_cells) * 0.5)
        # Set the spawn points
        self.spawns = [[], []]
        for agent_num in range(3):
            i = 0
            while red_cells[i].row > size//4 or not (agent_num*size//3 < red_cells[i].col < (agent_num+1)*size//3):
                i += 1
            red_spawn = red_cells.pop(i)
            blue_spawn = red_spawn.get_mirror(size)
            self.spawns[0].append(red_spawn)
            self.spawns[1].append(blue_spawn)
        self.spawns[0].sort()
        self.spawns[1].sort()
        # Place the dots
        self.dots = [[], []]
        for _ in range(n_dots):
            dot = red_cells.pop()
            self.dots[1].append(dot)
            self.dots[0].append(dot.get_mirror(size))
        self.dots[0].sort()
        self.dots[1].sort()
        # Set up the players
        self.agents = deepcopy(self.spawns)
        self.eaten_dots = [[[] for _ in range(3)] for _ in range(2)]
        self.directors = []
        self.scores = [0, 0]
        # Set up the logfile
        if log:
            self.logfile = open("logs/pacman_{}.csv".format(int(time.time())), "w")
            self.logfile.write("{}\n".format(len(self.passages)))
            for row in self.passages:
                for cell in row:
                    self.logfile.write("{},".format(cell))
            self.logfile.write("x\n")
            for team in self.spawns:
                for coord in team:
                    self.logfile.write("{},{},".format(coord.row, coord.col))
            self.logfile.write("x\n")
            self.log_state()
        else:
            self.logfile = None
        
    def play_game(self):
        '''
        Run this function to play out the game. Returns the winning director object.
        '''
        for player in self.directors:
            with timeout(seconds=8*self.time_limit):
                try:
                    player.start()
                except:
                    pass
        while True:
            for agent in range(3):
                for player in range(len(self.directors)):
                    with timeout(seconds=self.time_limit):
                        try:
                            move = self.directors[player].get_move(agent)
                        except:
                            move = None
                    newLoc = self.agents[player][agent].get_loc_in_dir(move)
                    if newLoc.isLegal(self.passages) and self.passages[newLoc.row][newLoc.col] > 0:
                        self.agents[player][agent] = newLoc
                    self.eat_dots()
                    self.capture_agents()
                    self.score_points()
                    self.turn += 1
                    if self.logfile:
                        self.log_state()
                    if self.turn > self.turn_limit:
                        if self.logfile:
                            self.logfile.flush()
                            self.logfile.close()
                        return self.directors[self.scores.index(max(self.scores))]
                    
    def update(self):
        self.eat_dots()
        self.capture_agents()
        self.score_points()
                    
    def eat_dots(self):
        for team_i in range(len(self.agents)):
            for agent_i in range(len(self.agents[team_i])):
                loc = self.agents[team_i][agent_i]
                if loc in self.dots[team_i]:
                    self.dots[team_i].remove(loc)
                    self.eaten_dots[team_i][agent_i].append(loc)
                    
    def capture_agents(self):
        conflicts = [coord for coord in self.agents[0] if coord in self.agents[1]]
        for conf in conflicts:
            remove = 2 - self.passages[conf.row][conf.col]
            for i in range(len(self.agents[remove])):
                if self.agents[remove][i] == conf:
                    self.agents[remove][i] = self.spawns[remove][i]
                    for dot in self.eaten_dots[remove][i]:
                        self.dots[remove].append(dot)
                    self.eaten_dots[remove][i].clear()
    
    def score_points(self):
        for team in range(len(self.agents)):
            for i in range(len(self.agents[team])):
                agent = self.agents[team][i]
                space = self.passages[agent.row][agent.col] - 1
                if space == team:
                    self.scores[team] += len(self.eaten_dots[team][i]) * (len(self.eaten_dots[team][i])+1) // 2
                    self.eaten_dots[team][i].clear()
                    
    def log_state(self):
        line = ""
        for team in self.agents:
            for agent in team:
                line += "{},{},".format(agent.row,agent.col)
        for score in self.scores:
            line += "{},".format(score)
        for team in self.dots:
            for dot in team:
                line += "{},{},".format(dot.row,dot.col)
        line += "x\n"
        self.logfile.write(line)                
        
    def add_director(self, director):
        if len(self.directors) < 2:
            self.directors.append(director)
            
    def get_number(self, director):
        return self.directors.index(director) + 1
    
    def get_passages(self):
        return deepcopy(self.passages)
    
    def get_dots(self, number):
        return [loc.get_tuple() for loc in self.dots[number - 1]]
    
    def get_agents(self, number):
        return [loc.get_tuple() for loc in self.agents[number - 1]]
    
    def get_enemy_agents(self, number):
        enemies = self.agents[1 - (number - 1)]
        friends = self.agents[number - 1]
        out = []
        for enemy in enemies:
            found = False
            for friend in friends:
                if friend.manhattan_distance(enemy) <= 5:
                    found = True
                    break
            out.append(enemy.get_tuple() if found else None)
        return out
    
    def radar(self, number, agent_number):
        random.seed(self.seed + self.turn)
        enemies = self.agents[1 - (number - 1)]
        agent = self.agents[number - 1][agent_number]
        max_diff = max(agent.row, len(self.passages) - agent.row - 1) + max(agent.col, len(self.passages[0]) - agent.col - 1)
        out = []
        for enemy in enemies:
            dist = enemy.manhattan_distance(agent)
            out.append(random.randint(max(0, dist - 6), min(dist + 6, max_diff)))
        return out
    
import signal

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

if __name__ == "__main__":
    '''
    You'll set up your game here.
    '''
    game = Pacman_CTF_Game(log=True) #create the game.
    Random_Pacman(game) #Create the two directors and pass the game in as objects.
    Random_Pacman(game)
    game.play_game() #Play the game.
