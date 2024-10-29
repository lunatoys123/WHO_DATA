import pymongo
from bson import ObjectId
import math
import argparse
import random
import names
from datetime import datetime, date, timedelta

client = pymongo.MongoClient(
    "mongodb+srv://lunatoys:lunatoys@cluster0.9yv231a.mongodb.net/Malaria?retryWrites=true&w=majority")

db = client["Malaria"]
Doctors = db["Doctor"]
Patient = db["Patient"]
Case = db["Case"]

# fix Patient Ages
# Patient_objects = Patient.find({}, {"Age": 1})
# Patient_objects = list(Patient_objects)
# Patient_objects = list(
#     map(lambda x: {"_id": x["_id"], "Age": int(x["Age"])}, Patient_objects))

# for p in Patient_objects:
#     Fix_Patient = Patient.update_one({"_id": ObjectId(p["_id"])}, {
#                                      "$set": {"_id": ObjectId(p["_id"]), "Age": p["Age"]}})
#     print("Fix Patient successfullys")


def EmailGenerator(Name):
    servers = ['@gmail', '@yahoo', '@redmail', '@hotmail', '@bing']
    servpos = random.randint(0, len(servers)-1)
    email = Name+servers[servpos]
    tlds = ['.com', '.in', '.gov', '.ac.in', '.net', '.org']
    tldpos = random.randint(0, len(tlds)-1)
    email = email+tlds[tldpos]
    return email


Patient_Objects = Patient.find({"Email": {"$exists": False}}, {"Name": 1})
Patient_Objects = list(Patient_Objects)

for p in Patient_Objects:
    Fix_Patient = Patient.update_one({"_id": ObjectId(p["_id"])}, {
                                    "$set": {"_id": ObjectId(p["_id"]), "Email": EmailGenerator(p["Name"].replace(" ", "_"))}})
    print("Fix Patient successfully")
