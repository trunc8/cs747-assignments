#!/usr/bin/env python

# trunc8 did this
import time
import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n")
args = parser.parse_args()

start = time.time()
prev = start
file = f"outputDataT{args.n}.txt"
if os.path.exists(file):
    os.remove(file) # To prevent appending

f = open(file,"w")

instances = ["../instances/i-1.txt", "../instances/i-2.txt", "../instances/i-3.txt"]

if args.n == '1':
  algorithms = ["epsilon-greedy", "ucb", "kl-ucb", "thompson-sampling"]
elif args.n == '2':
  # algorithms = ["thompson-sampling", "thompson-sampling-with-hint"]
  algorithms = ["thompson-sampling-with-hint"]

horizons = [100, 400, 1600, 6400, 25600, 102400]
randomSeeds = range(50)
epsilon = 0.02
for instance in instances:
    for algorithm in algorithms:
        for horizon in horizons:
            for randomSeed in randomSeeds:
                cmd = f"python bandit.py --instance {instance} --algorithm {algorithm} --randomSeed {randomSeed} --epsilon {epsilon} --horizon {horizon}"
                try:
                    p = subprocess.Popen(cmd.split(), shell=False, stdout=f)
                except:
                    print("Error occurred")
                p.wait()
            curr = time.time()
            print(f"Time elapsed:{curr - start:.2f}s\tsince last", 
                f"print:{curr - prev:.2f}s\t{instance}\t{algorithm}\t{horizon}")
            prev = curr
f.close()
# cmd = "python bandit.py --instance ../instances/i-1.txt --algorithm epsilon-greedy --randomSeed 0 --epsilon 0.02 --horizon 100"
# subprocess.run(cmd)
