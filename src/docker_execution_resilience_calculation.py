from midas_run_analysis import calculate_resilience


import sys
import json
import numpy as np
import pickle

if __name__=="__main__":
    if len(sys.argv) > 1:
        run_id = sys.argv[1]

    result_path = 'results_' + run_id + '.pkl'
    print("Loading result from " + str(result_path))
    with open(result_path, 'rb') as inp:
        results = pickle.load(inp)
    print("Calculating resiliences")
    resiliences = calculate_resilience(results, run_id)
    with open(str(run_id) + "_resiliences.json", "w") as fp:
        json.dump(resiliences, fp)