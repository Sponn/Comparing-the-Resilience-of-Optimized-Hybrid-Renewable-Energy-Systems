from pymoo_test import run_optimization
from pymoo_palaestrai_bridge import run_palaestrai_on_one_individual
from pymoo_analysis import generate_optimization_plots
from midas_run_analysis import calculate_resilience
from pandapower.pf import run_newton_raphson_pf

import json
import sys
import numpy as np
import pickle

if __name__=="__main__":
    if len(sys.argv) > 2:
        run_id = sys.argv[1]
        individual_counter = np.int64(sys.argv[2])

    result_path = 'results_' + run_id + '.pkl'
    with open(result_path, 'rb') as inp:
        results = pickle.load(inp)
    run_palaestrai_on_one_individual(results, run_id, individual_counter=individual_counter)