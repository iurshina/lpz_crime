import sqlite3

def create_db(db_path='polizei_reports_2023.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ort TEXT,
            zeit TEXT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_leipzig_reports(db_path='polizei_reports_2023.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = """
    SELECT id, ort, zeit, title, content
    FROM reports
    WHERE ort LIKE 'Leipzig%'
    """

    c.execute(query)
    results = c.fetchall() 

    conn.close()  

    return results

def save_to_db(ort, zeit, title, content):
    conn = sqlite3.connect('polizei_reports_2023.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reports (ort, zeit, title, content) VALUES (?, ?, ?, ?)
    ''', (ort, zeit, title, content))
    conn.commit()
    conn.close()