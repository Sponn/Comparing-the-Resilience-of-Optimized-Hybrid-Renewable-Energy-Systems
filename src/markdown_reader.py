def read_bus_health_from_markdown(filepath):
    file = open(filepath, 'r') 
    lines = file.readlines()
    bus_health_line = lines[4]
    bus_health = float(bus_health_line[-8:-3])
    return bus_health



if __name__ == "__main__":
    bus_health = read_bus_health_from_markdown("./_outputs/midasmv_der/midasmv_der_Powergrid-0_report.md")
    print(bus_health)
