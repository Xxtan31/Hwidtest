from flask import Flask, request, jsonify, render_template, redirect
import random
import string
import requests

app = Flask(__name__)

# Bu sözlük, gerçek uygulamada bir veritabanı ile değiştirilmelidir
hwid_keys = {}

LINKVERTISE_API_URL = 'https://publisher.linkvertise.com/api/v1/redirect/link/'
LINKVERTISE_USER_ID = '1208943'  # LinkVertise kullanıcı ID'nizi buraya girin

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-key')
def get_key():
    hwid = request.args.get('hwid')
    if not hwid:
        return "HWID is required", 400

    # LinkVertise URL'sini oluştur
    linkvertise_url = f"https://link-to.net/{LINKVERTISE_USER_ID}/dynamic?random=1&to={request.url_root}generate-key?hwid={hwid}"
    return redirect(linkvertise_url)

@app.route('/generate-key')
def generate_key_route():
    hwid = request.args.get('hwid')
    if not hwid:
        return "HWID is required", 400

    # LinkVertise tamamlanma kontrolü (gerçek uygulamada API kullanılmalıdır)
    # Bu örnek her zaman başarılı kabul eder
    key = generate_key()
    hwid_keys[hwid] = key
    return render_template('key_generated.html', key=key)

@app.route('/api/check-key')
def check_key():
    key = request.args.get('key')
    hwid = request.args.get('hwid')
    if not key or not hwid:
        return jsonify({"valid": False}), 400

    if hwid in hwid_keys and hwid_keys[hwid] == key:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})

if __name__ == '__main__':
    app.run(debug=True)
