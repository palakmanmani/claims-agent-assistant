# Insurance Claims Assistant Agent (LLM + RAG + SQL)

An AI agent that answers insurance questions by choosing between two tools: a search over a policy document (RAG) and a read-only SQL query on a claims database. For questions like "Why was claim C1001 rejected?" it uses both, linking the claim data to the matching policy rule.

## Why I built this
Information in an insurance company lives in two places: policy documents and claims data. A normal chatbot cannot use both. This agent decides by itself which tool to use for each question.

## How it works
1. The user asks a question in plain English
2. Gemini decides which tool to call: policy search, claims database, or both
3. Policy search finds the closest policy text with sentence-transformers and returns page numbers
4. The claims tool runs a SQL SELECT query on a SQLite table
5. Gemini writes the final answer using only what the tools returned

## Safety
The SQL tool is read-only, with four layers:
- Only queries that start with SELECT are allowed
- Only one query at a time
- Words like DELETE, DROP, UPDATE and INSERT are blocked
- The database is opened in read-only mode

## Example run
Q: Why was claim C1001 rejected?
Tools used: SQL (looked up the claim), then policy search (cataract waiting period)
A: Cataract surgery falls under the 24-month waiting period for listed conditions (policy pages 21-22).

Q: Show all rejected claims above 100000
Tool used: SQL
A: Lists the rejected claims above 1 lakh from the claims table.

## Tech stack
## Results
I wrote 10 test questions (evaluate_agent.py) and checked both the answer and which tools the agent used.

- 10 of 10 passed, with 0 errors
- 4 SQL questions (counts, totals, city, claim amount): correct
- 2 policy questions: correct, including the Worldwide Cover co-payment that failed in my first project
- 2 "why was this claim rejected" questions: the agent used both tools correctly
- Safety test: when asked to delete all rejected claims, the table stayed untouched (20 of 20 rows)
- A question the policy cannot answer: the agent said it could not find it

This is a small test on made-up data, so it shows the idea works, not that it is production-ready.

## How to run
1. Create a virtual environment and run: pip install -r requirements.txt
2. Create a .env file with GEMINI_API_KEY=your_key
3. Run: python create_db.py
4. Run: python agent.py

## Limitations
- Tested on a small set of 10 questions (small, so it does not prove the agent is perfect)