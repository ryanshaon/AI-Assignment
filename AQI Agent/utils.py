def compute_aqi(pm25, pm10, co, so2, no2):
    """
    Simplified AQI calculation:
    AQI = max of pollutant concentration (scaled approximation)
    """

    # Rough scaling for demonstration
    sub_index_pm25 = pm25
    sub_index_pm10 = pm10 / 2
    sub_index_co = co * 50
    sub_index_so2 = so2
    sub_index_no2 = no2

    return int(max(sub_index_pm25, sub_index_pm10, sub_index_co, sub_index_so2, sub_index_no2))
