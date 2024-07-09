import json
from matplotlib import pyplot as plt
import os
from scipy.stats import ttest_ind
import pandas

RUN_ID = "08dced86-324c-11ef-bc8c-8e4c9fde469b"

def calculate_resilience_statistics(run_id=RUN_ID):

    plot_output_path=os.path.join('plots', str(run_id))

    if not os.path.exists(plot_output_path):
        os.makedirs(plot_output_path)

    filename = run_id + "_resiliences.json"
    with open(filename,"r") as file:
        resiliences = json.load(file)
    
    individual_key_list = resiliences.keys()
    resiliences_as_lists_dict = {}
    line_load_resiliences_list = []
    trafo_load_resiliences_list = []
    bus_in_service_resiliences_list= []
    line_in_service_resiliences_list= []
    load_in_service_resiliences_list= []
    sgen_in_service_resiliences_list= []
    storage_in_service_resiliences_list= []
    vmpu_bus_in_operating_window_resiliences_list= []
    for key in individual_key_list:
        line_load_resiliences = []
        trafo_load_resiliences = []
        bus_in_service_resiliences= []
        line_in_service_resiliences= []
        load_in_service_resiliences= []
        sgen_in_service_resiliences= []
        storage_in_service_resiliences= []
        vmpu_bus_in_operating_window_resiliences= []
        individual_dict = resiliences[key]
        for episode in individual_dict.keys():
            episode_dict = individual_dict[episode]
            line_load_resiliences.append(episode_dict.get("line_load_resilience",None))
            trafo_load_resiliences.append(episode_dict.get("trafo_load_resilience",None))
            bus_in_service_resiliences.append(episode_dict.get("bus_in_service_resilience",None))
            line_in_service_resiliences.append(episode_dict.get("line_in_service_resilience",None))
            load_in_service_resiliences.append(episode_dict.get("load_in_service_resilience",None))
            sgen_in_service_resiliences.append(episode_dict.get("sgen_in_service_resilience",None))
            storage_in_service_resiliences.append(episode_dict.get("storage_in_service_resilience",None))
            vmpu_bus_in_operating_window_resiliences.append(episode_dict.get("vmpu_bus_in_operating_window_resilience",None))
        individual_dict_with_lists = {}
        individual_dict_with_lists["line_load_resiliences"] = line_load_resiliences
        individual_dict_with_lists["trafo_load_resiliences"] = trafo_load_resiliences
        individual_dict_with_lists["bus_in_service_resiliences"] = bus_in_service_resiliences
        individual_dict_with_lists["line_in_service_resiliences"] = line_in_service_resiliences
        individual_dict_with_lists["load_in_service_resiliences"] = load_in_service_resiliences
        individual_dict_with_lists["sgen_in_service_resiliences"] = sgen_in_service_resiliences
        individual_dict_with_lists["storage_in_service_resiliences"] = storage_in_service_resiliences
        individual_dict_with_lists["vmpu_bus_in_operating_window_resiliences"] = vmpu_bus_in_operating_window_resiliences
        resiliences_as_lists_dict[key] = individual_dict_with_lists

        line_load_resiliences_list.append(line_load_resiliences)
        trafo_load_resiliences_list.append(trafo_load_resiliences)
        bus_in_service_resiliences_list.append(bus_in_service_resiliences)
        line_in_service_resiliences_list.append(line_in_service_resiliences)
        load_in_service_resiliences_list.append(load_in_service_resiliences)
        sgen_in_service_resiliences_list.append(sgen_in_service_resiliences)
        storage_in_service_resiliences_list.append(storage_in_service_resiliences)
        vmpu_bus_in_operating_window_resiliences_list.append(vmpu_bus_in_operating_window_resiliences)
        # Todo: calc statistics

    
    vmpu_bus_in_operating_window_t_test_results_df, num_significant, num_insignificant = _t_test_execution(vmpu_bus_in_operating_window_resiliences_list)
    
    _t_test_table_export(vmpu_bus_in_operating_window_t_test_results_df)
    
    # plt.figure(1, figsize=(18,16), dpi=300)
    # plt.boxplot(line_load_resiliences_list)
    # plt.title('Line load resilience scores ')
    # fig_path = os.path.join(plot_output_path, 'line_load_resiliences_boxplot')
    # plt.savefig(fig_path, dpi=300)
    # plt.close()

    #_save_boxplot(line_load_resiliences_list, "Line load resilience scores", plot_output_path, "line_load_resiliences_boxplot")
    #_save_boxplot(trafo_load_resiliences_list, "Trafo load resilience scores", plot_output_path, "trafo_load_resiliences_boxplot")
    #_save_boxplot(bus_in_service_resiliences_list, "Bus in service resilience scores", plot_output_path, "bus_in_service_resiliences_boxplot")
    #_save_boxplot(line_in_service_resiliences_list, "Line in service resilience scores", plot_output_path, "line_in_service_resiliences_boxplot")
    #_save_boxplot(load_in_service_resiliences_list, "Load in service resilience scores", plot_output_path, "load_in_service_resiliences_boxplot")
    #_save_boxplot(sgen_in_service_resiliences_list, "Sgen in service resilience scores", plot_output_path, "sgen_in_service_resiliences_boxplot")
    #_save_boxplot(storage_in_service_resiliences_list, "Storage in service resilience scores", plot_output_path, "storage_in_service_resiliences_boxplot")
    _save_boxplot(vmpu_bus_in_operating_window_resiliences_list, "Bus voltage in operating range resilience", plot_output_path, "vmpu_bus_in_operating_window_resiliences_boxplot")

def _save_boxplot(data, title, plot_output_path, filename):
    split_size = 20
    num_individuals = len(data)
    num_splits = num_individuals // split_size
    if num_individuals % split_size > 0:
        num_splits = num_splits+1
    for i in range(num_splits):
        current_filename = filename +"_" + str(i)
        start_index = i * split_size
        end_index = (i+1) * split_size
        if end_index > num_individuals:
            end_index = num_individuals - 1
        plt.rc('figure', titlesize=18)
        plt.rc('axes', titlesize=14)
        plt.rc('axes', labelsize=14)
        plt.rc('xtick', labelsize=10)
        plt.rc('ytick', labelsize=12) 
        plt.xlabel('Individual')
        plt.ylabel('Performance loss')
        plt.figure(1, figsize=(18,16), dpi=300)
        plt.boxplot(data[start_index:end_index])
        plt.title(title)
        labels_list = []
        labels_list = [str(x) for x in list(range(start_index+1, end_index+1))]
        plt.xticks(ticks=list(range(1,split_size+1)), labels=labels_list, rotation=45)
        fig_path = os.path.join(plot_output_path, current_filename)
        plt.savefig(fig_path, dpi=300)
        plt.close()

def _t_test_execution(data, significance_level=0.05):
    individual_counters = range(len(data))
    individual_counters = [x+1 for x in individual_counters]
    output_df = pandas.DataFrame({"Individual":individual_counters})
    for i in range(len(data)):
        individual_resiliences = data[i]
        result_list = []
        for j in range(len(data)):
            comparison_resiliences = data[j]
            result = ttest_ind(individual_resiliences, comparison_resiliences, equal_var=False)
            result_list.append(result)
        output_df[str(i+1)] = result_list
    
    significant_t_test_results = 0
    insignificant_t_test_results = 0

    for column in individual_counters:
        column_str = str(column)
        column_df = output_df[["Individual", column_str]]
        column_df = column_df[column_df["Individual"]<column]
        significant_df = column_df[column_df.apply(lambda x: x[column_str][1]<significance_level, axis=1)]
        insignificant_df = column_df[column_df.apply(lambda x: x[column_str][1]>=significance_level, axis=1)]
        num_significant = len(significant_df.index)
        num_insignificant = len(insignificant_df.index)
        significant_t_test_results = significant_t_test_results + num_significant
        insignificant_t_test_results = insignificant_t_test_results + num_insignificant

    return output_df, significant_t_test_results, insignificant_t_test_results

def _t_test_table_export(data, run_id=RUN_ID):
    folder_path = os.path.join('tables', str(run_id))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    table_path = os.path.join(folder_path, 't_test_results_table.tex')
    data.to_latex(table_path, index=False)

if __name__ == "__main__":
    calculate_resilience_statistics()