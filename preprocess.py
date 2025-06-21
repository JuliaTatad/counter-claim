# pip install google-genai dotenv tqdm

import csv
from case import list_cases, load_case_json
from tqdm import tqdm


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

    with open("cases.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "status", "nationalities", "title", "industries"])
        writer.writerows(cases_data)


if __name__ == "__main__":
    process_all_cases()
