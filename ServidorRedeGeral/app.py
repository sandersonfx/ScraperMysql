from flask import Flask, request, jsonify
from scraper import do_scraping, do_scraping_without_date
from nota_fiscal import doNotaScraping
from database import last_log, getEmpresaId, get_status, update_status, getProfissionalId

import threading
import re

ERROR = None

app = Flask(__name__)

@app.route('/emitir-nota', methods=['POST'])
def activateNota():
    global ERROR
    
    cnpj = request.json.get('cnpj')
    cpf = request.json.get('cpf', None)
    password = request.json.get('password')
    serviceValue = request.json.get('service_value')
    serviceDescription = request.json.get('service_description')

    profissionalId = getProfissionalId(cnpj=cnpj, password=password)

    if profissionalId:
        thread = threading.Thread(target=doNotaScraping, args=(profissionalId, cnpj, password, serviceDescription, serviceValue, cpf))
        thread.start()
        response = {"message": "successfully started"}
        return jsonify(response), 200
    else:
        return jsonify({'message': 'an error ocurred'}), 500

@app.route('/activate-with-date', methods=['POST'])
def activate():
    global ERROR
    
    email = request.json.get('email')
    password = request.json.get('password')
    link = request.json.get('link')
    startDate = request.json.get('start_date')
    finalDate = request.json.get('final_date')
    id_empresa = request.json.get('id_empresa')

    date_pattern = r'\d{2}/\d{2}/\d{4}'

    status = get_status()

    if status:
        response = {"message": "another scraper is running"}
        return jsonify(response), 400 

    if re.match(date_pattern, startDate) and re.match(date_pattern, finalDate):
        id = id_empresa
        #id = getEmpresaId(email, password)

        if id:
            update_status(True)
            thread = threading.Thread(target=do_scraping, args=(email, password, link, id, startDate, finalDate))
            thread.start()

            response = {"message": "successfully started"}
            return jsonify(response), 200
    else:
        response = {"message": "Dates must be in dd/mm/yyyy format"}
        return jsonify(response), 400

@app.route('/activate-without-date', methods=['POST'])
def activateWithoutDate():
    global ERROR
    
    email = request.json.get('email')
    password = request.json.get('password')
    link = request.json.get('link')
    id_empresa = request.json.get('id_empresa')

    status = get_status()

    if status:
        response = {"message": "another scraper is running"}
        return jsonify(response), 400 

    #id = getEmpresaId(email, password)
    id = id_empresa

    if id:
        update_status(True)
        thread = threading.Thread(target=do_scraping_without_date, args=(email, password, link, id))
        thread.start()

        response = {"message": "successfully started"}
        return jsonify(response), 200
    else:
        response = {"message": "Company not found"}
        return jsonify(response), 400

@app.route('/status', methods=['GET'])
def status():
    status = get_status()
    
    if status:
        return jsonify({"message": "running"}), 200
    else:
        return jsonify({"message": "not running"}), 200

@app.route('/last-log', methods=['GET'])
def getLastLog():    
    log = last_log()

    if log and len(log) > 1:
        return jsonify({"time": log[1], "message": log[2]}), 200

    return jsonify({"message": "no log"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
