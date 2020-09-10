# prob.py
# This is

import random
import numpy as np

from gridutil import *

best_turn = {('N', 'E'): 'turnright',
             ('N', 'S'): 'turnright',
             ('N', 'W'): 'turnleft',
             ('E', 'S'): 'turnright',
             ('E', 'W'): 'turnright',
             ('E', 'N'): 'turnleft',
             ('S', 'W'): 'turnright',
             ('S', 'N'): 'turnright',
             ('S', 'E'): 'turnleft',
             ('W', 'N'): 'turnright',
             ('W', 'E'): 'turnright',
             ('W', 'S'): 'turnleft'}


class LocAgent:

    def __init__(self, size, walls, eps_perc, eps_move):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.di_to_idx = {di: idx for idx, di in enumerate(['N', 'E', 'S', 'W'])}
        self.eps_perc = eps_perc
        self.eps_move = eps_move
        self.array = [0] * len(self.locations)    #self.array - the probability of transition between locations
        for i in range(len(self.locations)):
            self.array[i] = [0] * len(self.locations)
        self.array2 = [0] * len(self.locations)   #self.array2 - compliance of the sensor readings
        for k in range(len(self.locations)):
            self.array2[k] = [0] * 4
        self.array3 = [0] * 4                     #self.array3 - the probability of agent's orientation
        for k in range(4):
            self.array3[k] = [0] * 4
        # previous action
        self.prev_action = None

        prob = 1.0 / len(self.locations)
        prob = prob/4

        self.P = prob * np.ones([len(self.locations), 4], dtype=np.float)
        self.newP = []

    def value(self, percept, p, ret_loc, val):
        if (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] > self.size - 1) and p in percept and (p != 'fwd' or
        (p == 'fwd' and 'bump' not in percept)):
            val = val * (1 - self.eps_perc)
        elif (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] > (self.size - 1)) and 'bump' in percept and p == 'fwd':
            val = val * 1
        elif ret_loc not in self.walls and ret_loc[0] >= 0 and ret_loc[0] <= (self.size - 1) and p not in percept:
            val = val * (1 - self.eps_perc)
        elif (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] > (self.size - 1)) and p not in percept:
            val = val * self.eps_perc
        elif ret_loc not in self.walls and ret_loc[0] >= 0 and ret_loc[0] <= (self.size - 1) and p in percept:
            val = val * self.eps_perc
        elif ret_loc not in self.walls and ret_loc[0] >= 0 and ret_loc[0] <= (self.size - 1) and 'bump' in percept and p == 'fwd':
            val = val * 0
        return val

    def __call__(self, percept):
        # update posterior
        if self.prev_action != None:
            if self.prev_action == 'turnleft' or self.prev_action == 'turnright':
                self.array3 = [0] * 4
                for k in range(4):
                    self.array3[k] = [0] * 4
                for d in ['N', 'E', 'S', 'W']:
                    ind = self.di_to_idx[d]
                    self.array3[ind][ind] = self.eps_move
                    if self.prev_action == 'turnleft':
                        if ind == 0:
                            ind2 = 3
                        else:
                            ind2 = ind - 1
                        self.array3[ind][ind2] = 1 - self.eps_move
                    if self.prev_action == 'turnright':
                        if ind == 3:
                            ind2 = 0
                        else:
                            ind2 = ind + 1
                        self.array3[ind][ind2] = 1 - self.eps_move
                self.array = [0] * len(self.locations)
                for i in range(len(self.locations)):
                    self.array[i] = [0] * len(self.locations)
                for j in range(len(self.locations)):
                    self.array[j][j] = 1           #if the agent turned, he stayed in the same field
            if self.prev_action == 'forward':
                self.array3 = [0] * 4
                for k in range(4):
                    self.array3[k] = [0] * 4
                for d in ['N', 'E', 'S', 'W']:
                    ind = self.di_to_idx[d]
                    self.array3[ind][ind] = 1      #if the agent went forward his orientation stayed the same
                self.array = [0] * len(self.locations)
                for i in range(len(self.locations)):
                    self.array[i] = [0] * len(self.locations)

                for loca in self.locations:
                    if 'bump' in percept:
                        ind = self.loc_to_idx[loca]
                        self.array[ind][ind] = 1            #if the agent hit the wall he stayed in the same field
                    else:
                        wall = [0, 0, 0, 0]
                        loc = []
                        cnt = 0
                        for ind, d in enumerate(['N', 'E', 'S', 'W']): #checking four directions in which agent could go
                            if d == 'N':
                                ret_loc = (loca[0], loca[1] + 1)
                            elif d == 'E':
                                ret_loc = (loca[0] + 1, loca[1])
                            elif d == 'W':
                                ret_loc = (loca[0] - 1, loca[1])
                            elif d == 'S':
                                ret_loc = (loca[0], loca[1] - 1)
                            loc.append(ret_loc)
                            if ret_loc in self.walls or (ret_loc[0] < 0 or ret_loc[0] > self.size - 1):
                                wall[ind] = 1
                                cnt += 1           #count locations where agent can't go
                        ind = self.loc_to_idx[loca]
                        if cnt < 4:
                            val = 0.95/(4 - cnt)    #if agent can go to few locations divide 0.95 by numer of locations
                            self.array[ind][ind] = 0.05   #e.g. agent can go to two locations, so he is in one of them for 0.475 per cent
                            for i, l in enumerate(loc):
                                if wall[i] == 0:
                                    ind1 = self.loc_to_idx[l]
                                    self.array[ind][ind1] = val
            self.array2 = [0] * len(self.locations)
            for k in range(len(self.locations)):
                self.array2[k] = [0] * 4
            for loca in self.locations:
                val = 1
                for d in ['N', 'E', 'S', 'W']:
                    for p in ['fwd', 'right', 'bckwd', 'left']:   #checking the compatibility of the sensor with
                        if d == 'N':                              #the potential agent's position and orientation
                            if p == 'fwd':
                                ret_loc = (loca[0], loca[1] + 1)
                            elif p == 'right':
                                ret_loc = (loca[0] + 1, loca[1])
                            elif p == 'left':
                                ret_loc = (loca[0] - 1, loca[1])
                            elif p == 'bckwd':
                                ret_loc = (loca[0], loca[1] - 1)
                            val = self.value(percept, p, ret_loc, val)
                        if d == 'E':
                            if p == 'fwd':
                                ret_loc = (loca[0] + 1, loca[1])
                            elif p == 'right':
                                ret_loc = (loca[0], loca[1] - 1)
                            elif p == 'left':
                                ret_loc = (loca[0], loca[1] + 1)
                            elif p == 'bckwd':
                                ret_loc = (loca[0] - 1, loca[1])
                            val = self.value(percept, p, ret_loc, val)
                        if d == 'S':
                            if p == 'fwd':
                                ret_loc = (loca[0], loca[1] - 1)
                            elif p == 'right':
                                ret_loc = (loca[0] - 1, loca[1])
                            elif p == 'left':
                                ret_loc = (loca[0] + 1, loca[1])
                            elif p == 'bckwd':
                                ret_loc = (loca[0], loca[1] + 1)
                            val = self.value(percept, p, ret_loc, val)
                        if d == 'W':
                            if p == 'fwd':
                                ret_loc = (loca[0] - 1, loca[1])
                            elif p == 'right':
                                ret_loc = (loca[0], loca[1] + 1)
                            elif p == 'left':
                                ret_loc = (loca[0], loca[1] - 1)
                            elif p == 'bckwd':
                                ret_loc = (loca[0] + 1, loca[1])
                            val = self.value(percept, p, ret_loc, val)
                    ind = self.loc_to_idx[loca]
                    idx = self.di_to_idx[d]
                    self.array2[ind][idx] = val
                    val = 1
            self.newP = np.multiply(np.dot(np.dot(np.transpose(self.array), self.P), self.array3), self.array2)
            self.P = self.newP / self.newP.sum(keepdims=1)

        action = 'forward'
        if 'fwd' in percept and self.prev_action == ['forward'] and 'right' in percept and 'left' not in percept:
            action = 'turnleft'
        elif 'fwd' in percept and self.prev_action == ['forward'] and 'left' in percept and 'right' not in percept:
            action = 'turnright'
        elif 'fwd' in percept and self.prev_action == ['forward']:
            action = np.random.choice(['turnleft', 'turnright'], 1, p=[0.9, 0.1])
        elif self.prev_action == ['turnleft'] and 'fwd' in percept:
            action = 'turnleft'
        elif self.prev_action == ['turnright'] and 'fwd' in percept:
            action = 'turnright'
        else:
            action = np.random.choice(['forward', 'turnleft', 'turnright'], 1, p=[0.9, 0.05, 0.05])

        self.prev_action = action

        return action

    def getPosterior(self):
        # directions in order 'N', 'E', 'S', 'W'
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)

        for idx, loc in enumerate(self.locations):
            for ind in range(4):
                P_arr[loc[0], loc[1], ind] = self.P[idx][ind]
        return P_arr

    def forward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 1) % 4
        return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
        return cur_loc, dirs[idx]
