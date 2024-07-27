from flask import Flask, request, jsonify, redirect, url_for, render_template
import sqlite3
import uuid
from urllib.parse import urlencode

app = Flask(__name__)

# Veritabanına bağlanma
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanını başlatma
def initialize_database():
    conn = get_db_connection()
    conn.execute('''
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

# Key oluşturma
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

# Key kontrol etme
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

# Linkvertise 1 yönlendirme
@app.route('/linkvertise1')
def linkvertise1():
    user_id = "YOUR_LINKVERTISE_USER_ID"
    target_url = url_for('step1_html', _external=True)
    linkvertise_url = f"https://link-to.linkvertise.com/{user_id}?{urlencode({'url': target_url})}"
    return redirect(linkvertise_url)

# Linkvertise 2 yönlendirme
@app.route('/linkvertise2')
def linkvertise2():
    user_id = "YOUR_LINKVERTISE_USER_ID"
    target_url = url_for('step2_html', _external=True)
    linkvertise_url = f"https://link-to.linkvertise.com/{user_id}?{urlencode({'url': target_url})}"
    return redirect(linkvertise_url)

# Bypass yönergesi
@app.route('/anti_bypass')
def anti_bypass():
    return "Anti-bypass triggered.", 403

# HTML dosyalarını render et
@app.route('/step1.html')
def step1_html():
    hwid = request.args.get('hwid')
    return render_template('step1.html', hwid=hwid)

@app.route('/step2.html')
def step2_html():
    hwid = request.args.get('hwid')
    return render_template('step2.html', hwid=hwid)

@app.route('/generate_key.html')
def generate_key_html():
    hwid = request.args.get('hwid')
    return render_template('generate_key.html', hwid=hwid)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
