import sqlite3
import json
import math
import pandas as pd

DB_NAME = 'pkp-dashboard.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def safe_int(value, default=0):
    """Convert to int safely, replace NaN/None/empty with default."""
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return default
        return int(value)
    except:
        return default

def safe_str(value, default="Kosong"):
    """Convert to str safely, replace NaN/None with default."""
    if value is None:
        return default
    if isinstance(value, float) and math.isnan(value):
        return default
    return str(value).strip()

def seed_indikators_from_excel(excel_path, reset_schema=False):
    if reset_schema:
        with open('schema.sql', 'r') as f:
            conn = get_connection()
            conn.executescript(f.read())
            conn.commit()
            conn.close()

    df = pd.read_excel(excel_path)
    df = df.reset_index(drop=True)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    conn = get_connection()
    c = conn.cursor()

    for _, row in df.iterrows():
        try:
            c.execute("""
                INSERT INTO Indikator 
                (indikator, kriteria_key, capaian, nilai, kriteria, tahun, semester, bukti,
                 Penghargaan_Int, Penghargaan_Nas, Penghargaan_Lok)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                safe_str(row.get("indikator", "")),
                safe_str(row.get("kriteria_key", "")),
                safe_str(row.get("capaian", "")),
                safe_int(row.get("nilai"), default=None),
                safe_str(row.get("kriteria", "")),
                safe_int(row.get("tahun", 2025), default=2025),
                safe_int(row.get("semester", 1), default=1),
                safe_str(row.get("bukti", "Kosong")),
                safe_int(row.get("penghargaan_int", 0)),
                safe_int(row.get("penghargaan_nas", 0)),
                safe_int(row.get("penghargaan_lok", 0))
            ))
        except Exception as e:
            print(f"❌ Error inserting row: {e}")
        

    conn.commit()
    conn.close()
    print("✅ Seeding complete.")

def seed_tlhp_from_excel(excel_path):
    # Initialize database schema
    # with open('schema.sql', 'r') as f:
    #     conn = get_connection()
    #     conn.executescript(f.read())
    #     conn.commit()
    #     conn.close()

    # Load Excel data
    df = pd.read_excel(excel_path, index_col=None)
    df = df.reset_index(drop=True)

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    conn = get_connection()
    c = conn.cursor()

    for _, row in df.iterrows():
        try:
            pemeriksa = str(row.get("pemeriksa", "")).strip()
            no_lhp = str(row.get("no_lhp", "")).strip()
            tanggal = str(row.get("tanggal", "")).strip()  # Expecting YYYY-MM-DD
            obrik = str(row.get("obrik", "")).strip()
            temuan = str(row.get("temuan", "")).strip()
            rekomendasi = str(row.get("rekomendasi", "")).strip()
            rencana_aksi = str(row.get("rencana_aksi", "")).strip()
            status = str(row.get("status", "")).strip()
            hasil_evaluasi = str(row.get("hasil_evaluasi", "")).strip()

            c.execute("""
                INSERT INTO TLHP 
                (pemeriksa, no_lhp, tanggal, obrik, temuan, rekomendasi, rencana_aksi, status, hasil_evaluasi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pemeriksa,
                no_lhp,
                tanggal,
                obrik,
                temuan,
                rekomendasi,
                rencana_aksi,
                status,
                hasil_evaluasi
            ))

        except Exception as e:
            print(f"❌ Error inserting row {row.to_dict()}: {e}")

    conn.commit()
    conn.close()
    print("✅ TLHP seeding complete.")

# ─── USER FUNCTIONS ──────────────────────────────────────────────────────────
def add_user(username, password, unit, is_admin=False):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password, unit, is_admin) VALUES (?, ?, ?, ?)",
                (username, password, unit, is_admin)
            )
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def get_user(username, password):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            return c.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def get_all_users():
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            return c.fetchall()
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []

# ─── INDIKATOR FUNCTIONS ─────────────────────────────────────────────────────

def add_indikator(name, capaian, kategori, nilai, year, bukti):
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO Indikator (name, capaian, kategori, nilai, year, bukti)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, capaian, kategori, json.dumps(nilai), year, bukti))
        return True
    except Exception as e:
        print(f"Error adding indikator: {e}")
        return False

def get_all_indikators():
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Indikator")
            rows = c.fetchall()
            colnames = [desc[0] for desc in c.description]
            return rows, colnames
    except Exception as e:
        print(f"Error fetching all indikators: {e}")
        return []

def get_indikator_by_id(indikator_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Indikator WHERE id = ?", (indikator_id,))
            return c.fetchone()
    except Exception as e:
        print(f"Error fetching indikator by ID: {e}")
        return None

def update_indikator(indikator_id, name, capaian, kategori, nilai, year, bukti):
    try:
        with get_connection() as conn:
            conn.execute("""
                UPDATE Indikator
                SET name = ?, capaian = ?, kategori = ?, nilai = ?, year = ?, bukti = ?
                WHERE id = ?
            """, (name, capaian, kategori, json.dumps(nilai), year, bukti, indikator_id))
        return True
    except Exception as e:
        print(f"Error updating indikator: {e}")
        return False

def delete_indikator(indikator_id):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM Indikator WHERE id = ?", (indikator_id,))
        return True
    except Exception as e:
        print(f"Error deleting indikator: {e}")
        return False
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM Indikator WHERE id = ?", (indikator_id,))
    conn.commit()
    conn.close()

def get_all_tlhp():
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM TLHP")
            return c.fetchall()
    except Exception as e:
        print(f"Error fetching all TLHP: {e}")
        return []
    
def get_tlhp_by_id(tlhp_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM tlhp WHERE id = ?", (tlhp_id,))
            return c.fetchone()
    except Exception as e:
        print(f"Error fetching TLHP by ID: {e}")
        return None


def update_tlhp(tlhp_id, pemeriksa, no_lhp, tanggal, obrik, temuan, rekomendasi, rencana_aksi, status, hasil_evaluasi):
    try:
        with get_connection() as conn:
            conn.execute("""
                UPDATE tlhp
                SET pemeriksa = ?, no_lhp = ?, tanggal = ?, obrik = ?, 
                    temuan = ?, rekomendasi = ?, rencana_aksi = ?, 
                    status = ?, hasil_evaluasi = ?
                WHERE id = ?
            """, (
                pemeriksa, no_lhp, tanggal, obrik, temuan,
                rekomendasi, rencana_aksi, status, hasil_evaluasi, tlhp_id
            ))
        return True
    except Exception as e:
        print(f"Error updating TLHP: {e}")
        return False


def delete_tlhp(tlhp_id):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM tlhp WHERE id = ?", (tlhp_id,))
        return True
    except Exception as e:
        print(f"Error deleting TLHP: {e}")
        return False

def add_tlhp(pemeriksa, no_lhp, tanggal, obrik, temuan, rekomendasi, rencana_aksi, status, hasil_evaluasi):
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO tlhp 
                (pemeriksa, no_lhp, tanggal, obrik, temuan, rekomendasi, rencana_aksi, status, hasil_evaluasi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pemeriksa,
                no_lhp,
                tanggal,
                obrik,
                temuan,
                rekomendasi,
                rencana_aksi,
                status,
                hasil_evaluasi
            ))
        return True
    except Exception as e:
        print(f"Error adding TLHP: {e}")
        return False
