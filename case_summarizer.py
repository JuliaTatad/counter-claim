from case import load_case_json, SAMPLE_USER_QUERY
from llm import call_llm, MODEL, llm_thread_pool
import copy
import yaml
from tqdm import tqdm
from concurrent.futures import as_completed


def case_summary(case_id: str, user_query: str):
    case = load_case_json(case_id=case_id)
    case_copy = copy.deepcopy(case)
    for decision in case_copy.decisions:
        decision.content = None
        decision.opinions = None
    case_without_decisions_yaml = yaml.dump(case_copy, sort_keys=False)

    def process_decision(decision):
        decision_content = decision.content
        decision.content = None
        decision.opinions = None
        prompt = f"""Analyze the full DECISION text provided below. Create a structured summary of the findings on the following topics, but ONLY if they are relevant to the USER_QUERY:
1.  **Jurisdiction over Counterclaim**: Did the tribunal accept jurisdiction over the state's counterclaim? What was the reasoning (e.g., 'close connection' test)?
2.  **Merits of Counterclaim - Causation**: What was the tribunal's finding on the causal link between the investor's actions and the alleged damage? What was the standard of proof required? How was evidence like expert reports treated?
3.  **Merits of Counterclaim - Quantum**: How did the tribunal assess the damages claimed by the state? Did it accept the claimed amount? What methodology did it use? State the amounts claimed vs. awarded if available.
4.  **Overall Outcome**: Briefly state the final outcome regarding the counterclaim.

If DECISION_CONTENT is not relevant to USER_QUERY respond with NOT_RELEVANT.

<USER_QUERY>{user_query}</USER_QUERY>
<CASE>
{case_without_decisions_yaml}
</CASE>
<DECISION>
{yaml.dump(decision)}
</DECISION>
<DECISION_CONTENT>
{decision_content}
</DECISION_CONTENT>

REMEMBER: do NOT include introductory sentences such as "Here is the summary:"
"""
        response = call_llm(prompt=prompt, model=MODEL.GEMINI_FLASH_LIGHT)
        decision.content = response
        return decision

    with tqdm(total=len(case.decisions), desc=f"Reading case_id={case_id}") as pbar:
        futures = [
            llm_thread_pool.submit(process_decision, decision)
            for decision in case.decisions
        ]
        for future in as_completed(futures):
            pbar.update(1)

    # Remove NOT_RELEVANT decisions.
    case.decisions = [
        d
        for d in case.decisions
        if d.content is None or "NOT_RELEVANT" not in str(d.content)
    ]
    case_str = f"""CASE_ID: {case_id}
IDENTIFIER: {case.identifier}
TITLE: {case.title}
CASE_NUMBER: {case.case_number}

INDUSTRIES:
{"".join([f"- {industry}{chr(10)}" for industry in getattr(case, "industries", [])])}

STATUS: {case.status}

PARTY_NATIONALITIES:
{"".join([f"- {nat}{chr(10)}" for nat in getattr(case, "party_nationalities", [])])}

INSTITUTION: {case.institution}

RULES_OF_ARBITRATION:
{"".join([f"- {rule}{chr(10)}" for rule in getattr(case, "rules_of_arbitration", [])])}

APPLICABLE_TREATIES:
{"".join([f"- {treaty}{chr(10)}" for treaty in getattr(case, "applicable_treaties", [])])}

DECISIONS:
{
        "".join(
            [
                f'''- TITLE: {getattr(decision, "title", "")}
  TYPE: {getattr(decision, "type", "")}
  DATE: {getattr(decision, "date", "")}
  CONTENT: |
{str(decision.content).rstrip()}
'''
                for decision in getattr(case, "decisions", [])
            ]
        )
    }
"""
    return case_str


if __name__ == "__main__":
    print(case_summary(case_id="502", user_query=SAMPLE_USER_QUERY))
