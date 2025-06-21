import dataclasses
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
import glob

CASES_DIR = "data/jus_mundi_hackathon_data/cases/"


# --- Data Loading Classes (as provided) ---
@dataclasses.dataclass
class Opinion:
    title: str
    type: str
    date: Optional[datetime]
    content: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Opinion":
        date_str = data.get("Date")
        return cls(
            title=data["Title"],
            type=data["Type"],
            date=datetime.fromisoformat(date_str) if date_str else None,
            content=data.get("Content", ""),
        )


@dataclasses.dataclass
class Decision:
    title: str
    type: str
    date: Optional[datetime]
    opinions: List[Opinion]
    content: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Decision":
        date_str = data.get("Date")
        return cls(
            title=data["Title"],
            type=data["Type"],
            date=datetime.fromisoformat(date_str) if date_str else None,
            opinions=[Opinion.from_dict(o) for o in data.get("Opinions", [])],
            content=data["Content"],
        )


@dataclasses.dataclass
class Case:
    identifier: str
    title: str
    case_number: Optional[str]
    industries: List[str]
    status: str
    party_nationalities: List[str]
    institution: str
    rules_of_arbitration: List[str]
    applicable_treaties: List[str]
    decisions: List[Decision]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Case":
        return cls(
            identifier=data["Identifier"],
            title=data["Title"],
            case_number=data.get("CaseNumber"),
            industries=data.get("Industries", []),
            status=data["Status"],
            party_nationalities=data.get("PartyNationalities", []),
            institution=data["Institution"],
            rules_of_arbitration=data.get("RulesOfArbitration", []),
            applicable_treaties=data.get("ApplicableTreaties", []),
            decisions=[Decision.from_dict(d) for d in data.get("Decisions", [])],
        )


def load_case_json(case_id: str) -> Optional[Case]:
    """Loads a single case JSON file into a Case object."""
    file_path = os.path.join(CASES_DIR, f"{case_id}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        data = json.load(f)
    return Case.from_dict(data)


def list_cases() -> list[str]:
    json_files = glob.glob(os.path.join(CASES_DIR, "*.json"))
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {CASES_DIR}")
    case_ids = []
    for file_path in json_files:
        case_id = os.path.splitext(os.path.basename(file_path))[0]
        case_ids.append(case_id)
    return case_ids


SAMPLE_USER_QUERY = """
I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this.
Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.

Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?
"""
