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
Treatment = db["Treatment"]

existing_Treatment_Case_id = Treatment.distinct("case_id")
existing_Treatment_Case_id = list(existing_Treatment_Case_id)
existing_Treatment_Case_id = list(
    map(lambda x: str(x), existing_Treatment_Case_id))

existing_Case_id = Case.distinct("_id")
existing_Case_id = list(existing_Case_id)
existing_Case_id = list(map(lambda x: str(x), existing_Case_id))

difference_Case_id = list(set(existing_Case_id) -
                          set(existing_Treatment_Case_id))
print(len(difference_Case_id))
TherapyOptions = [
    "Chlorquine",
    "Primaquine",
    "Pyrimethamine-sulfadoxine",
    "Mefloquine",
    "Atovaquone-proguanil",
    "Exchange transfusion",
    "Tetracycline/doxycycline",
    "Quinine/quindine",
    "Other",
]

Drug_Taken_Options = [
    "Chloroquine",
    "Doxycycline",
    "Atovaquone-proguanil",
    "Mefloroquine",
    "Primqauine",
    "Other",
]

for case in difference_Case_id:
    # Generate_Treatment = True if random.randint(0, 10) >= 5 else False
    # if Generate_Treatment:
    case_id = ObjectId(case)
    Therapy = random.choice(TherapyOptions)
    Therapy_Other = ""
    Received = "Yes"
    Chemoprophylaxis_taken = "Yes"
    Drug_taken = random.choice(Drug_Taken_Options)
    Drug_taken_Other = ""
    pills_taken = "No, missed one to few does"
    pills_taken_Other = ""
    missed_dose_reason = ""
    Side_Effect = ""

    Treatment_object = {
        "case_id": case_id,
        "Therapy": Therapy,
        "Therapy_Other": Therapy_Other,
        "Received": Received,
        "Chemoprophylaxis_taken": Chemoprophylaxis_taken,
        "Drug_taken": Drug_taken,
        "Drug_taken_Other": Drug_taken_Other,
        "pills_taken": pills_taken,
        "pills_taken_Other": pills_taken_Other,
        "missed_dose_reason": missed_dose_reason,
        "Side_Effect": Side_Effect,
        "dtCreated": datetime.now(),
        "dtUpdated": datetime.now()
    }

    new_Treatment = Treatment.insert_one(Treatment_object)
    print(f"new Treatment Added for {case_id}")
