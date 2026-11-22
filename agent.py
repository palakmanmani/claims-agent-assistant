import time
from google.genai import types
from rag import client, MODEL
from tools import search_policy, run_sql


def search_policy_tool(question: str) -> str:
    """Search the insurance policy document. Use this for questions about
    coverage, waiting periods, exclusions, limits, rules and claim procedures.
    Returns policy text with page numbers."""
    print(f"\n  [Tool used: policy search] {question}")
    return search_policy(question)


def query_claims_database(sql_query: str) -> str:
    """Run a read-only SQLite SELECT query on the claims table. Use this for
    questions about specific claims, amounts, statuses, cities or rejection
    reasons. Returns the matching rows."""
    print(f"\n  [Tool used: SQL] {sql_query}")
    return run_sql(sql_query)


SYSTEM = """You are an insurance claims assistant with two tools.

Tool 1, search_policy_tool: searches the policy document (rules, waiting periods, exclusions, limits).
Tool 2, query_claims_database: runs a read-only SQL SELECT on a SQLite table.

The table is called claims with columns:
claim_id, holder, city, treatment, claim_amount (rupees), status ('Approved' or 'Rejected'),
rejection_reason, claim_date.

Rules:
- Questions about policy rules: use the policy tool.
- Questions about claim data: use the SQL tool.
- Questions like "why was claim X rejected": check the claim with SQL first, then search the policy for the matching rule.
- Answer only from tool results. Never invent facts or numbers.
- Mention the policy page numbers you used.
- If the policy tool does not contain the answer, say "I could not find this in the policy."
- Keep answers short and clear."""


def ask_agent(question):
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM,
                    tools=[search_policy_tool, query_claims_database],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        maximum_remote_calls=6
                    ),
                ),
            )
            return response.text
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                print("  Google is busy. Waiting 60 seconds, then trying again...")
                time.sleep(60)
            else:
                return "ERROR: " + str(e)
    return "ERROR: Google is still busy. Please try again later."


if __name__ == "__main__":
    print("Claims assistant ready. Type quit to exit.")
    while True:
        q = input("\nAsk a question: ")
        if q.lower() == "quit":
            break
        print("\nAnswer:", ask_agent(q))