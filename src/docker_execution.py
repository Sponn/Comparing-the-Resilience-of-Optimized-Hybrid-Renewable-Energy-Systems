from pymoo_test import run_optimization
from pymoo_palaestrai_bridge import run_palaestrai_on_results
from pymoo_analysis import generate_optimization_plots
from midas_run_analysis import calculate_resilience
from pandapower.pf import run_newton_raphson_pf

import json
import sys
import numpy as np
import pickle

if __name__=="__main__":
    if len(sys.argv) > 6:
        n_gen = np.int64(sys.argv[1])
        pop_size = np.int64(sys.argv[2])
        seed = np.int64(sys.argv[3])
        verbose = bool(sys.argv[4])
        save_results = bool(sys.argv[5])
        num_threads = np.int64(sys.argv[6])
        run_id = None
    if len(sys.argv) > 7:
        n_gen = np.int64(sys.argv[1])
        pop_size = np.int64(sys.argv[2])
        seed = np.int64(sys.argv[3])
        verbose = bool(sys.argv[4])
        save_results = bool(sys.argv[5])
        num_threads = np.int64(sys.argv[6])
        run_id = sys.argv[7]
    else:
        n_gen = 2
        pop_size = 20
        seed = 1337
        verbose = True
        save_results = True
        num_threads = 4
        run_id = None

    if run_id is None:
        results, run_id = run_optimization(n_gen=n_gen, pop_size=pop_size, seed=seed, verbose=verbose, save_results=save_results, num_threads = num_threads)
    else:
        result_path = 'results_' + run_id + '.pkl'
        with open(result_path, 'rb') as inp:
            results = pickle.load(inp)
    generate_optimization_plots(results, run_id)
    run_palaestrai_on_results(results, run_id)
    resiliences = calculate_resilience(results, run_id)
    with open(str(run_id) + "_resiliences.json", "w") as fp:
        json.dump(resiliences, fp)