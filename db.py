import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis de configuração do banco de dados
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Função para conectar ao banco de dados PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )
    
# Executar uma consulta SELECT
def ISelect(sql, params=None):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute(sql, params)
        res = cursor.fetchall()
        return res if res else False
    finally:
        db.close()

# Inserir um registro de emissão
def insertEmissao(idProfissional, serviceDescription, serviceValue, cpf, success):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO emissoes (id_profissional, cpf, service_description, service_value, status_emissao)
            VALUES (%s, %s, %s, %s, %s);
        """, (idProfissional, cpf if cpf else None, serviceDescription, float(serviceValue.replace(',', '.')), 1 if success else 0))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Obter ID do profissional pelo CNPJ e senha
def getProfissionalId(cnpj, password):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM profissionais WHERE cnpj = %s AND password = %s", (cnpj, password))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            # Insere o profissional caso não exista e retorna o ID
            cursor.execute("INSERT INTO profissionais (cnpj, password) VALUES (%s, %s) RETURNING id", (cnpj, password))
            db.commit()
            res = cursor.fetchone()
            return res[0]
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Atualiza o status
def update_status(status=False):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("UPDATE status SET status = %s WHERE id = 1", (status,))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()
# Obtém o status atual
def get_status():
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT status FROM status WHERE id = 1")
        status = cursor.fetchone()
        return status[0] if status else None
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Adiciona um registro de log
def add_log(message):
    db = connect_db()
    try:
        cursor = db.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO logs (time, description) VALUES (%s, %s)", (now, message))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()

# Retorna o último log inserido
def last_log():
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 1")
        log = cursor.fetchone()
        return log
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()
# Verifica a existência de um registro no relatório 0063
def verify_relatorio_0063(data):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id FROM relatorio_0063 
            WHERE cliente = %s AND pacote = %s AND servico = %s AND total = %s AND utilizados = %s AND validade = %s AND compra = %s
        """, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Insere um registro no relatório 0063
def insert_relatorio_0063(r, idEmpresa):
    db = connect_db()
    try:
        cursor = db.cursor()
        for data in r:
            cursor.execute("""
                INSERT INTO relatorio_0063 (id_empresa, cliente, pacote, servico, total, utilizados, validade, compra)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (idEmpresa,) + tuple(data))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
# Verifica a existência de um registro no relatório 0123
def verify_relatorio_0123(data):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id FROM relatorio_0123
            WHERE profissional = %s AND tipo_contratacao = %s AND cargo = %s AND banco = %s AND agencia = %s 
              AND conta = %s AND faturado = %s AND rateio_servicos = %s AND rateio_produtos = %s 
              AND rateio_outros = %s AND caixinha = %s AND descontos = %s AND a_pagar = %s AND valor_casa = %s
        """, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Insere um registro no relatório 0123
def insert_relatorio_0123(r, idEmpresa):
    db = connect_db()
    try:
        cursor = db.cursor()
        for data in r:
            cursor.execute("""
                INSERT INTO relatorio_0123 (id_empresa, profissional, tipo_contratacao, cargo, banco, agencia, 
                                            conta, faturado, rateio_servicos, rateio_produtos, rateio_outros, 
                                            caixinha, descontos, a_pagar, valor_casa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idEmpresa,) + tuple(data))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
# Verifica a existência de um registro no relatório 0051
def verify_relatorio_0051(data):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id FROM relatorio_0051
            WHERE data_cadastro_reserva = %s AND data_reserva = %s AND hora = %s AND cliente = %s 
              AND celular = %s AND data_cadastro_cliente = %s AND email = %s AND profissional = %s 
              AND servico = %s AND origem = %s AND status = %s AND observacao = %s 
              AND data_comanda = %s AND numero = %s AND quem_cadastrou = %s
        """, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Insere um registro no relatório 0051
def insert_relatorio_0051(r, idEmpresa):
    db = connect_db()
    try:
        cursor = db.cursor()
        for data in r:
            cursor.execute("""
                INSERT INTO relatorio_0051 (id_empresa, data_cadastro_reserva, data_reserva, hora, cliente, 
                                            celular, data_cadastro_cliente, email, profissional, servico, 
                                            origem, status, observacao, data_comanda, numero, quem_cadastrou)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idEmpresa,) + tuple(data))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
# Verifica a existência de um registro no relatório 0053
def verify_relatorio_0053(data):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id FROM relatorio_0053
            WHERE data_reserva = %s AND hora = %s AND cliente = %s AND servico = %s AND valor = %s
        """, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Insere um registro no relatório 0053
def insert_relatorio_0053(r, idEmpresa):
    db = connect_db()
    try:
        cursor = db.cursor()
        for data in r:
            cursor.execute("""
                INSERT INTO relatorio_0053 (id_empresa, data_reserva, hora, cliente, servico, valor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (idEmpresa,) + tuple(data))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
# Verifica a existência de um registro no relatório 0004
def verify_relatorio_0004(data):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id FROM relatorio_0004
            WHERE cliente = %s AND codigo = %s AND aniversario = %s AND telefone = %s 
              AND celular = %s AND email = %s AND sexo = %s AND como_conheceu = %s 
              AND cpf = %s AND cep = %s AND endereco = %s AND numero = %s 
              AND estado = %s AND cidade = %s AND complemento = %s AND bairro = %s 
              AND profissao = %s AND cadastrado = %s AND obs = %s AND rg = %s
        """, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Insere um registro no relatório 0004
def insert_relatorio_0004(r, idEmpresa):
    db = connect_db()
    try:
        cursor = db.cursor()
        for data in r:
            cursor.execute("""
                INSERT INTO relatorio_0004 (id_empresa, cliente, codigo, aniversario, telefone, 
                                            celular, email, sexo, como_conheceu, cpf, cep, endereco, 
                                            numero, estado, cidade, complemento, bairro, profissao, 
                                            cadastrado, obs, rg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idEmpresa,) + tuple(data))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
# Insere um registro no relatório 0186
def insert_relatorio_0186(r, idEmpresa):
    db = connect_db()
    try:
        cursor = db.cursor()
        for data in r:
            cursor.execute("""
                INSERT INTO relatorio_0186 (id_empresa, data, comanda, item, tipo, categoria, profissional, 
                                            assistente_1, assistente_2, comissao_percentual, cliente, email, 
                                            telefone, celular, valor, desconto, quantidade, custo, comissao, 
                                            liquido, ua)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (idEmpresa,) + data)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# Verifica a existência de um registro no relatório 0186
def verify_relatorio_0186(data):
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id FROM relatorio_0186
            WHERE data = %s AND comanda = %s AND item = %s AND tipo = %s AND categoria = %s 
              AND profissional = %s AND assistente_1 = %s AND assistente_2 = %s 
              AND comissao_percentual = %s AND cliente = %s AND email = %s AND telefone = %s 
              AND celular = %s AND valor = %s AND desconto = %s AND quantidade = %s 
              AND custo = %s AND comissao = %s AND liquido = %s AND ua = %s
        """, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()
