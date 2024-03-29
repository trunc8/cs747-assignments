#!/usr/bin/env python

# trunc8 did this

import numpy as np
import logging

def soln(R, T, gamma):
  logging.debug("Value Iteration started")
  V = np.zeros(R.shape[0])
  eps = 1e-12
  timestep = 1
  S = R.shape[0]

  # valid_action_values = np.sum(T, axis=2)
  # logging.debug(f"Valid action values: {valid_action_values}")

  while True:
    action_values = np.sum(np.multiply(T, R + gamma*V), axis=2)
    V_next = np.amax(action_values, axis=1)

    if np.linalg.norm(V_next - V) < eps:
      logging.debug("Value Iteration [OK]")
      break

    V[:] = V_next

    timestep += 1
    if timestep > 1e10:
      logging.error("Value Iteration [FAILED]")
      break
  logging.debug(f"{timestep} iterations taken")
  # Unless we had a timeout, V is now V*
  
  # Finding policy*
  Policy = np.argmax(np.sum(np.multiply(T, R + gamma*V), axis=2), axis=1)

  return V, Policy
