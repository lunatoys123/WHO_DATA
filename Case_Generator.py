import pymongo
from bson import ObjectId
import math
import argparse
import random
import names
from datetime import datetime, date, timedelta

parser = argparse.ArgumentParser(description="Case Generator Helper")
parser.add_argument(
    "--num_of_data", help="The number of newly generate data", default=300, type=int)
parser.add_argument("--num_of_Patient",
                    help="The number of newly generate Patient", default=50)
parser.add_argument(
    "--AddPatient", help="Need to Add Patient or Not", default=False, type=bool)
args = parser.parse_args()

client = pymongo.MongoClient(
    "mongodb+srv://lunatoys:lunatoys@cluster0.9yv231a.mongodb.net/Malaria?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["Malaria"]
Doctors = db["Doctor"]
Patient = db["Patient"]
Case = db["Case"]

num_of_data = args.num_of_data
num_of_Patient = args.num_of_Patient
AddPatient = args.AddPatient


def EmailGenerator(Name):

    servers = ['@gmail', '@yahoo', '@redmail', '@hotmail', '@bing']
    servpos = random.randint(0, len(servers)-1)
    email = Name+servers[servpos]
    tlds = ['.com', '.in', '.gov', '.ac.in', '.net', '.org']
    tldpos = random.randint(0, len(tlds)-1)
    email = email+tlds[tldpos]
    return email


def DateGenerator():
    date_1, date_2 = date(2022, 2, 3), date(2023, 2, 3)
    dates_bet = date_2 - date_1
    total_days = dates_bet.days

    random_day = random.randrange(total_days)
    return date_1 + timedelta(days=random_day)


# Generate New Patient
if AddPatient:
    for i in range(0, num_of_Patient):
        Gender = "Male" if random.uniform(0, 1) >= 0.5 else "Female"
        Name = names.get_full_name(gender=Gender)
        Id = "1111"
        Phone = "33442234"
        Age = random.randint(0, 100)
        Home = {
            "Location": "",
            "Telephone": "",
            "Contact_Person": "",
            "Contact_Person_Tel": ""
        }
        Work = {
            "Location": "",
            "Telephone": "",
            "Contact_Person": "",
            "Contact_Person_Tel": ""
        }
        Email = EmailGenerator(Name.replace(" ", "_"))
        insert_Patient = Patient.insert_one({
            "Gender": Gender,
            "Name": Name,
            "Email": Email,
            "Id": Id,
            "Phone": Phone,
            "Age": Age,
            "Home": Home,
            "Work": Work,
            "CreateBy": "System",
            "dtCreated": datetime.now(),
            "UpdateBy": "System",
            "dtUpdated": datetime.now()
        })


# Assign Patient to Doctor

# Get List of Doctors
Normal_Doctors = Doctors.find({"Hospital_id": ObjectId(
    "63142ffb9e02653ba0a25f4e"), "Role": "NU"}, {"Doctor_id": "$_id", "_id": 0})
Normal_Doctors = list(Normal_Doctors)
Normal_Doctors = list(map(lambda x: x["Doctor_id"], Normal_Doctors))

# Get List of Patient
Patient_list = Patient.find({}, {"Patient_id": "$_id", "_id": 0})
Patient_list = list(Patient_list)
Patient_list = list(map(lambda x: x["Patient_id"], Patient_list))


chunk_Size = math.floor(num_of_data / len(list(Normal_Doctors)))

Symptoms_choice = ["Fever", "Headache", "Abdominal pain",
                   "Chills", "Sweats", "Myalgia"]

Clinical_Complications_choice = ["Cerebral malria",
                                 "Spleen ruture", "ARDS pulmonary edma", "Anemia"]
All_Patient_Status = ["survived", "Stable", "Emergency", "Died", "Unknown"]
All_Report_Status = ["Preliminary", "Final"]

new_Case = []
for i in range(0, num_of_data):
    Patient_id = random.choice(Patient_list)
    Symptoms = {
        "Sign": random.choices(Symptoms_choice, k=random.randint(1, 3)),
        "Onset_date": datetime.now(),
        "Remark": "",
        "Symptomatic": "",
    }
    Clinical_Complications = {
        "Complications": random.choices(Clinical_Complications_choice, k=random.randint(1, 3)),
        "Description": ""
    }

    Hospital_count = random.randint(0, 4)
    Travel_count = random.randint(0, 3)

    Hospitalization = []
    Travel_History = []
    for i in range(Hospital_count):
        Admin_Date = DateGenerator()
        Admin_Date = datetime(
            Admin_Date.year, Admin_Date.month, Admin_Date.day)
        Discharge_Date = Admin_Date + timedelta(days=10)
        Hosptial_object = {
            "Hospital": f"hospital {i}",
            "Admit_Date": Admin_Date,
            "City": "city",
            "DisCharge_Date": Discharge_Date
        }
        Hospitalization.append(Hosptial_object)

    for i in range(Travel_count):
        Travel_Date_Start = DateGenerator()
        Travel_Date_Start = datetime(
            Travel_Date_Start.year, Travel_Date_Start.month, Travel_Date_Start.day)
        Travel_Date_end = Travel_Date_Start + timedelta(days=3)
        Location = f"Location {i}"

        Travel_Object = {
            "Date_Start": Travel_Date_Start,
            "Date_End": Travel_Date_end,
            "Location": Location
        }
        Travel_History.append(Travel_Object)

    Previous_Diagnosis_Malaria = {
        "Diagnosed_Malaria_previous": "No"
    }
    Patient_Status = random.choice(All_Patient_Status)
    Status_Date = datetime.now()
    Report_Status = random.choice(All_Report_Status)

    Case_Object = {
        "Patient_id": Patient_id,
        "Symptoms": Symptoms,
        "Clinical_Complications": Clinical_Complications,
        "Hospitalization": Hospitalization,
        "Previous_Diagnosis_Malaria": Previous_Diagnosis_Malaria,
        "Patient_Status": Patient_Status,
        "Status_date": Status_Date,
        "Report_Status": Report_Status,
        "Travel_History": Travel_History,
        "dtCreated": datetime.now(),
        "dtupdated": datetime.now()
    }
    new_Case.append(Case_Object)

new_Case = [new_Case[i:i+chunk_Size]
            for i in range(0, len(new_Case), chunk_Size)]

doctor_to_Case_dict = dict()
for index, case in enumerate(new_Case):
    Doctor_id = Normal_Doctors[index]

    for c in case:
        Case_Object = {**c, "Doctor_id": Doctor_id}
        input_Case = Case.insert_one(Case_Object)
        print("Add Case Successfully")
