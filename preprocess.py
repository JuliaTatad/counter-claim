# pip install google-genai dotenv tqdm
# python -m venv .venv


import json
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from tqdm import tqdm

import csv
from case import list_cases, load_case_json

load_dotenv()
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def llm(prompt: str, big_model: bool = False) -> str:
    model = "gemini-2.5-pro" if big_model else "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        response_mime_type="text/plain",
    )

    response_text = ''
    stream = gemini_client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    with tqdm(unit='token', unit_scale=True, desc=f"Calling {model}") as pbar:
        for chunk in stream:
            response_text += chunk.text
            pbar.update(len(chunk.text))
            
    return response_text

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
                'status': case.Status,
                'nationalities': ', '.join(case.PartyNationalities)
            })

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['case_id', 'title', 'industries', 'status', 'nationalities']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_cases)
    print(f"Successfully created {output_csv_path}")

from case import list_cases, load_case_json

#load_all_cases_to_csv('data\jus_mundi_hackathon_data\cases', 'cases.csv')
print(llm(prompt="hello"))

def process_all_cases():
    """
    Loads all cases from the data directory, extracts relevant data,
    and saves it as a CSV file named cases.csv, sorted by industry.
    """

    cases_data = []
    for case_id in tqdm(list_cases()):
        case = load_case_json(case_id=case_id)
        industries_str = ", ".join(case.industries)
        party_nationalities_str = ", ".join(case.party_nationalities)
        cases_data.append(
            [case_id, case.status, party_nationalities_str, case.title, industries_str]
        )

    with open("cases.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Status", "Nationalities", "Title", "Industries"])
        writer.writerows(cases_data)


if __name__ == "__main__":
    process_all_cases()