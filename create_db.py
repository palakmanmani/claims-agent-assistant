import sqlite3

conn = sqlite3.connect("claims.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS claims")
cur.execute("""
CREATE TABLE claims (
    claim_id TEXT,
    holder TEXT,
    city TEXT,
    treatment TEXT,
    claim_amount INTEGER,
    status TEXT,
    rejection_reason TEXT,
    claim_date TEXT
)
""")

rows = [
    ("C1001", "Asha Verma", "Noida", "Cataract surgery", 45000, "Rejected", "Cataract surgery within 24-month waiting period", "2026-01-12"),
    ("C1002", "Rohit Sharma", "Delhi", "Appendectomy", 85000, "Approved", None, "2026-01-20"),
    ("C1003", "Neha Gupta", "Ghaziabad", "Maternity delivery", 120000, "Rejected", "Maternity not covered; Optional Maternity Cover not opted", "2026-02-03"),
    ("C1004", "Imran Khan", "Mumbai", "Knee replacement", 260000, "Rejected", "Joint replacement within 24-month waiting period, not due to accident", "2026-02-14"),
    ("C1005", "Priya Nair", "Kochi", "Dengue hospitalisation", 38000, "Approved", None, "2026-02-25"),
    ("C1006", "Vikram Singh", "Gurgaon", "Cosmetic rhinoplasty", 150000, "Rejected", "Cosmetic surgery is excluded", "2026-03-05"),
    ("C1007", "Anita Desai", "Pune", "Admission for diagnostic evaluation", 22000, "Rejected", "Admission only for diagnostics and evaluation is excluded", "2026-03-18"),
    ("C1008", "Karan Mehta", "Noida", "Fracture surgery after road accident", 175000, "Approved", None, "2026-03-29"),
    ("C1009", "Sunita Rao", "Hyderabad", "Hernia repair", 70000, "Rejected", "Hernia within 24-month waiting period", "2026-04-10"),
    ("C1010", "Deepak Joshi", "Delhi", "Heart bypass surgery", 520000, "Approved", None, "2026-04-22"),
    ("C1011", "Meera Iyer", "Chennai", "Diabetes complications", 95000, "Rejected", "Pre-existing disease within 24-month waiting period", "2026-05-06"),
    ("C1012", "Arjun Patel", "Ahmedabad", "Kidney stone removal", 60000, "Rejected", "Urinary stones within 24-month waiting period", "2026-05-19"),
    ("C1013", "Sana Sheikh", "Mumbai", "Pneumonia hospitalisation", 54000, "Approved", None, "2026-06-02"),
    ("C1014", "Rahul Yadav", "Ghaziabad", "IVF fertility treatment", 300000, "Rejected", "Infertility treatment is excluded", "2026-06-15"),
    ("C1015", "Pooja Bansal", "Noida", "Appendicitis surgery", 72000, "Approved", None, "2026-07-01"),
    ("C1016", "Manoj Kumar", "Patna", "Hypertension treatment", 18000, "Rejected", "Hypertension within 90 days of first policy start", "2026-07-14"),
    ("C1017", "Kavita Reddy", "Bengaluru", "Angioplasty", 310000, "Approved", None, "2026-08-08"),
    ("C1018", "Aman Tiwari", "Delhi", "Dental implants", 80000, "Rejected", "Dental treatment excluded unless due to accident", "2026-08-21"),
    ("C1019", "Ritu Malhotra", "Gurgaon", "Chemotherapy day care", 140000, "Approved", None, "2026-09-09"),
    ("C1020", "Sandeep Das", "Kolkata", "Weight loss surgery", 400000, "Rejected", "Obesity surgery excluded unless BMI and doctor conditions are met", "2026-10-03"),
]

cur.executemany("INSERT INTO claims VALUES (?,?,?,?,?,?,?,?)", rows)
conn.commit()

total = cur.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
rejected = cur.execute("SELECT COUNT(*) FROM claims WHERE status = 'Rejected'").fetchone()[0]
print("Created", total, "claims. Rejected:", rejected)
conn.close()