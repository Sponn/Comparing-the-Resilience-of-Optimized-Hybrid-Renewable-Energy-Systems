import pandas
from pandasgui import show

# possible key values: ['CommercialData__0', 'Powergrid__0', 'Pysimmods__0', 'SmartNordData__0', 'TimeSim__0', 'WeatherData__0']

# most useful:

df = pandas.read_hdf('_outputs/d98e87d8-d64d-11ee-b430-00155db1ed53_individual_0_2.hdf5', 'Powergrid__0')

show(df)