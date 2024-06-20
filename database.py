import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

db = mysql.connector.connect(
    host=DATABASE_HOST,
    user=DATABASE_USER,
    database=DATABASE_NAME,
    password=DATABASE_PASSWORD,
)

def ISelect(sql):
    try:
        db = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            database=DATABASE_NAME,
            password=DATABASE_PASSWORD,
        )
        cursor = db.cursor(buffered=True)

        cursor.execute(sql)
        db.commit()

        res = cursor.fetchall()

        if res:
            return res

        return False
    except Exception as e:
        print(e)
        return False  


def getProfissionalId(cnpj, password):
    res = ISelect("SELECT id FROM profissionais WHERE cnpj = '{}' AND password = '{}'".format(cnpj, password))

    try:
        if res:
            return res[0][0]
        else:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

            connection.execute("""INSERT INTO profissionais (id, cnpj, password) VALUES (NULL, '{}', '{}')""".format(cnpj, password))
            
            db.commit()

            connection.execute("SELECT LAST_INSERT_ID();")
            db.commit()

            res = connection.fetchone()

            if res:
                return res[0]
    except Exception as e:
        print(e)
        return False
    return False

def insertEmissao(idProfissional, serviceDescription, serviceValue, cpf, success):
    try:
        connection = db.cursor(buffered=True)
        sql = """
            INSERT INTO emissoes (id_profissional, cpf, service_description, service_value, status_emissao)
            VALUES ({}, '{}', '{}', {}, {});
        """.format(idProfissional, cpf if cpf else 'NULL', serviceDescription, serviceValue.replace(',', '.'), 1 if success else 0)

        connection.execute(sql)

        db.commit()

        return True
    except Exception as e:
        print(e)
        return False

def update_status(status = False):
    try: 
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        connection.execute("""
            UPDATE STATUS
            SET status = '{}'
            WHERE id = 1;
        """.format(str(status)))

        db.commit()

        return True

    except Exception as e:
        print(e)
        return False


def get_status():
    try: 
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        connection.execute("""
            SELECT * FROM STATUS
            WHERE id = 1;
        """)

        db.commit()

        status = connection.fetchone()[1]

        if status == 'True':
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False

def getEmpresaId(email, password):
    try: 
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        connection.execute("""SELECT id FROM empresa WHERE email="{}" AND password="{}";""".format(email, password))
        db.commit()

        id = connection.fetchone()[0]

        if id:
            return id
        else:
            return False

    except Exception as e:
        print(e)
        return False

def add_log(message):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        connection.execute("""INSERT INTO `logs`(`id`, `time`, `description`) VALUES (NULL,"{}","{}")""".format(str(datetime.now().strftime('%d/%m/%Y %H:%M')), str(message)))
        
        db.commit()

        return True
    except Exception as e:
        print(e)
        return None
    
def last_log():
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        connection.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 1;")
        db.commit()

        log = connection.fetchone()

        if log:
            return log
        else:
            return False

    except Exception as e:
        print(e)
        return False
    
def verify_relatorio_0063(data):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )
            connection = db.cursor(buffered=True)

        (cliente, pacote, servico, total, utilizados, validade, compra) = data

        connection.execute("""SELECT id FROM relatorio_0063 WHERE cliente = "{}" AND pacote = "{}" AND servico = "{}" AND total = "{}" AND utilizados = "{}" AND validade = "{}" AND compra = "{}";""".format(cliente, pacote, servico, total, utilizados, validade, compra))
        db.commit()

        id = connection.fetchone()[0]

        if id:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False

def insert_relatorio_0063(r, idEmpresa):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        if len(r) > 0:

            query = 'INSERT INTO `relatorio_0063` (`id_empresa`, `id`, `cliente`, `pacote`, `servico`, `total`, `utilizados`, `validade`, `compra`) VALUES '
            count = 0

            for data in r:
                (cliente, pacote, servico, total, utilizados, validade, compra) = data

                if (count == len(r) - 1):
                    query += """ ("{}", NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}");""".format(idEmpresa, cliente, pacote, servico, total, utilizados, validade, compra)
                else:
                    query += """ ("{}", NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}"),""".format(idEmpresa, cliente, pacote, servico, total, utilizados, validade, compra)
                count += 1
            
            connection.execute(query)
        
        db.commit()

        return True
    except Exception as e:
        print(e)
        return None

def verify_relatorio_0123(data):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        (profissional, tipo_contratacao, cargo, banco, agencia, conta, faturado, rateio_servicos, rateio_produtos, rateio_outros, caixinha, descontos, a_pagar, valor_casa) = data

        connection.execute("""SELECT id FROM relatorio_0123 WHERE profissional = "{}" AND tipo_contratacao = "{}" AND cargo = "{}" AND banco = "{}" AND agencia = "{}" AND conta = "{}" AND faturado = "{}" AND rateio_servicos = "{}" AND rateio_produtos = "{}" AND caixinha = "{}" AND descontos = "{}" AND a_pagar = "{}" AND valor_casa = "{}";""".format(profissional, tipo_contratacao, cargo, banco, agencia, conta, faturado, rateio_servicos, rateio_produtos, rateio_outros, caixinha, descontos, a_pagar, caixinha, valor_casa))

        db.commit()

        id = connection.fetchone()[0]

        if id:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False

def insert_relatorio_0123(r, idEmpresa):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        if len(r) > 0:

            query = 'INSERT INTO `relatorio_0123` (`id_empresa`, `id`, `profissional`, `tipo_contratacao`, `cargo`, `banco`, `agencia`, `conta`, `faturado`, `rateio_servicos`, `rateio_produtos`, `rateio_outros`, `caixinha`, `descontos`, `a_pagar`, `valor_casa`) VALUES '
            count = 0

            for data in r:
                (profissional, tipo_contratacao, cargo, banco, agencia, conta, faturado, rateio_servicos, rateio_produtos, rateio_outros, caixinha, descontos, a_pagar, valor_casa) = data

                if (count == len(r) - 1):
                    query +=  """   ("{}",NULL,"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");""".format(idEmpresa ,profissional, tipo_contratacao, cargo, banco, agencia, conta, faturado, rateio_servicos, rateio_produtos, rateio_outros, caixinha, descontos, a_pagar, caixinha, valor_casa)
                else:
                    query +=  """ ("{}",NULL,"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"),  """ .format(idEmpresa ,profissional, tipo_contratacao, cargo, banco, agencia, conta, faturado, rateio_servicos, rateio_produtos, rateio_outros, caixinha, descontos, a_pagar, caixinha, valor_casa)
                count += 1
            connection.execute(query)
        
        db.commit()

        return True
    except Exception as e:
        print(e)
        return None
    
def insert_relatorio_0051(r, idEmpresa):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        if len(r) > 0:
            query = 'INSERT INTO `relatorio_0051` (`id_empresa`, `id`, `data_cadastro_reserva`, `data_reserva`, `hora`, `cliente`, `celular`, `data_cadastro_cliente`, `email`, `profissional`, `servico`, `origem`, `status`, `observacao`, `data_comanda`, `numero`, `quem_cadastrou`) VALUES '
            count = 0

            for data in r:
                (data_cadastro_reserva, data_reserva, hora, cliente, celular, data_cadastro_cliente, email, profissional, servico, origem, status, observacao, data_comanda, numero, quem_cadastrou) = data

                if (count == len(r) - 1):
                    query += """({}, NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");""".format(idEmpresa, data_cadastro_reserva, data_reserva, hora, cliente, celular, data_cadastro_cliente, email, profissional, servico, origem, status, observacao, data_comanda, numero, quem_cadastrou)
                else:
                    query += """({}, NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"), """.format(idEmpresa, data_cadastro_reserva, data_reserva, hora, cliente, celular, data_cadastro_cliente, email, profissional, servico, origem, status, observacao, data_comanda, numero, quem_cadastrou)
                count += 1

            connection.execute(query)
        
        db.commit()

        return True
    except Exception as e:
        print(e)
        return None

def insert_relatorio_0053(r, idEmpresa):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        if len(r) > 0:

            query = 'INSERT INTO `relatorio_0053` (`id_empresa`, `id`, `data_reserva`, `hora`, `cliente`, `servico`, `valor`) VALUES '
            count = 0

            for data in r:
                (data_reserva, hora, cliente, servico, valor) = data

                if (count == len(r) - 1):
                    query +=  """  ("{}", NULL, "{}", "{}", "{}", "{}", "{}"); """ .format(idEmpresa, data_reserva, hora, cliente, servico, valor)
                else:
                    query +=  """  ("{}", NULL, "{}", "{}", "{}", "{}", "{}"), """ .format(idEmpresa, data_reserva, hora, cliente, servico, valor)
                count += 1

            connection.execute(query)
        
        db.commit()

        return True
    except Exception as e:
        print(e)
        return None
    
def verify_relatorio_0053(data):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        (data_reserva, hora, cliente, servico, valor) = data

        connection.execute("""SELECT id FROM relatorio_0053 WHERE data_reserva = "{}" AND hora = "{}" AND cliente = "{}" AND servico = "{}" AND valor = "{}";""".format(data_reserva, hora, cliente, servico, valor))
        db.commit()

        id = connection.fetchone()[0]

        if id:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False

def insert_relatorio_0004(r, idEmpresa):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        if len(r) > 0:
            query = 'INSERT INTO `relatorio_0004` (`id_empresa`, `id`, `cliente`, `codigo`, `aniversario`, `telefone`, `celular`, `email`, `sexo`, `como_conheceu`, `cpf`, `cep`, `endereco`, `numero`, `estado`, `cidade`, `complemento`, `bairro`, `profissao`, `cadastrado`, `obs`, `rg`) VALUES '
            count = 0

            for data in r:
                (cliente, codigo, aniversario, telefone, celular, email, sexo, como_conheceu, cpf, cep, endereco, numero, estado, cidade, complemento, bairro, profissao, cadastrado, obs, rg) = data

                if (count == len(r) - 1):
                    query += """ ("{}", NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");""".format(
            idEmpresa, cliente, codigo, aniversario, telefone, celular, email, sexo, como_conheceu, cpf, cep, endereco, numero, estado, cidade, complemento, bairro, profissao, cadastrado, obs, rg)
                else:
                    query += """ ("{}", NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"),""".format(
            idEmpresa, cliente, codigo, aniversario, telefone, celular, email, sexo, como_conheceu, cpf, cep, endereco, numero, estado, cidade, complemento, bairro, profissao, cadastrado, obs, rg)
                count += 1

            connection.execute(query)

        db.commit()

        return True
    except Exception as e:
        print(e)
        return False

def verify_relatorio_0004(data):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        (cliente, codigo, aniversario, telefone, celular, email, sexo, como_conheceu, cpf, cep, endereco, numero, estado, cidade, complemento, bairro, profissao, cadastrado, obs, rg) = data

        query =  """ SELECT id FROM relatorio_0004 WHERE cliente = "{}" AND codigo = "{}" AND aniversario = "{}" AND telefone = "{}" AND celular = "{}" AND email = "{}" AND sexo = "{}" AND como_conheceu = "{}" AND cpf = "{}" AND cep = "{}" AND endereco = "{}" AND numero = "{}" AND estado = "{}" AND cidade = "{}" AND complemento = "{}" AND bairro = "{}" AND profissao = "{}" AND cadastrado = "{}" AND obs = "{}" AND rg = "{}"; """ .format(
            cliente, codigo, aniversario, telefone, celular, email, sexo, como_conheceu, cpf, cep, endereco, numero, estado, cidade, complemento, bairro, profissao, cadastrado, obs, rg)

        connection.execute(query)
        db.commit()

        id = connection.fetchone()[0]

        if id:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False
    
def insert_relatorio_0186(r, idEmpresa):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        if len(r) > 0:
            query = 'INSERT INTO `relatorio_0186` (`id_empresa`, `id`, `data`, `comanda`, `item`, `tipo`, `categoria`, `profissional`, `assistente_1`, `assistente_2`, `comissao_percentual`, `cliente`, `email`, `telefone`, `celular`, `valor`, `desconto`, `quantidade`, `custo`, `comissao`, `liquido`, `ua`) VALUES '
            count = 0

            for data in r:
                (data, comanda, item, tipo, categoria, profissional, assistente_1, assistente_2, comissao_percentual, cliente, email, telefone, celular, valor, desconto, quantidade, custo, comissao, liquido, ua) = data

                if (count == len(r) - 1):
                    query += """ ("{}", NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"); """.format(
            idEmpresa, data, comanda, item, tipo, categoria, profissional, assistente_1, assistente_2, comissao_percentual, cliente, email, telefone, celular, valor, desconto, quantidade, custo, comissao, liquido, ua)
                else:
                    query +=  """  ("{}", NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"), """ .format(
            idEmpresa, data, comanda, item, tipo, categoria, profissional, assistente_1, assistente_2, comissao_percentual, cliente, email, telefone, celular, valor, desconto, quantidade, custo, comissao, liquido, ua)
                count += 1

            connection.execute(query)

        db.commit()

        return True
    except Exception as e:
        print(e)
        return False

def verify_relatorio_0186(data):
    try:
        try:
            connection = db.cursor(buffered=True)
        except:
            db = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                database=DATABASE_NAME,
                password=DATABASE_PASSWORD,
            )    
            connection = db.cursor(buffered=True)

        (data, comanda, item, tipo, categoria, profissional, assistente_1, assistente_2, comissao_percentual, cliente, email, telefone, celular, valor, desconto, quantidade, custo, comissao, liquido, ua) = data

        query =  """ SELECT id FROM relatorio_0186 WHERE data = "{}" AND comanda = "{}" AND item = "{}" AND tipo = "{}" AND categoria = "{}" AND profissional = "{}" AND assistente_1 = "{}" AND assistente_2 = "{}" AND comissao_percentual = "{}" AND cliente = "{}" AND email = "{}" AND telefone = "{}" AND celular = "{}" AND valor = "{}" AND desconto = "{}" AND quantidade = "{}" AND custo = "{}" AND comissao = "{}" AND liquido = "{}" AND ua = "{}"; """ .format(
            data, comanda, item, tipo, categoria, profissional, assistente_1, assistente_2, comissao_percentual, cliente, email, telefone, celular, valor, desconto, quantidade, custo, comissao, liquido, ua)

        connection.execute(query)

        result = connection.fetchone()

        if result:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False
