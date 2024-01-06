from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/classify', methods=['POST', 'GET'])
def classify():
    image_data = request.form['image_data']
    response = jsonify(util.classify_image(image_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    print('Starting Python Flask Server For World Leaders Image Classification...')
    util.load_artifacts()
    app.run(port=5000, debug=True)