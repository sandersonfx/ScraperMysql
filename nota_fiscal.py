from webdriver import Webdriver
from database import update_status, add_log, insertEmissao

import os
import time

def doNotaScraping(idProfissional, cnpj, password, service_description, service_value, cpf = ''):
    try:
        driver = Webdriver(os.path.dirname(__file__)).getDriver()
        driver.get("https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional")

        inputUser = driver.execute_script("return document.getElementsByClassName('form-control input-lg cpfcnpj')[0]")
        inputUser.send_keys(cnpj)

        inputPassword = driver.execute_script("return document.getElementsByClassName('input-lg form-control')[1]")
        inputPassword.send_keys(password)

        driver.execute_script("document.getElementsByClassName('btn btn-lg btn-primary')[0].click()")

        time.sleep(4)

        driver.get("https://www.nfse.gov.br/EmissorNacional/DPS/Simplificada")

        time.sleep(5)

        if cpf and cpf != '':
            cpfInput = driver.execute_script("return document.getElementsByClassName('form-control cpfcnpj')[0]")
            cpfInput.send_keys(cpf)

        driver.execute_script("document.getElementsByTagName('select')[0].value = '5219965b-3b23-4327-9871-6fc8c4637806';")
        time.sleep(1)
        driver.execute_script("document.getElementById('Descricao').value = '{}'".format(service_description))

        inputMoney = driver.execute_script("return document.getElementsByClassName('form-control monetario')[0]")
        inputMoney.send_keys(service_value)

        time.sleep(4)

        driver.execute_script("document.getElementsByTagName('button')[8].click()")

        time.sleep(10)

        res = driver.execute_script("return document.getElementsByClassName('alert-success alert')[0]?.textContent ?? null")

        res = insertEmissao(
            idProfissional=idProfissional,
            serviceDescription=service_description,
            serviceValue=service_value,
            cpf=cpf,
            success=res == 'A NFS-e foi emitida com sucesso'
        )

        if res == False:
            add_log('Error when logging in: could not emissao fiscal in database')

        driver.quit()
    except Exception as e:
        print(e)
        add_log('Error when logging in: ' + str(e))
