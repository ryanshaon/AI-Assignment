def classify_aqi(aqi_value):
    if 0 <= aqi_value <= 50:
        return "Good", "Air quality is satisfactory."
    elif 51 <= aqi_value <= 100:
        return "Satisfactory", "Minor breathing discomfort to sensitive people."
    elif 101 <= aqi_value <= 200:
        return "Moderate", "Breathing discomfort to people with lung disease."
    elif 201 <= aqi_value <= 300:
        return "Poor", "Breathing discomfort to most people."
    elif 301 <= aqi_value <= 400:
        return "Very Poor", "Respiratory illness on prolonged exposure."
    elif 401 <= aqi_value <= 500:
        return "Severe", "Affects healthy people and seriously impacts those with diseases."
    else:
        return "Out of Range", "Invalid AQI value."