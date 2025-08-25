CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    unit TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
);
DROP TABLE IF EXISTS Indikator;

CREATE TABLE IF NOT EXISTS Indikator (
    No INTEGER PRIMARY KEY AUTOINCREMENT, -- your numbering column
    indikator TEXT NOT NULL,               -- full human-readable indikator
    kriteria_Key TEXT,                     -- the mapped key for scoring
    capaian TEXT,                           -- raw capaian value (string, number, or "Kosong")
    nilai INTEGER,                          -- computed score
    kriteria TEXT,                          -- computed kategori
    tahun INTEGER NOT NULL,                 -- year
    semester INTEGER NOT NULL,              -- semester number (1 or 2)
    bukti TEXT,                             -- reference to evidence file or description
    Penghargaan_Int INTEGER DEFAULT 0,      -- count for internasional awards
    Penghargaan_Nas INTEGER DEFAULT 0,      -- count for nasional awards
    Penghargaan_Lok INTEGER DEFAULT 0       -- count for lokal awards
);

DROP TABLE IF EXISTS TLHP;

CREATE TABLE IF NOT EXISTS TLHP (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- unique row identifier
    pemeriksa TEXT NOT NULL,                -- e.g., bpk, itjen, apip, bpkp
    no_lhp TEXT NOT NULL,                   -- report number, might contain letters/numbers
    tanggal DATE NOT NULL,                  -- date of the report
    obrik TEXT,                             -- audited entity/obrik
    temuan TEXT,                            -- findings (free text)
    rekomendasi TEXT,                       -- recommendations (free text)
    rencana_aksi TEXT,                      -- planned actions (free text)
    status TEXT,                            -- status of follow-up (e.g., 'selesai', 'proses')
    hasil_evaluasi TEXT                     -- evaluation result (free text / summary)
);