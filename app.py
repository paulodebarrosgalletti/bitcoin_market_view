from flask import Flask, jsonify, render_template
import crypto_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crypto/<crypto_id>', methods=['GET'])
def crypto(crypto_id):
    data = crypto_data.get_crypto_data(crypto_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
