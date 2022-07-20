#!usr/bin/env python3
"""
random number generator
"""
import random

__author__ = 'Max Allred'
__version__ = 'Spring 2022'
__pylint__ = '2.12.2'

class QLearning:
    """
    the class that learns via qlearning
    """
    qtable = dict()
    reward_indices = {6: -10, 7: -10, 10: 1500, 13: 25, 14: -10, 24: -100,
                      25: -10, 26: -10, 28: -10, 34: -100, 38: -10, 42: -10, 44: -100, 48: -10}

    def __init__(self, alpha, gamma, epsilon):
        self.generate_qtable()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.possible_moves = ['N', 'W', 'E', 'S']
        self.current_reward = 0
        self.current_route = ""
        self.current_location = 31
        self.move_list = []
        self.continue_current = True
        random.seed(0)

    #    q(s,a) = (1 - self.ALPHA)*Q(s,a) + self.alpha*(gamma + epsilon * maxQ(s', a) - Q(s,a)  )

    def train(self, times_trained):
        """
        trains the program a specified number of times
        """
        for _i in range(times_trained):
            self.train_single_time()
        self.move_list.append(self.current_location)

    def train_single_time(self):
        """
        runs one epoch
        """
        self.current_reward = 0
        self.current_route = ""
        self.current_location = 31
        self.find_possible_moves()
        self.move_list = []
        self.continue_current = True
        while self.continue_current:
            self.find_move()

    def generate_qtable(self):
        """
        generates q table for beginning
        """

        for current in range(50):
            if (current+1) > 10:
                position = (current+1, 'N')
                self.qtable[position] = 0
            if (current+1) % 10 != 1:
                position = (current+1, 'W')
                self.qtable[position] = 0
            if (current+1) % 10 != 0:
                position = (current+1, 'E')
                self.qtable[position] = 0
            if (current+1) <= 40:
                position = (current+1, 'S')
                self.qtable[position] = 0

        # array = 0

        # POSSIBLE_MOVES[position] = array

    def find_move(self):
        """
        finds the move that the current epoch will take next
        """
        self.move_list.append(self.current_location)
        old_position = self.current_location
        direction_moved = ''
        self.find_possible_moves()
        random_move = random.random()
        if random_move < self.epsilon:
            chosen = random.choice(self.possible_moves)
            direction_moved = chosen
            self.current_location = self.find_destination(
                self.current_location, chosen)
            self.current_reward = 0
            for current in self.reward_indices.items():
                if current[0] == self.current_location:
                    self.current_reward = current[1]
        else:
            best_move = self.find_best_move(
                self.current_location, self.possible_moves)
            direction_moved = best_move
            self.current_reward = 0
            self.current_location = self.find_destination(
                self.current_location, best_move)
            for current in self.reward_indices.items():
                if current[0] == self.current_location:
                    self.current_reward = current[1]
        move_tuple = (old_position, direction_moved)
        self.find_possible_moves()
        self.qtable[move_tuple] = self.qtable[move_tuple] + self.alpha*(
            self.current_reward + self.gamma * self.find_future_max(
                self.current_location) - self.qtable[move_tuple])
        if self.current_reward in (1500, -100):
            if(self.current_reward == 1500):
                print(self.qtable)
            self.continue_current = False

    def find_possible_moves(self):
        """
        finds the possible moves from the current location
        """
        self.possible_moves = ['N', 'W', 'E', 'S']
        if self.current_location <= 10:
            self.possible_moves.remove('N')
        if self.current_location % 10 == 1:
            self.possible_moves.remove('W')
        if self.current_location % 10 == 0:
            self.possible_moves.remove("E")
        if self.current_location > 40:
            self.possible_moves.remove('S')

    def find_destination(self, start_position, direction):
        """
        finds the destination for the current move
        """
        position = start_position
        if direction == 'N':
            position = start_position - 10
        elif direction == 'S':
            position = start_position + 10
        elif direction == 'E':
            position = start_position + 1
        elif direction == 'W':
            position = start_position - 1
        return position

    def find_best_move(self, position, possible_directions):
        """
        finds the best move from the current position
        """
        best = -999999
        tie_counter = []
        for current in possible_directions:
            q_value = self.qtable[(position, current)]
            if q_value > best:
                best = q_value
                best_move = current
                tie_counter = []
            if q_value == best:
                tie_counter.append(current)
        if len(tie_counter) > 0:
            return random.choice(tie_counter)
        return best_move

    def find_future_max(self, location):
        """
        finds the best qvalue of the future move
        """

        best = 0
        for current in self.possible_moves:
            q_value = self.qtable[(location, current)]
            if q_value > best:
                best = q_value
        return best

    def find_policy(self):
        """
        finds the final path and formats it
        """
        string_of_path = ""
        for current in self.move_list:
            string_of_path = string_of_path + str(current) + ', '

        result = string_of_path.rstrip(', ')
        string_of_path = result + '.'
        return string_of_path
