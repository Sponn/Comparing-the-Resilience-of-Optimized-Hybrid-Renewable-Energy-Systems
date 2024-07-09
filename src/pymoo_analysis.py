import pickle
from pymoo.core.result import Result
from pymoo_test import MidasProblem
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas

RUN_ID = '08dced86-324c-11ef-bc8c-8e4c9fde469b'
def generate_table(result=None, run_id=None, generation=1):
    if run_id == None:
        run_id = RUN_ID
    if result == None:
         with open('results_' + RUN_ID + '.pkl', 'rb') as inp:
            result = pickle.load(inp)

    history = result.history

    folder_path = os.path.join('tables', str(run_id))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    generation_solutions = history[generation-1]
    non_dominated_population = generation_solutions.opt
    f1s =[]
    f2s =[]
    individual_counters = []
    counter = 1
    for individuum in non_dominated_population:
        f1s.append(individuum.F[0])
        f2s.append(individuum.F[1])
        individual_counters.append(counter)
        counter = counter + 1
    
    df = pandas.DataFrame({"Individual": individual_counters, "LPSP": f1s, "COE": f2s})

    table_path = os.path.join(folder_path, 'generation_' + str(generation) + "_table.tex")
    df.to_latex(table_path, index=False)

def generate_optimization_plots(result=None, run_id =None):
    if run_id == None:
        run_id = RUN_ID
    if result == None:
         with open('results_' + RUN_ID + '.pkl', 'rb') as inp:
            result = pickle.load(inp)

    history = result.history

    folder_path = os.path.join('plots', str(run_id))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    counter=1
    for generation in history:
        non_dominated_population = generation.opt
        f1s =[]
        f2s =[]
        for individuum in non_dominated_population:
            f1s.append(individuum.F[0])
            f2s.append(individuum.F[1])

        try:
            polyfit = np.polyfit(f1s, f2s, 2)
            approx = np.poly1d(polyfit)(f1s)
        except:
            plt.rc('figure', titlesize=40)
            plt.rc('axes', titlesize=40)
            plt.rc('axes', labelsize=40)
            plt.rc('xtick', labelsize=30)
            plt.rc('ytick', labelsize=30) 
            plt.figure(counter, figsize=(18,16), dpi=300)
            plt.scatter(f1s, f2s, marker="X", s=400)
            plt.title('Non dominated solutions Generation ' + str(counter))
            plt.xlabel('LPSP [%]')
            plt.ylabel('COE [$/kWh]')
            plt.xlim([0,0.12])
            plt.ylim([0,0.01])

            fig_path = os.path.join(folder_path, 'generation_' + str(counter))
            plt.savefig(fig_path, dpi=300)
            plt.close()
            counter = counter + 1

        plt.rc('figure', titlesize=40)
        plt.rc('axes', titlesize=40)
        plt.rc('axes', labelsize=40)
        plt.rc('xtick', labelsize=30)
        plt.rc('ytick', labelsize=30) 
        plt.figure(counter, figsize=(18,16), dpi=300)
        plt.scatter(f1s, f2s, marker="X", s=400)
        #plt.plot(f1s, approx)
        plt.title('Non dominated solutions Generation ' + str(counter))
        plt.xlabel('LPSP [%]')
        plt.ylabel('COE [$/kWh]')
        plt.xlim([0,0.12])
        plt.ylim([0,0.01])

        fig_path = os.path.join(folder_path, 'generation_' + str(counter))
        plt.savefig(fig_path, dpi=300)
        plt.close()
        counter = counter + 1

    print("")

if __name__ == "__main__":
    #generate_optimization_plots(run_id=RUN_ID)
    generate_table(run_id=RUN_ID, generation=40)