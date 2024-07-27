from flask import Flask, request, jsonify, redirect
import random
import string
import hashlib
import requests

app = Flask(__name__)

keys = {}
hwids = {}

LINKVERTISE_API_KEY = "cdc7dfa708fe5e9c06eff796927e3efaf209adc5551cbf2adb40615b94623ada"
LINKVERTISE_USER_ID = "1208943"

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

@app.route('/verify_hwid', methods=['POST'])
def verify_hwid():
    data = request.json
    user_id = data['userId']
    device_id = data['deviceId']
    client_version = data['clientVersion']

    unique_string = f"{user_id}-{device_id}-{client_version}"
    hashed_hwid = hashlib.sha256(unique_string.encode()).hexdigest()

    if hashed_hwid not in hwids:
        hwids[hashed_hwid] = {'userId': user_id, 'deviceId': device_id}

    return jsonify({'valid': True, 'hwid': hashed_hwid})

@app.route('/generate', methods=['POST'])
def generate():
    hwid = request.json['hwid']
    key = generate_key()
    keys[key] = {'hwid': hwid, 'uses': 0}
    return jsonify({'key': key})

@app.route('/check', methods=['GET'])
def check():
    key = request.args.get('key')
    hwid = request.args.get('hwid')
    
    if key in keys and keys[key]['hwid'] == hwid:
        keys[key]['uses'] += 1
        return jsonify({'valid': True})
    return jsonify({'valid': False})

@app.route('/hwid', methods=['GET'])
def check_hwid():
    hwid = request.args.get('hwid')
    if hwid in hwids:
        return jsonify({'valid': True})
    
    # HWID geçerli değilse, LinkVertise'a yönlendir
    linkvertise_url = create_linkvertise_link(hwid)
    return redirect(linkvertise_url)

def create_linkvertise_link(hwid):
    base_url = f"https://link-to.net/{LINKVERTISE_USER_ID}/dynamic"
    to = f"{request.url_root}complete_linkvertise?hwid={hwid}"
    params = {
        "random": "1",
        "to": to
    }
    response = requests.get(base_url, params=params)
    return response.url

@app.route('/complete_linkvertise', methods=['GET'])
def complete_linkvertise():
    hwid = request.args.get('hwid')
    # Burada LinkVertise'dan gelen doğrulama yapılmalı
    # Basitlik için doğrudan HWID'yi kaydediyoruz
    hwids[hwid] = {'completed': True}
    return "LinkVertise tamamlandı. Oyuna geri dönebilirsiniz."

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        'total_keys': len(keys),
        'total_hwids': len(hwids),
        'keys': keys,
        'hwids': hwids
    })

if __name__ == '__main__':
    app.run(debug=True)
