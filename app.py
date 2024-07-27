from flask import Flask, request, jsonify, redirect, url_for, render_template_string
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
@app.route('/linkvertise_step1')
def linkvertise_step1():
    user_id = "1208943"
    hwid = request.args.get('hwid')
    target_url = url_for('step1_html', hwid=hwid, _external=True)
    linkvertise_url = f"https://link-to.linkvertise.com/{user_id}?{urlencode({'url': target_url})}"
    return redirect(linkvertise_url)

# Linkvertise 2 yönlendirme
@app.route('/linkvertise_step2')
def linkvertise_step2():
    user_id = "1208943"
    hwid = request.args.get('hwid')
    target_url = url_for('step2_html', hwid=hwid, _external=True)
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
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Linkvertise Step 1</title>
    </head>
    <body>
        <h1>Step 1</h1>
        <a href="/linkvertise_step1?hwid={{ hwid }}">Proceed to Linkvertise Step 1</a>
        <br><br>
        <a href="/step2.html?hwid={{ hwid }}">Next Step</a>
    </body>
    </html>
    ''', hwid=hwid)

@app.route('/step2.html')
def step2_html():
    hwid = request.args.get('hwid')
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Linkvertise Step 2</title>
    </head>
    <body>
        <h1>Step 2</h1>
        <a href="/linkvertise_step2?hwid={{ hwid }}">Proceed to Linkvertise Step 2</a>
        <br><br>
        <a href="/generate_key.html?hwid={{ hwid }}">Generate Key</a>
    </body>
    </html>
    ''', hwid=hwid)

@app.route('/generate_key.html')
def generate_key_html():
    hwid = request.args.get('hwid')
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Generate Key</title>
    </head>
    <body>
        <h1>Generate Key</h1>
        <input type="hidden" id="hwid" value="{{ hwid }}">
        <button onclick="generateKey()">Generate Key</button>
        <p id="keyDisplay"></p>
        <script>
            function generateKey() {
                const hwid = document.getElementById('hwid').value;
                fetch('/generate_key', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ hwid: hwid })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.key) {
                        document.getElementById('keyDisplay').innerText = 'Your Key: ' + data.key;
                    } else {
                        alert('Error generating key.');
                    }
                });
            }
        </script>
    </body>
    </html>
    ''', hwid=hwid)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
