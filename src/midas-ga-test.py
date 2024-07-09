import midas

midas.run(scenario_name="midasmv_der", params={"mosaikdb_params": {"filename": "midasmv_der_modified.hdf5"},
                                               "der_params": {"midasmv": {"mapping": {
                                                   3: [["PV", 10], ["HVAC", 1.279], ["HVAC", 0.343]],
                                                   4: [["CHP", 0.4], ["HVAC", 0.343]],
                                                   7: [["DIESEL", 10]],
                                                   8: [["CHP", 0.4], ["PV", 1]],
                                                   9: [["HVAC", 0.23], ["BAT", 0.08]],
                                                   11: [["Biogas", 2.05], ["BAT", 0.555], ["PV", 1]],
                                                   13: [["HVAC", 0.23], ["PV", 1]],
                                                   14: [["PV", 10], ["HVAC", 1.279]]},
                                                   "weather_provider_mapping": {
                                                   "PV": ["bremen", 0],
                                                   "HVAC": ["bremen", 0],
                                                   "BAT": ["bremen", 0],
                                                   "CHP": ["bremen", 0],
                                                   "Biogas": ["bremen", 0],
                                                   "DIESEL": ["bremen", 0]}
                                               }}})


print("bla")
