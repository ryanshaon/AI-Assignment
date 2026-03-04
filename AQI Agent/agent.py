import csv
from utils import compute_aqi
from aqi_rules import classify_aqi


def simple_reflex_agent(file_path):
    print("===== AQI SIMPLE REFLEX AGENT =====\n")

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            location = row["Location"]
            pm25 = float(row["PM2.5"])
            pm10 = float(row["PM10"])
            co = float(row["CO"])
            so2 = float(row["SO2"])
            no2 = float(row["NO2"])

            # Percept from environment
            aqi_value = compute_aqi(pm25, pm10, co, so2, no2)

            # Condition-Action Rule
            category, advisory = classify_aqi(aqi_value)

            print(f"Location: {location}")
            print(f"AQI Value: {aqi_value}")
            print(f"Category: {category}")
            print(f"Health Advisory: {advisory}")
            print("-" * 40)


if __name__ == "__main__":
    simple_reflex_agent("environment_data.csv")
