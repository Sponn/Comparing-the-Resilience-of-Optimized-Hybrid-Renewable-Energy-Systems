from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from fitness_calculator import calculate_fitness, clear_directory
import multiprocessing as mp
import numpy as np
import pickle
import uuid
import datetime

class MidasProblem(Problem):
    def __init__(self, num_threads=4):
        self.num_threads = num_threads
        super().__init__(n_var=8, n_obj=2, n_ieq_constr=0, xl=[0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001], xu=[10.0, 10.0, 10.0, 1.0, 1.0, 10.0, 10.0, 10.0])

    def _evaluate(self, x, out, *args, **kwargs):
        
        individual_mappings = []

        for individual in x:
            individual_mappings.append(get_individual_mapping(individual))

        pool= mp.Pool(self.num_threads)
        fitnesses = pool.map(calculate_fitness, individual_mappings)
        pool.close()
        
        
        
        out["F"] = np.array(fitnesses)


def get_individual_mapping(x):
    # cast to python float for compatibility with yml
    x = [float(item) for item in x]

    individual = {3: [["PV", x[0]], ["HVAC", 1.279], ["HVAC", 0.343]],
                                                4: [["HVAC", 0.343]],
                                                7: [["DIESEL", x[1]]],
                                                8: [["PV", x[2]]],
                                                9: [["HVAC", 0.23], ["BAT", x[3]]],
                                                11: [["Biogas", 2.05], ["BAT", x[4]], ["PV", x[5]]],
                                                13: [["HVAC", 0.23], ["PV", x[6]]],
                                                14: [["PV", x[7]], ["HVAC", 1.279]]}
    
    individual_mapping = {"midasmv": {"mapping": individual,
                                    "weather_provider_mapping": {
                                        "PV": ["bremen", 0],
                                        "HVAC": ["bremen", 0],
                                        "BAT": ["bremen", 0],
                                        "CHP": ["bremen", 0],
                                        "Biogas": ["bremen", 0],
                                        "DIESEL": ["bremen", 0]}}}
    
    return individual_mapping

def get_initial_population(problem, pop_size):
    known_initial_solution = np.array([0.7, 0.8, 0.8, 0.8, 0.8, 0.6, 0.6, 0.4])
    sampling = FloatRandomSampling()
    X = sampling(problem, pop_size-1).get("X")
    X = np.insert(X, 0, known_initial_solution, axis=0)
    return X

    
def run_optimization(n_gen=10, pop_size=10, seed=1337, verbose=True, save_results=True, num_threads=4):
    id = None
    problem = MidasProblem(num_threads=num_threads)
    initial_population = get_initial_population(problem, pop_size)
    algorithm = NSGA2(pop_size=pop_size, sampling=initial_population)

    before = datetime.datetime.now()
    res = minimize(problem, algorithm, ('n_gen',n_gen), seed=seed, verbose=verbose, save_history=True)
    after = datetime.datetime.now()
    
    if save_results:
        id = uuid.uuid1()
        file_name = './results_'+str(id)+'.pkl'
        with open(file_name, 'wb') as file:
            pickle.dump(res, file)
            print(f'Object successfully saved to "{file_name}"')
    
    duration = after-before
    print("Optimization took " + str(after-before) + " .")

    try:
        clear_directory()
    except:
        print("Something went wrong trying to delete the outputs.")
    return res, id

if __name__ == "__main__":
    res = run_optimization(pop_size=20)