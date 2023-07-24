"""Module for interacting with OS"""
import os
from flask import Flask, request, render_template
from csrgen import select_csr

app = Flask(__name__)

@app.route('/')
def index():
    """Initial route for homepage"""
    return render_template('index.html')


@app.route('/generatecsr')
def generatecsr():
    """Route when clicking Submit"""
    common_name = request.form.get('CN')
    organization = request.form.get('O')
    locality = request.form.get('L')
    state = request.form.get('ST')
    country = request.form.get('C')
    key_algorithm = request.form.get('keyAlgorithm')
    key_size = request.form.get('keySize')
    sans = request.form.get('Sans')
    try:
        select_csr(common_name,organization,locality,state,country, key_algorithm, key_size,sans)
    finally:
        return render_template('result.html')

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5555))
    app.run(host='0.0.0.0', port=port)