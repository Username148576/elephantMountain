from flask import Flask, request, redirect, jsonify, send_file, url_for
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

LINK = {}

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    print('Received data:', data)
    # 處理數據（如儲存到資料庫）
    return jsonify({'status': 'success'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    
    return jsonify([{'name': 'success', 'description':"asdasdasd", "price":50}]*20), 200

@app.route('/data/image', methods=['GET'])
def get_images():
    name = request.args.get('name')
    return send_file(f"{name}", mimetype='image/gif')

@app.route('/data/upload-pattern', methods=['POST'])
def upload_pattern():
    markerFile = request.files.get('markerFile')
    patternFile = request.files.get('patternFile')
    image = request.files.get('image')
    linkName = request.form.get('linkName')
    
    if markerFile and image and linkName and patternFile:
        patternFile.save(f"assets/patterns/{patternFile.filename}")
        image.save(f"assets/images/{image.filename}")
        markerFile.save(f"assets/images/{patternFile.filename}")
        LINK[linkName] = {'pattern': patternFile.filename, 'image': image.filename, 'marker': markerFile.filename}
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No pattern file uploaded'}), 400

@app.route('/data/marker-list', methods=['GET'])
def get_marker_list():
    marker_list = []
    for name in LINK:
        marker_info = {
            'name': name,
            'marker': f'assets/images/{LINK[name]["marker"]}',
            'image': f'assets/images/{LINK[name]["image"]}',
            'pattern': f'assets/patterns/{LINK[name]["pattern"]}',
        }
        marker_list.append(marker_info)
    
    return jsonify(marker_list)

if __name__ == '__main__':
    app.run(debug=True)