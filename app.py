from flask import Flask, request, jsonify, redirect
import sqlite3
import uuid
import hashlib
from urllib.parse import urlencode

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanı kurulum fonksiyonu
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hwid TEXT UNIQUE,
            key TEXT,
            link1_done BOOLEAN DEFAULT FALSE,
            link2_done BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/generate_key', methods=['POST'])
def generate_key():
    hwid = request.json.get('hwid')
    if not hwid:
        return jsonify({'error': 'HWID is required!'}), 400
    
    key = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO keys (hwid, key) VALUES (?, ?)', (hwid, key))
    conn.commit()
    conn.close()
    
    return jsonify({'key': key})

@app.route('/check_key', methods=['GET'])
def check_key():
    hwid = request.args.get('hwid')
    if not hwid:
        return jsonify({'error': 'HWID is required!'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM keys WHERE hwid = ?', (hwid,))
    key_row = cursor.fetchone()
    conn.close()
    
    if key_row:
        return jsonify({'valid': True, 'key': key_row['key']})
    else:
        return jsonify({'valid': False})

@app.route('/linkvertise1', methods=['GET'])
def linkvertise1():
    user_id = "1208943"
    target_url = "YOUR_FIRST_LINKVERTISE_TARGET"
    linkvertise_url = f"https://publisher.linkvertise.com/api/v1/redirect/link/static/{user_id}?{urlencode({'url': target_url})}"
    return redirect(linkvertise_url)

@app.route('/linkvertise2', methods=['GET'])
def linkvertise2():
    user_id = "1208943"
    target_url = "YOUR_SECOND_LINKVERTISE_TARGET"
    linkvertise_url = f"https://publisher.linkvertise.com/api/v1/redirect/link/static/{user_id}?{urlencode({'url': target_url})}"
    return redirect(linkvertise_url)

@app.route('/anti_bypass', methods=['GET'])
def anti_bypass():
    return redirect("YOUR_ANTI_BYPASS_URL")

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
