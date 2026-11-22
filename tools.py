import re
import sqlite3
from rag import load_pdf, chunk_pages, build_index, retrieve

# ---------- Tool 1: search the policy (your Project 1 code) ----------
_cache = {}


def _load():
    """Load and index the policy only once, then reuse it."""
    if "chunks" not in _cache:
        pages = load_pdf("data/policy.pdf")
        chunks = chunk_pages(pages)
        _cache["chunks"] = chunks
        _cache["vectors"] = build_index(chunks)
    return _cache["chunks"], _cache["vectors"]


def search_policy(question, k=5):
    """Return the policy text pieces closest to the question, with page numbers."""
    chunks, vectors = _load()
    results = retrieve(question, chunks, vectors, k=k)
    return "\n\n".join(f"[Page {c['page']}] {c['text']}" for c, _ in results)


# ---------- Tool 2: query the claims table (read-only) ----------
BLOCKED = ["insert", "update", "delete", "drop", "alter", "create",
           "attach", "pragma", "replace", "vacuum"]


def run_sql(query):
    """Run a SELECT query on claims.db. Anything else is blocked."""
    q = query.strip().rstrip(";").strip()
    low = q.lower()

    # Safety check 1: must start with SELECT
    if not low.startswith("select"):
        return "BLOCKED: only SELECT queries are allowed."
    # Safety check 2: only one query at a time
    if ";" in q:
        return "BLOCKED: only one query at a time."
    # Safety check 3: no dangerous words
    for word in BLOCKED:
        if re.search(r"\b" + word + r"\b", low):
            return f"BLOCKED: the word '{word}' is not allowed."

    try:
        # Safety check 4: the database itself is opened in read-only mode
        conn = sqlite3.connect("file:claims.db?mode=ro", uri=True)
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchmany(20)
        columns = [d[0] for d in cur.description]
        conn.close()
    except Exception as e:
        return "SQL ERROR: " + str(e)

    if not rows:
        return "No rows found."
    lines = [" | ".join(columns)]
    for r in rows:
        lines.append(" | ".join(str(x) for x in r))
    return "\n".join(lines)


# ---------- Quick test ----------
if __name__ == "__main__":
    print("--- Test 1: allowed query ---")
    print(run_sql("SELECT claim_id, status FROM claims WHERE claim_amount > 300000"))
    print("\n--- Test 2: dangerous query ---")
    print(run_sql("DELETE FROM claims"))
    print("\n--- Test 3: policy search ---")
    print(search_policy("waiting period for cataract")[:600])