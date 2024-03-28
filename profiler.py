import pandas as pd
import demandlib.bdew as bdew
import datetime
import matplotlib.pyplot as plt

class EnergyDemandProfile:
    """
    Description: #TODO: Describing class, methods and params
    """
    def __init__(self, year, temperature_data, holidays):
        self.year = year
        self.temperature = temperature_data
        self.holidays = holidays
        self.demand_time_series = pd.date_range(start=datetime.datetime(year, 1, 1, 0),
                                                end=datetime.datetime(year, 12, 31, 23),
                                                freq='H')

    def create_heat_demand_profile(self, building_type, building_class, wind_class, ww_incl, annual_heat_demand):
        heat_demand = bdew.HeatBuilding(self.demand_time_series, holidays=self.holidays, temperature=self.temperature,
                                        shlp_type=building_type, building_class=building_class, 
                                        wind_class=wind_class, ww_incl=ww_incl, annual_heat_demand=annual_heat_demand, 
                                        name=building_type).get_bdew_profile()
        
        return heat_demand
    
    def create_power_demand_profile(self, annual_electricity_demand_per_sector):
        elec_slp = bdew.ElecSlp(self.year, holidays=self.holidays)
        # Further logic
        elec_demand = elec_slp.get_profile(annual_electricity_demand_per_sector)

        return elec_demand

    def create_industrial_demand_profile(self):
        pass
    
    def simple_plot(self, df):
        if plt is not None:
            # Plot demand of building
            ax = df.plot()
            ax.set_xlabel("Date")
            ax.set_ylabel("Demand in [kW]")
            ax.grid()
            plt.show()
        else:
            print(f'Annual demand: {df.sum()}')

    def area_chart(self, df):
        if plt is not None:
            # Plot demand of building
            ax = df.plot.area()
            ax.set_xlabel("Date")
            ax.set_ylabel("Demand in [kW]")
            plt.show()
        else:
            print(f'Annual demand: {df.sum()}')

    def export_csv(self, df, filename):
        df.to_csv(filename + '.csv')


# main
if __name__ == "__main__":
    # Beispiel zur Verwendung der Klasse
    # T: Daily mean temperature 2 meters above the ground (simple mean or "geometric series", which means a weighted sum over the previous days).
    temperature_data = pd.read_csv('example_data.csv')["temperature"]

    # A dictionary for holidays can be created by "workalendar"
    # pip3 install workalendar
    # >>> from workalendar.europe import Germany
    # >>> cal = Germany()
    # >>> holidays = dict(cal.holidays(2010))
    holidays = {
            datetime.date(2010, 5, 24): 'Whit Monday',
            datetime.date(2010, 4, 5): 'Easter Monday',
            datetime.date(2010, 5, 13): 'Ascension Thursday',
            datetime.date(2010, 1, 1): 'New year',
            datetime.date(2010, 10, 3): 'Day of German Unity',
            datetime.date(2010, 12, 25): 'Christmas Day',
            datetime.date(2010, 5, 1): 'Labour Day',
            datetime.date(2010, 4, 2): 'Good Friday',
            datetime.date(2010, 12, 26): 'Second Christmas Day'}
    
    # set up time data
    year = 2010
    resolution = 365
    freq = 'D'

    # dataframe for collecting generated profiles
    demand = pd.DataFrame(
            index=pd.date_range(datetime.datetime(year, 1, 1, 0),
                                periods=resolution, freq=freq))

    energy_profile = EnergyDemandProfile(2010, temperature_data, holidays)

    # example profiles: param building_type > 0
    demand['efh'] = energy_profile.create_heat_demand_profile('efh', 1, 0, 1, 20000)
    demand['mfh'] = energy_profile.create_heat_demand_profile('mfh', 1, 0, 1, 20000)
    # except for the classes 'efh' and 'mfh', the building type parameter has to be '0'
    demand['gmk'] = energy_profile.create_heat_demand_profile('gmk', 0, 0, 1, 20000)
    demand['gha'] = energy_profile.create_heat_demand_profile('gha', 0, 0, 1, 20000)

    # power_demand = energy_profile.create_power_demand_profile({'g0':3000})
    # power_demand = power_demand.resample('H').mean()

    # plot stacked area chart for further usage
    energy_profile.area_chart(demand)
