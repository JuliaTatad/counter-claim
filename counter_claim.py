from case import SAMPLE_USER_QUERY
from case_finder import find_cases
from case_summarizer import case_summary
from llm import call_llm, MODEL
from tqdm import tqdm


def make_counter_claim(user_query: str):
    print("USER QUERY:")
    print(user_query)
    print("-----")
    print("Finding relevant cases...")
    case_ids = find_cases(user_query=SAMPLE_USER_QUERY, top_n=8)
    print(f"Found relevant cases: {case_ids}")
    case_summaries = []
    for case_id in tqdm(case_ids, desc="Summarazing cases"):
        case_summaries.append(case_summary(case_id=case_id, user_query=user_query))
    print("Producing report...")
    summaries_str = "\n\n".join(case_summaries)
    prompt = f"""Produce comprehensive precise report satisfying:    

1. Legal source retrieval
Retrieve all relevant legal sources from Jus Mundi (using available API)
Strategies need to be backed by legal sources: we will scope down this initiative to only including case law available through the API.
2. Fact matching
Measure similarity between user’s facts & prior cases (metadata & semantic similarities).
Strong strategies are ones that have previous case law that positively support it. Weak strategies are ones that previous case law do not support it.
Although ALL case law can be relevant, the ones with the most weight are the ones where the elements of the facts are comparable.
3. Weakness detection
Based on previous case law opposing this strategy, if there are at least 1, it should be highlighted. Detecting whether a case is supportive or not supportive of the strategy.
A weakness can be detected if the strategy is usually rejected by tribunals, or the risk that a strong jurisprudence exists that the opponent counsel can use to counter-argue.
4. UI
Structured visual output: tabular with columns for retrieved sources.
Users want to absorb complex info at a glance. They need to compare sources quickly, spot inconsistencies, and justify conclusions easily. Anything from tabular, to the way the information is structured in a particular order, to interactive UI can help (and even more). Be creative!
5. Legal source breakdown
Adds additional layered insights to each retrieved case: global summary, each of the parties’ arguments about the topic, the reasoning of the tribunal, how is it cited by others.
Users want to transparency and depth. They don’t just want the AI’s final conclusion, they want to see the reasoning and supporting evidence so they can evaluate it themselves.
6. Predictive analysis
Estimate likely a tribunal’s response and/or chances of succeeding metric
Users want to assess risk and plan accordingly. They’re looking for informed guidance, not just raw facts. A predictive signal helps them make smarter, faster decisions under uncertainty.
7. Strategy rewriter
Suggest stronger or safer version of the strategy, if needed
Act as a thought partner. User expects support in refining their arguments and exploring alternatives, especially when the stakes are high or the answer is ambiguous.

<USER_QUERY>{user_query}</USER_QUERY>

<CASES>
{summaries_str}
</CASES>

REMEMBER: do NOT start your report with "Of course. Here is a report...", get straight to the report.
"""
    with open("report_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    response = call_llm(prompt=prompt, model=MODEL.GEMINI_PRO)
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(response)
    return response


if __name__ == "__main__":
    print(make_counter_claim(user_query=SAMPLE_USER_QUERY))
