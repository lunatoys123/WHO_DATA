import requests
import pymongo
import statistics
import math

WHO_request = requests.get(
    "https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'Malaria')")


data = WHO_request.json()
data = data["value"]

data = list(map(lambda x: x["IndicatorCode"], data))

# client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient(
    "mongodb+srv://lunatoys:lunatoys@cluster0.9yv231a.mongodb.net/Malaria?retryWrites=true&w=majority")
db = client["Malaria"]

WHO_db = db["WHO_DATA"]

for d in data:
    data_dict = dict()
    Indicator_request = requests.get(f"https://ghoapi.azureedge.net/api/{d}")
    Indicator_data = Indicator_request.json()
    Indicator_data = Indicator_data["value"]

    WHO_data = list(map(lambda x: {"Year": x["TimeDim"], "low": x["Low"],
                                   "value": x["NumericValue"], "High": x["High"],
                                   "country_code": x["SpatialDim"]}, Indicator_data))

    for WHO in WHO_data:
        if WHO["country_code"] not in data_dict.keys():
            data_dict[WHO["country_code"]] = [{"Year": WHO["Year"], "low": WHO["low"],
                                               "value": WHO["value"], "High": WHO["High"]}]
        else:
            data_dict[WHO["country_code"]].append({"Year": WHO["Year"], "low": WHO["low"],
                                                   "value": WHO["value"], "High": WHO["High"]})

    for key in data_dict.keys():
        # print(key)
        # print(data_dict[key])

        data_values = list(
            map(lambda x: x["value"] if x["value"] is not None else 0, data_dict[key]))
        sum = math.fsum(data_values)
        mean = round((sum / len(data_values)), 2)
        max_value = round(max(data_values), 2)
        min_value = round(min(data_values), 2)
        standard_deviation = round(statistics.stdev(
            data_values), 2) if len(data_values) > 1 else 0
        variance = round(statistics.variance(
            data_values), 2) if len(data_values) > 1 else 0
        WHO_db.update_one(
            {"Indication_code": d, "country_code": key},
            {"$set": {"Indication_code": d, "country_code": key, "data": data_dict[key], "Analytics": {
                "sum": sum, "mean": mean, "max": max_value, "min": min_value, "std": standard_deviation, "variance": variance}}},
            upsert=True)
        print(f"data inserted for {d} and country {key}")
