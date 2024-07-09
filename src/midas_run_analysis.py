import pandas
from scipy import integrate
import ruamel.yaml
import os

RUN_ID = '0cb48ee2-bd59-499f-9991-e6b1734a977e'

def calc_line_load_fom(df):
    target_column = 'line_load_fom'
    loads = df.filter(regex='.*line.*loading_percent')
    loads = loads.apply(lambda x: _calc_load_fom(x, target_column), axis=1)
    df[target_column] = loads[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_trafo_load_fom(df):
    target_column = 'trafo_load_fom'
    loads = df.filter(regex='.*trafo.*loading_percent')
    loads = loads.apply(lambda x: _calc_load_fom(x, target_column), axis=1)
    df[target_column] = loads[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_bus_in_service_fom(df):
    target_column = 'bus_in_service_fom'
    values = df.filter(regex='.*bus.*in_service')
    values = values.apply(lambda x: _calc_in_service_fom(x, target_column), axis=1)
    df[target_column] = values[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_line_in_service_fom(df):
    target_column = 'line_in_service_fom'
    values = df.filter(regex='.*line.*in_service')
    values = values.apply(lambda x: _calc_in_service_fom(x, target_column), axis=1)
    df[target_column] = values[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_load_in_service_fom(df):
    target_column = 'load_in_service_fom'
    values = df.filter(regex='.*load.*in_service')
    values = values.apply(lambda x: _calc_in_service_fom(x, target_column), axis=1)
    df[target_column] = values[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_sgen_in_service_fom(df):
    target_column = 'sgen_in_service_fom'
    values = df.filter(regex='.*sgen.*in_service')
    values = values.apply(lambda x: _calc_in_service_fom(x, target_column), axis=1)
    df[target_column] = values[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_storage_in_service_fom(df):
    target_column = 'storage_in_service_fom'
    values = df.filter(regex='.*storage.*in_service')
    values = values.apply(lambda x: _calc_in_service_fom(x, target_column), axis=1)
    df[target_column] = values[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df

def calc_vmpu_bus_fom(df):
    target_column = 'vmpu_bus_in_operating_window_fom'
    values = df.filter(regex='.*vm_pu')
    values = values.apply(lambda x: _calc_vmpu_fom(x, target_column), axis=1)
    df[target_column] = values[target_column]
    #just for testing
    # testing_list = []
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.7,0.7,0.7,0.7,0.7,0.8,0.9])
    # for i in range(20):
    #     testing_list.append(1.0)
    # testing_list.extend([0.9, 0.8, 0.7, 0.6,0.5,0.5,0.6,0.7,0.8,0.9, 1.0, 
    #                      0.9, 0.8, 0.7, 0.6,0.6,0.6,0.7,0.8,0.9])
    # for i in range(26):
    #     testing_list.append(1.0)
    # testing_dict = {target_column: testing_list}
    # testing_df = pandas.DataFrame(testing_dict)
    # df[target_column] = testing_dict[target_column]

    return df


def _calc_load_fom(row, target_column):
    num_total = len(row.axes[0])
    num_overloaded = (row>100).sum()
    percentage_not_overloaded = 1 - (num_overloaded/num_total)
    row[target_column] = percentage_not_overloaded
    return row

def _calc_in_service_fom(row, target_column):
    num_total = len(row.axes[0])
    num_in_service = (row).sum()
    percentage_in_service = (num_in_service/num_total)
    row[target_column] = percentage_in_service
    return row

def _calc_vmpu_fom(row, target_column):
    # calculate fom as percentage of buses inside regular operating window between 0.9 and 1.1 pu.
    # one simulation step is 1 minute, which is the trigger point for being outside the operating window
    # according to VDE 4110
    num_total = len(row.axes[0])
    num_outside_regular_operation = ((row<0.9) | (row>1.1)).sum()
    percentage_inside_regular_operation = 1 - (num_outside_regular_operation/num_total)
    row[target_column] = percentage_inside_regular_operation
    return row




def calc_resilience_as_amount_of_loss(df, column_name):
    
    fom_df = df[column_name]
    i=0
    amount_of_loss = 0
    while i< len(fom_df):
        # find first index of degraded performance
        if fom_df.iloc[i].item() < 1:
            # degraded performance detected
            # find last index of degraded performance
            end_index=i
            for j in range(i, len(fom_df)):
                if fom_df.iloc[j].item() >= 1:
                    end_index = j
                    break
            degraded_performance_df = fom_df.iloc[i:j]
            # difference to optimal fom values (optimal is 1 in this case)
            degraded_performance_df = (degraded_performance_df-1)*-1
            # integral of degraded performance
            integral = integrate.trapz(degraded_performance_df.values, degraded_performance_df.index)
            amount_of_loss += integral
            i=j
        i+=1         
    return amount_of_loss

def _get_number_of_training_and_test_episodes(run_id):
    yaml = ruamel.yaml.YAML(typ="safe", pure=True)

    folder_path = os.path.join('run_files', str(run_id))
    run_file_name = 'individual_0_run.yml'
    run_file_path = os.path.join(folder_path, run_file_name)

    with open(run_file_path) as file:
        run_yml = yaml.load(file)
    
    num_training_episodes = run_yml["schedule"][0]["training"]["phase_config"]["episodes"]
    num_test_episodes = run_yml["schedule"][1]["test"]["phase_config"]["episodes"]
    return num_training_episodes, num_test_episodes

def calculate_resilience(result, run_id):
    num_individuals = len(result.opt)
    print("Number of individuals " + str(num_individuals))
    num_training_episodes, num_test_episodes = _get_number_of_training_and_test_episodes(run_id)
    resiliences_dict = {}
    print("Starting calculation")
    for individual_counter in range(num_individuals):
        resilience_dict = {}
        for test_episode_counter in range(1,num_test_episodes+1):
            # get only results of test run ignore all training outputs
            print("Loading simulation logs")
            result_path = '_outputs/' + str(run_id) + '_individual_' + str(individual_counter) + '_' + str(num_training_episodes+test_episode_counter) +'.hdf5'
            try:
                df_powergrid = pandas.read_hdf(result_path, 'Powergrid__0')
            except:
                print("Failed to load simulation log for individual " + str(individual_counter) + " episode " + str(num_training_episodes+test_episode_counter))
                continue
            
            print("Starting calculation for individual " + str(individual_counter) + " episode " + str(test_episode_counter))

            #line_load_fom = calc_line_load_fom(df_powergrid)
            #trafo_load_fom = calc_trafo_load_fom(df_powergrid)
            #bus_in_service_fom = calc_bus_in_service_fom(df_powergrid)
            #line_in_service_fom = calc_line_in_service_fom(df_powergrid)
            #load_in_service_fom = calc_load_in_service_fom(df_powergrid)
            #sgen_in_service_fom = calc_sgen_in_service_fom(df_powergrid)
            #storage_in_service_fom = calc_storage_in_service_fom(df_powergrid)
            vmpu_bus_fom = calc_vmpu_bus_fom(df_powergrid)

            print("Finished FOM calculation")

            #line_load_resilience = calc_resilience_as_amount_of_loss(line_load_fom, 'line_load_fom')
            #trafo_load_resilience = calc_resilience_as_amount_of_loss(trafo_load_fom, 'trafo_load_fom')
            #bus_in_service_resilience = calc_resilience_as_amount_of_loss(bus_in_service_fom, 'bus_in_service_fom')
            #line_in_service_resilience = calc_resilience_as_amount_of_loss(line_in_service_fom, 'line_in_service_fom')
            #load_in_service_resilience = calc_resilience_as_amount_of_loss(load_in_service_fom, 'load_in_service_fom')
            #sgen_in_service_resilience = calc_resilience_as_amount_of_loss(sgen_in_service_fom, 'sgen_in_service_fom')
            #storage_in_service_resilience = calc_resilience_as_amount_of_loss(storage_in_service_fom, 'storage_in_service_fom')
            vmpu_bus_resilience = calc_resilience_as_amount_of_loss(vmpu_bus_fom, 'vmpu_bus_in_operating_window_fom')

            #resilience_dict_for_test_episode = {"test_episode"+str(test_episode_counter):{"line_load_resilience": line_load_resilience, "trafo_load_resilience": trafo_load_resilience, 
            #                "bus_in_service_resilience": bus_in_service_resilience, "line_in_service_resilience": line_in_service_resilience,
            #                "load_in_service_resilience": load_in_service_resilience, "sgen_in_service_resilience": sgen_in_service_resilience,
            #                "storage_in_service_resilience": storage_in_service_resilience, "vmpu_bus_in_operating_window_resilience": vmpu_bus_resilience}}
            resilience_dict_for_test_episode = {"test_episode"+str(test_episode_counter):{"vmpu_bus_in_operating_window_resilience": vmpu_bus_resilience}}
            resilience_dict = resilience_dict | resilience_dict_for_test_episode
            print("Finished episode " + str(test_episode_counter))
        
        resiliences_dict["individual_" + str(individual_counter)] = resilience_dict
        print("Finished individual " + str(individual_counter))
    return resiliences_dict
        

if __name__ == '__main__':
    print(_get_number_of_training_and_test_episodes('ded73c70-d63f-11ee-b976-00155db1ed53')
          )
    # result_path='_outputs/' + RUN_ID + '.hdf5'
    # df_powergrid = pandas.read_hdf(result_path, 'Powergrid__0')
    # line_load_fom = calc_line_load_fom(df_powergrid)
    # trafo_load_fom = calc_trafo_load_fom(df_powergrid)
    # bus_in_service_fom = calc_bus_in_service_fom(df_powergrid)
    # line_in_service_fom = calc_line_in_service_fom(df_powergrid)
    # load_in_service_fom = calc_load_in_service_fom(df_powergrid)
    # sgen_in_service_fom = calc_sgen_in_service_fom(df_powergrid)
    # storage_in_service_fom = calc_storage_in_service_fom(df_powergrid)
    # line_load_resilience = calc_resilience_as_amount_of_loss(line_load_fom, 'line_load_fom')
    # trafo_load_resilience = calc_resilience_as_amount_of_loss(trafo_load_fom, 'trafo_load_fom')
    # bus_in_service_resilience = calc_resilience_as_amount_of_loss(bus_in_service_fom, 'bus_in_service_fom')
    # line_in_service_resilience = calc_resilience_as_amount_of_loss(line_in_service_fom, 'line_in_service_fom')
    # load_in_service_resilience = calc_resilience_as_amount_of_loss(load_in_service_fom, 'load_in_service_fom')
    # sgen_in_service_resilience = calc_resilience_as_amount_of_loss(sgen_in_service_fom, 'sgen_in_service_fom')
    # storage_in_service_resilience = calc_resilience_as_amount_of_loss(storage_in_service_fom, 'storage_in_service_fom')
    # print()