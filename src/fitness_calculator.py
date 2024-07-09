import uuid
import midas.api as midas
from pathlib import Path
from markdown_reader import read_bus_health_from_markdown
import shutil
import multiprocessing as mp
import pandas
import random

def calculate_fitness(individual):
    id = uuid.uuid4()
    db_filename = str(id) + ".hdf5"
    run_params = {"silent": True, "end": 24*60*60*365, "step_size": 60*15, "store_params": {"filename": db_filename},
                                               "der_params": individual, "mosaik_params": {"addr": ("127.0.0.1", 0)}}
    try:
        midas.run(scenario_name="carl_cigre_ts", params=run_params, config='src/classic-arl.yml')
    except ValueError as e:
        print("Exception occured")
        print(e)
        # if run fails (due to non convergence of power flow for example) return absurdly high values for fitness
        return 1+random.random(),100+random.random()

    db_filepath = ("./_outputs/" + db_filename,)
    pysim_data = pandas.read_hdf(db_filepath[0], "Pysimmods__0")
    grid_data = pandas.read_hdf(db_filepath[0], "Powergrid__0")
    lpsp = calculate_lpsp(pysim_data, grid_data)
    coe = calculate_coe(pysim_data, grid_data, individual)
    print("LPSP: " + str(lpsp) + ", COE: " + str(coe))
    return lpsp, coe
    # midas.analyze(scenario_db_path=db_filepath)
    # markdown_filepath = "./_outputs/" + str(id) +"/" + str(id) +"_Powergrid-0_report.md"
    # bus_health = read_bus_health_from_markdown(markdown_filepath)
    # return bus_health

def calculate_lpsp(pysim_data, grid_data):

    individual_load_power = grid_data[[col for col in grid_data.columns if "__load" in col and "p_mw" in col]]
    load_power_sum = individual_load_power.sum(axis=1)

    individual_generator_power = pysim_data[[col for col in pysim_data.columns if "p_mw" in col]]
    generator_power_sum = individual_generator_power.sum(axis=1)

    power_difference_in_grid = (generator_power_sum-load_power_sum)*-1

    power_difference_in_grid = power_difference_in_grid.apply(lambda x: 0 if x < 0 else x)

    total_power_difference_in_grid = power_difference_in_grid.sum()

    total_generator_power = generator_power_sum.sum()

    lpsp = total_power_difference_in_grid/total_generator_power

    if lpsp<0:
        lpsp = 0
    return lpsp

def calculate_coe(pysim_data, grid_data, individual):
    batteries = []
    pvs = []
    diesel_generators = []
    mapping = individual["midasmv"]["mapping"]
    for bus,generators in individual["midasmv"]["mapping"].items():
        for generator in generators:
            if generator[0] == "BAT":
                batteries.append(generator[1])
            elif generator[0] =="PV":
                pvs.append(generator[1])
            elif generator[0] =="DIESEL":
                counter = len(diesel_generators)
                diesel_generators.append([bus, counter, generator[1]])
            else:
                print("Unhandled generator tpye: " + str(generator[0]))
    
    battery_cost = 0
    for charge_discharge_max_kw in batteries:
        # from pysimmods
        capacity = charge_discharge_max_kw*5
        # source: https://www.sciencedirect.com/science/article/abs/pii/S0306261920310199
        cost = 3670.6*pow(capacity,-0.507)
        battery_cost = battery_cost + cost

    pv_cost = 0
    for pv_max_kw in pvs:
        # source: https://www.sciencedirect.com/science/article/abs/pii/S0306261920310199
        cost = 2494.3*pow(pv_max_kw,-0.057)
        pv_cost = pv_cost + cost
    
    diesel_cost = 0
    for diesel_generator in diesel_generators:
        diesel_counter = diesel_generator[1]
        column_name = "DieselGenerator__" + str(diesel_counter) + "___p_mw"
        actual_diesel_generated_power_mw = pysim_data[column_name]
        # simulation stepsize is 15 minutes?
        actual_diesel_generated_power_mwh = actual_diesel_generated_power_mw.sum()/4
        diesel_max_mw = diesel_generator[2]
        # source: https://doi.org/10.1016/j.renene.2018.10.053
        # simulation runs for a day
        fuel_consumption_l = 0.246*actual_diesel_generated_power_mwh+0.08415*diesel_max_mw
        fuel_cost_euro_per_litre = 1.3
        total_fuel_cost = fuel_consumption_l*fuel_cost_euro_per_litre
        # source: https://www.hindawi.com/journals/je/2022/4966761/ sec 2.4
        generator_cost = diesel_max_mw*1000*164

        total_generator_cost = total_fuel_cost+generator_cost

        diesel_cost = diesel_cost + total_generator_cost
    
    total_cost = battery_cost+ pv_cost + diesel_cost

    individual_load_power = grid_data[[col for col in grid_data.columns if "__load" in col and "p_mw" in col]]
    load_power_sum = individual_load_power.sum(axis=1)

    total_load_kwh = load_power_sum.sum()*1000

    coe_euro_per_kwh = total_cost/total_load_kwh
    return coe_euro_per_kwh

def clear_directory():
    output_directory = "./_outputs"
    shutil.rmtree(output_directory)

if __name__ == "__main__":
    der_params = {"midasmv": {"mapping": {
                                                   3: [["PV", 1], ["HVAC", 1.279], ["HVAC", 0.343]],
                                                   4: [["CHP", 0.4], ["HVAC", 0.343]],
                                                   7: [["DIESEL", 1]],
                                                   8: [["CHP", 0.4], ["PV", 1]],
                                                   9: [["HVAC", 0.23], ["BAT", 0.08]],
                                                   11: [["Biogas", 2.05], ["BAT", 0.05], ["PV", 1]],
                                                   13: [["HVAC", 0.23], ["PV", 1]],
                                                   14: [["PV", 1], ["HVAC", 1.279]]},
                                                   "weather_provider_mapping": {
                                                   "PV": ["bremen", 0],
                                                   "HVAC": ["bremen", 0],
                                                   "BAT": ["bremen", 0],
                                                   "CHP": ["bremen", 0],
                                                   "Biogas": ["bremen", 0],
                                                   "DIESEL": ["bremen", 0]}
                                               }}
    
    mp_params = [der_params, der_params, der_params, der_params, der_params, der_params, der_params, der_params]
    # results = []
    # for i in range(5):
    #     results.append(calculate_fitness(der_params))

    # pool= mp.Pool(4)
    # pool.map(calculate_fitness, mp_params)
    # pool.close()
    print("LPSP: " + str(calculate_fitness(der_params)))
    clear_directory()

    #print(results)
