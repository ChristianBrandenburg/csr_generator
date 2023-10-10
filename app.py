import os
import logging
import re
from flask import Flask, request, render_template
from csrgen import select_csr

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

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

    # Use a list comprehension to split the string by newline characters and strip whitespace
    san_list = [san.strip() for san in sans.split('\n') if san.strip() != '']

    # Regular expression pattern to check if a string is a valid domain name
    domain_pattern = re.compile(r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}", re.IGNORECASE)

    invalid_domains = [san for san in san_list if not domain_pattern.match(san)]
    if invalid_domains:
        # Handle the invalid domain names. For instance, raise an exception, or return an error message
        logger.warning(f"The following are not valid domain names: {', '.join(invalid_domains)}")

    logger.info(common_name)
    logger.info(organization)
    logger.info(locality)
    logger.info(state)
    logger.info(country)
    logger.info(key_algorithm)
    logger.info(key_size)
    logger.info(sans)

    result = select_csr(common_name, organization, locality, state, country, key_algorithm, key_size,san_list)
    csr = result[0]
    key = result[1]
    print(csr)
    return render_template('result.html', csr=csr,key=key)
    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port=5500)
    
