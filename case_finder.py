from case import SAMPLE_USER_QUERY
from llm import call_llm_json, MODEL
import pandas as pd


CASES_CSV_PATH = "cases.csv"


def load_cases_prompt() -> str:
    try:
        df_cases = pd.read_csv(CASES_CSV_PATH)
        print(f"Loaded {len(df_cases)} cases from {CASES_CSV_PATH}")
        # Prepare a string representation of the cases for the prompt
        # This includes ID, Title, and Industries for the LLM to analyze
        return "\n".join(
            [
                f"- Case ID: {row['case_id']}, Status: {row['status']}, Title: {row['title']}, Industries: {row['industries']}, Nationalities: {row['nationalities']}"
                for _, row in df_cases.iterrows()
            ]
        )
    except Exception as e:
        print(f"An error occurred while reading the {CASES_CSV_PATH} file: {e}")
        raise


cases_prompt = load_cases_prompt()


def find_cases(user_query: str, top_n: int) -> list[str]:
    prompt = f"""\
Given USER_QUERY and CASES respond with a list of top {top_n} cases relevant to the USER_QUERY which should be read in detail.

Goals:
1. Fact matching
Measure similarity between user’s facts & prior cases (metadata & semantic similarities).
Strong strategies are ones that have previous case law that positively support it. Weak strategies are ones that previous case law do not support it.
Although ALL case law can be relevant, the ones with the most weight are the ones where the elements of the facts are comparable.
2. Weakness detection
Based on previous case law opposing this strategy, if there are at least 1, it should be highlighted. Detecting whether a case is supportive or not supportive of the strategy.

<USER_QUERY>{user_query}</USER_QUERY>
<CASES>
{cases_prompt}
</CASES>

OUTPUT:
.....
```json
["case_1", "...", ...]
```

REMEMBER: at the very end output JSON list with case IDs strings.
"""
    return call_llm_json(prompt=prompt, model=MODEL.GEMINI_PRO)


if __name__ == "__main__":
    print(find_cases(user_query=SAMPLE_USER_QUERY, top_n=8))
