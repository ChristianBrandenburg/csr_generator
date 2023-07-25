import os
from flask import Flask, request, render_template
from csrgen import select_csr

app = Flask(__name__)

@app.route('/')
def index():
    """Initial route for homepage"""
    return render_template('index.html')


@app.route('/generatecsr', methods=['POST'])
def generatecsr():
    """Route when clicking Submit"""
    common_name = request.form.get('CN')
    organization = request.form.get('O')
    locality = request.form.get('L')
    state = request.form.get('ST')
    country = request.form.get('C')
    key_algorithm = str(request.form.get('keyAlgorithm'))
    key_size = int(request.form.get('keySize'))
    sans = request.form.get('Sans')

    print(common_name)
    print(organization)
    print(locality)
    print(state)
    print(country)
    print(key_algorithm)
    print(key_size)
    print(sans)

    result = select_csr(common_name, organization, locality, state, country, key_algorithm, key_size,sans)
    csr = result[0]
    key = result[1]
    print(csr)
    return render_template('result.html', csr=csr,key=key)
    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port=5000)
    
