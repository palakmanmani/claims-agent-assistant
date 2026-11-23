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
Python, Gemini API (function calling), sentence-transformers, pypdf, SQLite

## How to run
1. Create a virtual environment and run: pip install -r requirements.txt
2. Create a .env file with GEMINI_API_KEY=your_key
3. Run: python create_db.py
4. Run: python agent.py

## Limitations
- The claims data is made up for demonstration
- Tested manually on a few questions so far, not on a full test set yet
- The free Gemini plan has usage limits, so answers can be slow
- Next: build a test set and measure accuracy, as I did in my first project (policy-rag-assistant)