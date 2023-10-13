# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

class WestAgent(Agent):

    def __init__(self):
        self.west = Directions.WEST
        self.north = Directions.NORTH
        self.south = Directions.SOUTH

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        # If west is a legal action, choose that.
        if self.west in legal:
            return api.makeMove(self.west, legal)
        
        # If not, check if either north or south is possible.
        up_down_moves = [move for move in [self.north, self.south] if move in legal]
        
        if up_down_moves:
            # If either up or down is possible, choose one of them randomly.
            return api.makeMove(random.choice(up_down_moves), legal)
        
        # If neither up nor down is possible, choose randomly from the remaining legal actions.
        return api.makeMove(random.choice(legal), legal)



def getNextPosition(position, direction):
    x, y = position
    if direction == Directions.NORTH:
        return (x, y + 1)
    if direction == Directions.SOUTH:
        return (x, y - 1)
    if direction == Directions.EAST:
        return (x + 1, y)
    if direction == Directions.WEST:
        return (x - 1, y)
    return position  # If direction is STOP or invalid

class HungryAgent(Agent):

    def getAction(self, state):
        # Get the current position of Pacman
        pacman_pos = api.whereAmI(state)

        # Get the positions of all food pellets
        food_positions = api.food(state)
        
        # If there's no food left, return a random move (this shouldn't happen in a normal game, but just in case)
        if not food_positions:
            legal = api.legalActions(state)
            return api.makeMove(random.choice(legal), legal)

        # Calculate the distance from Pacman to each food pellet
        distances = [util.manhattanDistance(pacman_pos, food) for food in food_positions]
        
        # Determine the position of the nearest food pellet
        nearest_food_pos = food_positions[distances.index(min(distances))]

        # Get legal moves
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # Decide on a move that takes Pacman closer to the nearest food pellet
        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]
        best_move = min(moves, key=lambda x: util.manhattanDistance(getNextPosition(pacman_pos, x[0]), nearest_food_pos))
        
        return best_move[1]





class SurvivalAgent(Agent):

    def getAction(self, state):
        # Get the current position of Pacman
        pacman_pos = api.whereAmI(state)

        # Get the positions of all ghosts
        ghost_positions = api.ghosts(state)

        # Get legal moves
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # If there are no ghosts, just return a random move
        if not ghost_positions:
            return api.makeMove(random.choice(legal), legal)

        # Calculate distances from Pacman to each ghost for each possible moveclass CornerSeekingAgentAvoidGhost(Agent):

    def __init__(self):
        self.corners_to_visit = []  # Initialize as an empty list
        self.target_corner = None
        self.intermediate_target = None
        self.last_action = None  # Track the last action taken

    def getAction(self, state):
        print("Starting a new action call...")

        # Get the current position of Pacman
        pacman_pos = api.whereAmI(state)
        print("Current Pacman position:", pacman_pos)


        # Get the positions of all ghosts
        ghost_positions = api.ghosts(state)




        # If corners_to_visit is empty, fill it with the corners and shuffle
        if not self.corners_to_visit:
            self.corners_to_visit = list(api.corners(state))
            random.shuffle(self.corners_to_visit)
            self.target_corner = self.corners_to_visit.pop()  # Start with the first corner in the shuffled list

        # If Pacman is at the target corner, set the next corner as the target (if any are left)
        if pacman_pos == self.target_corner and self.corners_to_visit:
            self.target_corner = self.corners_to_visit.pop()

        # Get the positions of all food pellets in sensory range
        food_positions = api.food(state)

        # If there's food nearby, set the nearest food pellet as the immediate target
        if food_positions:
            distances_to_food = [util.manhattanDistance(pacman_pos, food) for food in food_positions]
            nearest_food_pos = food_positions[distances_to_food.index(min(distances_to_food))]
            self.intermediate_target = nearest_food_pos
            print("Set nearest food as intermediate target:", nearest_food_pos)

        # If there's an intermediate target, move towards it; otherwise, move towards the corner
        target = self.intermediate_target if self.intermediate_target else self.target_corner
        print("Current target:", target)

        # Decide on a move that takes Pacman closer to the target
        legal = api.legalActions(state)
        
        # Remove "STOP" and the reverse of the last action from the legal moves to prevent oscillation
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if self.last_action and Directions.REVERSE[self.last_action] in legal:
            legal.remove(Directions.REVERSE[self.last_action])
            print("Removed reverse action:", Directions.REVERSE[self.last_action])

        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]
        sorted_moves = sorted(moves, key=lambda x: util.manhattanDistance(getNextPosition(pacman_pos, x[0]), target))

        # Iterate through the sorted moves and pick the first legal one
        for move in sorted_moves:

            if not ghost_positions: # If there are no ghosts, just return a random move

                if move[1] in legal:
                    self.last_action = move[0]  # Update the last action
                    print("Picking a legal move:", move[0], "towards:", target)
                    return move[1]



        moves_distances = []
        for direction in legal:
            next_pos = getNextPosition(pacman_pos, direction)
            #distances_to_ghosts = [util.manhattanDistance(next_pos, ghost) for ghost in ghost_positions]
            distances_to_ghosts = [util.manhattanDistance(pacman_pos, ghost) for ghost in ghost_positions]
            min_distance = min(distances_to_ghosts)  # Find the closest ghost for this move
            moves_distances.append((direction, min_distance))
        
        best_move = max(moves_distances, key=lambda x: x[1])

        return api.makeMove(best_move[0], legal)
                   
        
        # If, for some reason, no moves are legal (shouldn't happen), stop
        #return api.makeMove(Directions.STOP, legal)

        moves_distances = []
        for direction in legal:
            next_pos = getNextPosition(pacman_pos, direction)
            distances_to_ghosts = [util.manhattanDistance(next_pos, ghost) for ghost in ghost_positions]
            min_distance = min(distances_to_ghosts)  # Find the closest ghost for this move
            moves_distances.append((direction, min_distance))

        # Find the move that maximizes the distance to the nearest ghost
        best_move = max(moves_distances, key=lambda x: x[1])

        return api.makeMove(best_move[0], legal)

'''

class CornerSeekingAgent(Agent):

    def __init__(self):
        self.corners_to_visit = []  # Initialize as an empty list
        self.target_corner = None
        self.intermediate_target = None
        #Track Last Position
        self.last_position = None

    def getAction(self, state):

        self.last_position = api.whereAmI(state)

        # Get the current position of Pacman
        pacman_pos = api.whereAmI(state)

        # If corners_to_visit is empty, fill it with the corners and shuffle
        if not self.corners_to_visit:
            self.corners_to_visit = list(api.corners(state))
            random.shuffle(self.corners_to_visit)
            self.target_corner = self.corners_to_visit.pop()  # Start with the first corner in the shuffled list

        # If Pacman is at the target corner, set the next corner as the target (if any are left)
        if pacman_pos == self.target_corner and self.corners_to_visit:
            self.target_corner = self.corners_to_visit.pop()

        # Get the positions of all food pellets in sensory range
        food_positions = api.food(state)

        # If there's food nearby, set the nearest food pellet as the immediate target
        if food_positions:
            distances_to_food = [util.manhattanDistance(pacman_pos, food) for food in food_positions]
            nearest_food_pos = food_positions[distances_to_food.index(min(distances_to_food))]
            self.intermediate_target = nearest_food_pos

        # If Pacman has reached the intermediate target or there's no food nearby, reset the intermediate target
        if pacman_pos == self.intermediate_target or not self.intermediate_target:
            self.intermediate_target = None

        # If there's an intermediate target, move towards it; otherwise, move towards the corner
        target = self.intermediate_target if self.intermediate_target else self.target_corner

        # Decide on a move that takes Pacman closer to the target
        legal = api.legalActions(state)
        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]

        # Sort the moves based on the distance to the target
        sorted_moves = sorted(moves, key=lambda x: util.manhattanDistance(getNextPosition(pacman_pos, x[0]), target))

        # Iterate through the sorted moves and pick the first legal one
        for move in sorted_moves:
            new_position = getNextPosition(pacman_pos, move[0])
            if move[1] in legal and new_position!= self.last_position:
                print("pick a legal move")
                self.last_position = pacman_pos
                return move[1]

        # If for some reason no moves are legal (shouldn't happen), stop
        print("we are stopping")
        return api.makeMove(Directions.STOP, legal)


'''

class CornerSeekingAgent(Agent):

    def __init__(self):
        self.corners_to_visit = []  # Initialize as an empty list
        self.target_corner = None
        self.intermediate_target = None
        self.last_action = None  # Track the last action taken

    def getAction(self, state):
        print("Starting a new action call...")

        # Get the current position of Pacman
        pacman_pos = api.whereAmI(state)
        print("Current Pacman position:", pacman_pos)

        # If corners_to_visit is empty, fill it with the corners and shuffle
        if not self.corners_to_visit:
            self.corners_to_visit = list(api.corners(state))
            random.shuffle(self.corners_to_visit)
            self.target_corner = self.corners_to_visit.pop()  # Start with the first corner in the shuffled list

        # If Pacman is at the target corner, set the next corner as the target (if any are left)
        if pacman_pos == self.target_corner and self.corners_to_visit:
            self.target_corner = self.corners_to_visit.pop()

        # Get the positions of all food pellets in sensory range
        food_positions = api.food(state)

        # If there's food nearby, set the nearest food pellet as the immediate target
        if food_positions:
            distances_to_food = [util.manhattanDistance(pacman_pos, food) for food in food_positions]
            nearest_food_pos = food_positions[distances_to_food.index(min(distances_to_food))]
            self.intermediate_target = nearest_food_pos
            print("Set nearest food as intermediate target:", nearest_food_pos)

        # If there's an intermediate target, move towards it; otherwise, move towards the corner
        target = self.intermediate_target if self.intermediate_target else self.target_corner
        print("Current target:", target)

        # Decide on a move that takes Pacman closer to the target
        legal = api.legalActions(state)
        
        # Remove "STOP" and the reverse of the last action from the legal moves to prevent oscillation
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if self.last_action and Directions.REVERSE[self.last_action] in legal:
            legal.remove(Directions.REVERSE[self.last_action])
            print("Removed reverse action:", Directions.REVERSE[self.last_action])

        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]
        sorted_moves = sorted(moves, key=lambda x: util.manhattanDistance(getNextPosition(pacman_pos, x[0]), target))

        # Iterate through the sorted moves and pick the first legal one
        for move in sorted_moves:
            if move[1] in legal:
                self.last_action = move[0]  # Update the last action
                print("Picking a legal move:", move[0], "towards:", target)
                return move[1]
        
        # If, for some reason, no moves are legal (shouldn't happen), stop
        return api.makeMove(Directions.STOP, legal)



























'''

class CornerSeekingAgentNoFood(Agent):

    def __init__(self):
        # List of corners to visit
        self.corners_to_visit = None
        # Current target corner
        self.target_corner = None
        # Previous position of Pacman
        self.last_position = None

    def getAction(self, state):
        pacman_pos = api.whereAmI(state)
        print("Current Pacman Position:", pacman_pos)
        
        # Initialize the corners to visit
        if self.corners_to_visit is None:
            self.corners_to_visit = list(api.corners(state))
        
        # If we are at the target corner, remove it from the list of corners to visit
        if pacman_pos == self.target_corner:
            self.corners_to_visit.remove(self.target_corner)
            self.target_corner = None

        # If we don't have a target corner, choose the nearest one from the unvisited corners
        if not self.target_corner and self.corners_to_visit:
            self.target_corner = min(self.corners_to_visit, key=lambda x: util.manhattanDistance(pacman_pos, x))

        # If all corners are visited, maybe stay in place or add other behaviors.
        if not self.target_corner:
            return api.makeMove(Directions.STOP, api.legalActions(state))
        
        print("Target Corner:", self.target_corner)

        # Decide on a move that takes Pacman closer to the target corner
        legal = api.legalActions(state)
        print("Legal Moves:", legal) 
        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]
        best_move = min(moves, key=lambda x: util.manhattanDistance(getNextPosition(pacman_pos, x[0]), self.target_corner))

        print("Best Move:", best_move[1])
        

        # Check if the move leads to a change in position to avoid getting stuck
        new_position = getNextPosition(pacman_pos, best_move[0])
        if new_position == self.last_position:
            legal.remove(best_move[1])
            best_move = random.choice(legal) if legal else Directions.STOP
        else:
            self.last_position = pacman_pos
        
        return best_move[1]
'''

class CornerSeekingAgentNoFood(Agent):

    def __init__(self):
        self.visited_corners = set()
        self.target_corner = None
        self.last_move = None
        self.move_attempts = 0  # Counter for move attempts towards the current target corner
        self.all_corners = None

    def getAction(self, state):
        # Initialize all corners if they haven't been set yet
        if self.all_corners is None:
            self.all_corners = api.corners(state)

        pacman_pos = api.whereAmI(state)

        # If we are at the target corner, mark it as visited, reset the move attempts, and remove it from all_corners
        if pacman_pos == self.target_corner:
            self.visited_corners.add(self.target_corner)
            self.all_corners.remove(self.target_corner)
            self.target_corner = None
            self.move_attempts = 0

        # If we don't have a target corner, choose the first one from the remaining corners
        if not self.target_corner and self.all_corners:
            self.target_corner = self.all_corners[0]

        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # If move attempts exceed a threshold (e.g., 10), choose a random move
        if self.move_attempts > 10:
            self.move_attempts = 0
            return api.makeMove(random.choice(legal), legal)

        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]
        best_move = min(moves, key=lambda x: util.manhattanDistance(self.getNextPosition(pacman_pos, x[0]), self.target_corner))

        # If the agent is trying the same move again, increment move_attempts, otherwise reset it
        if best_move[0] == self.last_move:
            self.move_attempts += 1
        else:
            self.move_attempts = 0

        self.last_move = best_move[0]
        return best_move[1]

    def getNextPosition(self, position, direction):
        x, y = position
        if direction == Directions.NORTH:
            return (x, y + 1)
        if direction == Directions.SOUTH:
            return (x, y - 1)
        if direction == Directions.EAST:
            return (x + 1, y)
        if direction == Directions.WEST:
            return (x - 1, y)
        return position  # If direction is STOP or invalid





class CornerSeekingAgentAvoidGhost(Agent):

    def __init__(self):
        self.corners_to_visit = []  # Initialize as an empty list
        self.target_corner = None
        self.intermediate_target = None
        self.last_action = None  # Track the last action taken

    def getAction(self, state):
        print("Starting a new action call...")

        # Get the current position of Pacman
        pacman_pos = api.whereAmI(state)
        print("Current Pacman position:", pacman_pos)


        # Get the positions of all ghosts
        ghost_positions = api.ghosts(state)




        # If corners_to_visit is empty, fill it with the corners and shuffle
        if not self.corners_to_visit:
            self.corners_to_visit = list(api.corners(state))
            random.shuffle(self.corners_to_visit)
            self.target_corner = self.corners_to_visit.pop()  # Start with the first corner in the shuffled list

        # If Pacman is at the target corner, set the next corner as the target (if any are left)
        if pacman_pos == self.target_corner and self.corners_to_visit:
            self.target_corner = self.corners_to_visit.pop()

        # Get the positions of all food pellets in sensory range
        food_positions = api.food(state)

        # If there's food nearby, set the nearest food pellet as the immediate target
        if food_positions:
            distances_to_food = [util.manhattanDistance(pacman_pos, food) for food in food_positions]
            nearest_food_pos = food_positions[distances_to_food.index(min(distances_to_food))]
            self.intermediate_target = nearest_food_pos
            print("Set nearest food as intermediate target:", nearest_food_pos)

        # If there's an intermediate target, move towards it; otherwise, move towards the corner
        target = self.intermediate_target if self.intermediate_target else self.target_corner
        print("Current target:", target)

        # Decide on a move that takes Pacman closer to the target
        legal = api.legalActions(state)
        
        # Remove "STOP" and the reverse of the last action from the legal moves to prevent oscillation
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if self.last_action and Directions.REVERSE[self.last_action] in legal:
            legal.remove(Directions.REVERSE[self.last_action])
            print("Removed reverse action:", Directions.REVERSE[self.last_action])

        moves = [(direction, api.makeMove(direction, legal)) for direction in legal]
        sorted_moves = sorted(moves, key=lambda x: util.manhattanDistance(getNextPosition(pacman_pos, x[0]), target))

        # Iterate through the sorted moves and pick the first legal one
        for move in sorted_moves:

            if not ghost_positions: # If there are no ghosts, just return a random move

                if move[1] in legal:
                    self.last_action = move[0]  # Update the last action
                    print("Picking a legal move:", move[0], "towards:", target)
                    return move[1]



        moves_distances = []
        for direction in legal:
            next_pos = getNextPosition(pacman_pos, direction)
            #distances_to_ghosts = [util.manhattanDistance(next_pos, ghost) for ghost in ghost_positions]
            distances_to_ghosts = [util.manhattanDistance(pacman_pos, ghost) for ghost in ghost_positions]
            min_distance = min(distances_to_ghosts)  # Find the closest ghost for this move
            moves_distances.append((direction, min_distance))
        
        best_move = max(moves_distances, key=lambda x: x[1])

        return api.makeMove(best_move[0], legal)
                   
        
        # If, for some reason, no moves are legal (shouldn't happen), stop
        #return api.makeMove(Directions.STOP, legal)

