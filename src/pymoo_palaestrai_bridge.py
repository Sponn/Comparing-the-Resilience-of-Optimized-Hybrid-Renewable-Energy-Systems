import pickle
from pymoo.core.result import Result
from pymoo_test import MidasProblem
import os
from io import StringIO
from pymoo_test import get_individual_mapping
import ruamel.yaml
import ez_yaml
import shutil

from palaestrai.cli.manager import cli
import palaestrai

RUN_ID = 'cc4c8694-2a65-11ef-baf7-00155df516f1'

def run_palaestrai_on_results(result=None, run_id=None, result_path='results_' + RUN_ID + '.pkl'):
    if run_id == None:
        run_id = RUN_ID
    if result == None:
         with open(result_path, 'rb') as inp:
            result = pickle.load(inp)
    folder_path = os.path.join('run_files', str(run_id))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    yaml = ruamel.yaml.YAML(typ="safe", pure=True)
    yaml.preserve_quotes = True

    with open('src/classic-arl.yml') as file:
        base_scenario_yml = yaml.load(file)

    with open('src/classicarl_experiment_run.yml') as file:
        base_run_yml = yaml.load(file)

    counter = 0
    run_file_paths = []
    print(len(result.opt))
    for individual in result.opt:
        values = individual.X
        individual_mapping = get_individual_mapping(values)

        base_scenario_yml["carl_cigre_ts"]["der_params"] = individual_mapping
        scenario_file_name = 'individual_' + str(counter) + '_scenario.yml'
        scenario_path = os.path.join(folder_path, scenario_file_name)
        midas_store_filename = str(run_id) + '_individual_' + str(counter)
        with open(scenario_path, 'w') as scenario_output:
            yaml.dump(base_scenario_yml, scenario_output)

        base_run_yml["schedule"][0]["training"]["environments"][0]["environment"]["params"]["params"]["config"] = str(scenario_path)
        base_run_yml["schedule"][0]["training"]["environments"][0]["environment"]["params"]["params"]["store_params"]["filename"] = str(midas_store_filename)


        run_file_name = 'individual_' + str(counter) + '_run.yml'
        run_file_path = os.path.join(folder_path, run_file_name)
        with open(run_file_path, 'w') as run_output:
            yaml.dump(base_run_yml, run_output)

        run_file_as_string = ez_yaml.to_string(base_run_yml)

        rc = palaestrai.execute(StringIO(run_file_as_string))

        output_directory = "./_outputs/brains"
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory)

        run_file_paths.append(run_file_path)
        # TODO: 
        counter = counter + 1
        print("Finished individual " + str(counter))
    
    # run_file_paths_as_string = ""
    # for path in run_file_paths:
    #     #run_file_paths_as_string = run_file_paths_as_string + '"' + str(path) + '" '
    #     run_file_paths_as_string = run_file_paths_as_string + str(path) +" "
    # command = ["start"]
    # command.extend(run_file_paths)
    # print(command)
    # cli(command)
    #cli(["start", run_file_paths])
    print("Done!")


def run_palaestrai_on_one_individual(result=None, run_id=None, result_path='results_' + RUN_ID + '.pkl', individual_counter=0):
    if run_id == None:
        run_id = RUN_ID
    if result == None:
         with open(result_path, 'rb') as inp:
            result = pickle.load(inp)
    folder_path = os.path.join('run_files', str(run_id))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    yaml = ruamel.yaml.YAML(typ="safe", pure=True)
    yaml.preserve_quotes = True

    with open('src/classic-arl.yml') as file:
        base_scenario_yml = yaml.load(file)

    with open('src/classicarl_experiment_run.yml') as file:
        base_run_yml = yaml.load(file)

    run_file_paths = []
    print(len(result.opt))
    individual = result.opt[individual_counter]
    values = individual.X
    individual_mapping = get_individual_mapping(values)

    base_scenario_yml["carl_cigre_ts"]["der_params"] = individual_mapping
    scenario_file_name = 'individual_' + str(individual_counter) + '_scenario.yml'
    scenario_path = os.path.join(folder_path, scenario_file_name)
    midas_store_filename = str(run_id) + '_individual_' + str(individual_counter)
    with open(scenario_path, 'w') as scenario_output:
        yaml.dump(base_scenario_yml, scenario_output)

    base_run_yml["schedule"][0]["training"]["environments"][0]["environment"]["params"]["params"]["config"] = str(scenario_path)
    base_run_yml["schedule"][0]["training"]["environments"][0]["environment"]["params"]["params"]["store_params"]["filename"] = str(midas_store_filename)

    base_run_yml["uid"] = base_run_yml["uid"] + '_individual_' + str(individual_counter)

    run_file_name = 'individual_' + str(individual_counter) + '_run.yml'
    run_file_path = os.path.join(folder_path, run_file_name)
    with open(run_file_path, 'w') as run_output:
        yaml.dump(base_run_yml, run_output)

    run_file_as_string = ez_yaml.to_string(base_run_yml)

    rc = palaestrai.execute(StringIO(run_file_as_string))

    # output_directory = "./_outputs/brains"
    # if os.path.exists(output_directory):
    #     shutil.rmtree(output_directory)

    run_file_paths.append(run_file_path)
    # TODO: 
    print("Finished individual " + str(individual_counter))
    
    # run_file_paths_as_string = ""
    # for path in run_file_paths:
    #     #run_file_paths_as_string = run_file_paths_as_string + '"' + str(path) + '" '
    #     run_file_paths_as_string = run_file_paths_as_string + str(path) +" "
    # command = ["start"]
    # command.extend(run_file_paths)
    # print(command)
    # cli(command)
    #cli(["start", run_file_paths])
    print("Done!")



if __name__ == "__main__":
    run_palaestrai_on_one_individual()