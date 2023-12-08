# Databricks notebook source
# MAGIC %md
# MAGIC # Actividad :  Resolución de problema mediante búsqueda heurística
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

#!pip install pydot graphviz

# COMMAND ----------

#!/usr/bin/env python
# coding: utf-8

# 2022 Modified by: Alejandro Cervantes
# Remember installing pyplot and flask if you want to use WebViewer

# NOTA: WebViewer sólo funcionará si ejecutáis en modo local

from __future__ import print_function

import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import BaseViewer,ConsoleViewer,WebViewer

# COMMAND ----------

# MAGIC %md
# MAGIC # Configuración de los distintos escenarios

# COMMAND ----------

MAP_Base = """
########
#    T #
# #### #
#   P# #
# ##   #
#      #
########      
"""

MAP_5b = """
########
#  P   #
# #### #
#    # #
# ##   #
#   T  #
########      
"""

MAP_5c = MAP_Base

MAP_5d = """
###########
#       P #
# ####### #
#T      # #
#         #
###########      
"""

COSTS_Base = {
    "up": 1.0,
    "down": 1.0,
    "right": 1.0,
    "left": 1.0,
}
COSTS_5b = COSTS_Base
COSTS_5c = {
    "up": 5.0,
    "down": 1.0,
    "right": 1.0,
    "left": 1.0,
}
COSTS_5d = COSTS_Base


# COMMAND ----------

# MAGIC %md
# MAGIC # Definición de clases y métodos

# COMMAND ----------

class GameWalkPuzzle(SearchProblem):

    def __init__(self, board, fun_heuristic):
        self.board = board
        self.goal = (0, 0)
        self.fun_heuristic = fun_heuristic
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "t":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "p":
                    self.goal = (x, y)

        super(GameWalkPuzzle, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in list(COSTS.keys()):
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return self.fun_heuristic(x,gx, y, gy)
    
def searchInfo (problem,result,use_viewer):
    def getTotalCost (problem,result):
        originState = problem.initial_state
        totalCost = 0
        for action,endingState in result.path():
            if action is not None:
                totalCost += problem.cost(originState,action,endingState)
                originState = endingState
        return totalCost

    
    res = "Total length of solution: {0}\n".format(len(result.path()))
    res += "Total cost of solution: {0}\n".format(getTotalCost(problem,result))
        
    if use_viewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                         for stat, value in list(use_viewer.stats.items())]
        
        for s in stats:
            res+= '{0}: {1}\n'.format(s['name'],s['value'])
    return res


def resultado_experimento(problem,MAP,result,used_viewer):
    path = [x[1] for x in result.path()]

    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print("T", end='')
            elif (x, y) == problem.goal:
                print("P", end='')
            elif (x, y) in path:
                print("·", end='')
            else:
                print(MAP[y][x], end='')
        print()

    info=searchInfo(problem,result,used_viewer)
    print(info)

def manhattan(x,gx,y,gy):
    return abs(x - gx) + abs(y - gy)
    
def euclidian(x,gx,y,gy):
    return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)
        
def diagonal(x,gx,y,gy):
    return max(abs(x - gx),abs(y - gy))

# COMMAND ----------

def run_experiments(map_arg, use_console_viewer):
    experiment_MAP = [list(x) for x in map_arg.split("\n") if x]

    print('Breath')
    problem = GameWalkPuzzle(experiment_MAP, lambda x: 1)
    used_viewer = ConsoleViewer() if use_console_viewer else BaseViewer()
    # No podréis usar aquí WebViewer en Collab para ver los árboles
    result = breadth_first(problem, graph_search=True,viewer=used_viewer)
    resultado_experimento(problem,experiment_MAP,result,used_viewer)
    print('End Breath')

    print('Depth')    
    problem = GameWalkPuzzle(experiment_MAP, lambda x: 1)
    used_viewer = ConsoleViewer() if use_console_viewer else BaseViewer()
    result = depth_first(problem, graph_search=True,viewer=used_viewer)
    resultado_experimento(problem,experiment_MAP,result,used_viewer)
    print('End Depth')

    print('A* Manhattan')
    problem = GameWalkPuzzle(experiment_MAP,manhattan)
    used_viewer = ConsoleViewer() if use_console_viewer else BaseViewer()
    result = astar(problem, graph_search=True,viewer=used_viewer)
    resultado_experimento(problem,experiment_MAP,result,used_viewer)
    print('End A* Manhattan')

    print('A* Euclidian')
    problem = GameWalkPuzzle(experiment_MAP,euclidian)
    used_viewer = ConsoleViewer() if use_console_viewer else BaseViewer() 
    result = astar(problem, graph_search=True,viewer=used_viewer)
    resultado_experimento(problem,experiment_MAP,result,used_viewer)
    print('End A* Euclidian')

    #print('A* Diagonal')
    #problem = GameWalkPuzzle(MAP,diagonal)
    #used_viewer = ConsoleViewer() if use_console_viewer else BaseViewer()
    #print('A* Diagonal')
    #result = astar(problem, graph_search=True,viewer=used_viewer)
    #resultado_experimento(problem,MAP,result,used_viewer)
    #print('End A* Diagonal')

# COMMAND ----------

# MAGIC %md
# MAGIC # Ejecución de los distintos puntos de la actividad

# COMMAND ----------

# MAGIC %md
# MAGIC ### Actividad Base

# COMMAND ----------

COSTS = COSTS_Base
run_experiments(MAP_Base, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Actividad 5b

# COMMAND ----------

COSTS = COSTS_5b
run_experiments(MAP_5b, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Actividad 5c

# COMMAND ----------

COSTS = COSTS_5c
run_experiments(MAP_5c, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Actividad 5d

# COMMAND ----------

COSTS = COSTS_5d
run_experiments(MAP_5d, False)
