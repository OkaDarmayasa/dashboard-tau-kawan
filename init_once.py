from db import seed_indikators_from_excel, seed_tlhp_from_excel

# Initialize DB
file_path_indikator = "C:\\Users\\tokoj\\Documents\\Projecct\\PKP-Dashboard\\Ready to Prisma.xlsx"
seed_indikators_from_excel(file_path_indikator, reset_schema=True)

file_path_tlhp = "C:\\Users\\tokoj\\Documents\\Projecct\\PKP-Dashboard\\dataset\\TLHP Combined.xlsx"
seed_tlhp_from_excel(file_path_tlhp)

# import os, sqlite3

# DB_NAME = 'pkp-dashboard.db'
# print("DB absolute path:", os.path.abspath(DB_NAME))

# with sqlite3.connect(DB_NAME) as conn:
#     c = conn.cursor()
#     # list tables
#     c.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     print("Tables:", c.fetchall())
#     # count rows
#     try:
#         c.execute("SELECT COUNT(*) FROM Indikator")
#         print("Indikator rows:", c.fetchone()[0])
#         c.execute("SELECT * FROM Indikator LIMIT 3")
#         for r in c.fetchall():
#             print(r)
#     except sqlite3.OperationalError as e:
#         print("Table check error:", e)
