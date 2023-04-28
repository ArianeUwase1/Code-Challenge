#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 20:38:55 2023

@author: arianeuwase
"""

import requests

base_url = ("https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
            "?sf={search_fields}&terms={search_term}&maxList={max_list}")

patient_data = [
    {"patient_id": 0,
     "diagnoses": ["I10", "K21.9"]},
    {"patient_id": 1,
     "diagnoses": ["E78.5", "ABC.123", "U07.1", "J96.00"]},
    {"patient_id": 2,
     "diagnoses": []},
    {"patient_id": 3,
     "diagnoses": ["U07.1", "N18.30"]},
    {"patient_id": 4,
     "diagnoses": ["I10", "E66.9", "745.902"]},
    {"patient_id": 5,
     "diagnoses": ["G47.33", "I73.9", "N18.30", 1]}
]

def solution(data):
    result = []
    
    for patient in data:
        idnum = patient["patient_id"]
        diagnoses = []
        priority_diagnoses = []
        malformed_diagnoses = []
        
        for diagnosis in patient["diagnoses"]:
            url = base_url.format(search_fields="code", search_term=diagnosis, max_list=100)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                diagnose_code = False
                for i in data[3]:
                    if i[0] == diagnosis:
                        diagnose_code = True
                        diagnoses.append((diagnosis, i[1]))
                        if 'covid-19' in i[1].lower() or 'respiratory failure' in i[1].lower():
                            priority_diagnoses.append(i[1])
                if not diagnose_code:
                    malformed_diagnoses.append(diagnosis)
                    
        result.append({
            "patient_id": idnum,
            "diagnoses": diagnoses,
            "priority_diagnoses": priority_diagnoses,
            "malformed_diagnoses": malformed_diagnoses})
        
    result.sort(key=lambda x: len(x["priority_diagnoses"]), reverse=True)
    return result

output = solution(patient_data)

expected_output = [
        {'patient_id': 1,
         'diagnoses': [
             ('E78.5', 'Hyperlipidemia, unspecified'),
             ('U07.1', 'COVID-19'),
             ('J96.00', 'Acute respiratory failure, unspecified whether with hypoxia or hypercapnia')],
         'priority_diagnoses': [
             'COVID-19', 'Acute respiratory failure, unspecified whether with hypoxia or hypercapnia'],
         'malformed_diagnoses': ['ABC.123']
        },
        {'patient_id': 3,
         'diagnoses': [
             ('U07.1', 'COVID-19'),
             ('N18.30', 'Chronic kidney disease, stage 3 unspecified')],
         'priority_diagnoses': ['COVID-19'],
         'malformed_diagnoses': []
        },
        {'patient_id': 0,
         'diagnoses': [
             ('I10', 'Essential (primary) hypertension'),
             ('K21.9', 'Gastro-esophageal reflux disease without esophagitis')],
         'priority_diagnoses': [],
         'malformed_diagnoses': []
        },
        {'patient_id': 2, 'diagnoses': [],
         'priority_diagnoses': [],
         'malformed_diagnoses': []
        },
        {'patient_id': 4,
         'diagnoses': [
             ('I10', 'Essential (primary) hypertension'),
             ('E66.9', 'Obesity, unspecified')],
         'priority_diagnoses': [],
         'malformed_diagnoses': ['745.902']
        },
        {'patient_id': 5,
         'diagnoses': [
             ('G47.33', 'Obstructive sleep apnea (adult) (pediatric)'),
             ('I73.9', 'Peripheral vascular disease, unspecified'),
             ('N18.30', 'Chronic kidney disease, stage 3 unspecified')],
         'priority_diagnoses': [],
         'malformed_diagnoses': [1]
        }
    ]
try:
    assert(output == expected_output)
except AssertionError:
    print('error: your output does not match the expected output')
else:
    print('success!')
    
print("Actual output".ljust(15))
for i in range(len(output)):
    print(str(output[i]).ljust(15))