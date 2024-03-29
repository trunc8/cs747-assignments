#!/usr/bin/env python

# trunc8 did this

# Below three imports only have to do with logging
import logging
import sys
import pulp

import argparse
import numpy as np

import value_iteration_solver, howard_policy_iteration_solver, linear_programming_solver

def main():
  logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s.%(msecs)03d %(message)s', datefmt='%H:%M:%S')
  logging.getLogger(pulp.__name__).setLevel(logging.WARNING)
  # Below is a toggle switch for logging messages
  logging.disable(sys.maxsize)
  
  parser = argparse.ArgumentParser(description="Input path to the MDP file and algorithm to be used")
  parser.add_argument("--mdp", help="mdp file path")
  parser.add_argument("--algorithm", help="vi: Value Iteration; hpi: Howard Policy Iteration; lp: Linear Programming")
  args = parser.parse_args() # Read args from terminal

  S = 0 # Number of states
  A = 0 # Number of actions
  st = 0 # Start state
  end = [] # List of terminal states; -1 if none
  R = None # 3d numpy array for rewards
  T = None # 3d numpy array for transition probabilities
  mdptype = "" # Episodic or continuing
  gamma = 0 # Discount factor

  # File I/O
  mdp_file = open(args.mdp, "r")
  for line in mdp_file:
    data = line.split()
    if "numStates" == data[0]:
      S = int(data[1])
    elif "numActions" == data[0]:
      A = int(data[1])
      R = np.zeros((S, A, S), dtype=np.float64)
      T = np.zeros((S, A, S), dtype=np.float64)
    elif "start" == data[0]:
      st = int(data[1])
    elif "end" == data[0]:
      for ed in data[1:]:
        end.append(int(ed))
    elif "transition" == data[0]:
      s1 = int(data[1])
      a = int(data[2])
      s2 = int(data[3])
      R[s1,a,s2] = float(data[4])
      T[s1,a,s2] = float(data[5])
    elif "mdptype" == data[0]:
      mdptype = data[1]
    elif "discount" == data[0]:
      gamma = float(data[1])

  mdp_file.close()
  # File I/O ends

  if args.algorithm == "vi":
    V, P = value_iteration_solver.soln(R, T, gamma) # mdptype, start, end??
  elif args.algorithm == "hpi":
    V, P = howard_policy_iteration_solver.soln(S, A, R, T, gamma)
  elif args.algorithm == "lp":
    V, P = linear_programming_solver.soln(S, A, R, T, gamma)
  else:
    print("Invalid algorithm entered")
    return

  for s in range(S):
    print(f"{V[s]:.6f}\t{int(P[s])}")

  #import json
  #print(json.dumps(T, indent=4))

if __name__ == '__main__':
  main()
