import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Opinion:
    Title: str
    Type: str
    Date: Optional[str]
    Content: str

@dataclass
class Decision:
    Title: str
    Type: str
    Date: Optional[str]
    Opinions: List[Opinion]
    Content: str

@dataclass
class Case:
    Identifier: str
    Title: str
    CaseNumber: Optional[str]
    Industries: List[str]
    Status: str
    PartyNationalities: List[str]
    Institution: str
    RulesOfArbitration: List[str]
    ApplicableTreaties: List[str]
    Decisions: List[Decision]

def load_json(file_path: str) -> Case:
    """Loads a JSON file and converts it into a Case object."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    decisions = [
        Decision(
            Title=d['Title'],
            Type=d['Type'],
            Date=d.get('Date'),
            Opinions=[
                Opinion(
                    Title=o['Title'],
                    Type=o['Type'],
                    Date=o.get('Date'),
                    Content=o.get('Content', '')
                ) for o in d.get('Opinions', [])
            ],
            Content=d.get('Content', '')
        ) for d in data.get('Decisions', [])
    ]

    return Case(
        Identifier=data['Identifier'],
        Title=data['Title'],
        CaseNumber=data.get('CaseNumber'),
        Industries=data.get('Industries', []),
        Status=data['Status'],
        PartyNationalities=data.get('PartyNationalities', []),
        Institution=data['Institution'],
        RulesOfArbitration=data.get('RulesOfArbitration', []),
        ApplicableTreaties=data.get('ApplicableTreaties', []),
        Decisions=decisions
    )

def load_all_cases_to_csv(directory_path: str, output_csv_path: str):
    """
    Loads all *.json files from a directory, extracts a list of titles,
    industries, case id, and status, and saves them as a CSV file.
    """
    import csv
    import os

    all_cases = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            case = load_json(file_path)
            all_cases.append({
                'case_id': os.path.splitext(filename)[0],
                'title': case.Title,
                'industries': ', '.join(case.Industries),
                'status': case.Status
            })

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['case_id', 'title', 'industries', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_cases)
    print(f"Successfully created {output_csv_path}")

load_all_cases_to_csv('data\jus_mundi_hackathon_data\cases', 'cases.csv')
