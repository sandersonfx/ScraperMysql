import mysql.connector
from mysql.connector import Error

# Informações de conexão para o banco de dados de origem
source_db_info = {
    'host': 'exbodcemtop76rnz.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    'user': 'v1a1h8pzusa02wub',
    'database': 'r2rkr7eiskm8loif',
    'password': 's0h3d7thd8lssmg1'
}

# Informações de conexão para o banco de dados de destino (backup)
destination_db_info = {
    'host': '144.202.66.199',
    'user': 'user_bk',
    'database': 'kihonhair',
    'password': 'Rf7wP9K2cH1A'
}

try:
    # Conecte-se ao banco de dados de origem
    source_connection = mysql.connector.connect(**source_db_info)
    source_cursor = source_connection.cursor()

    # Conecte-se ao banco de dados de destino (backup)
    destination_connection = mysql.connector.connect(**destination_db_info)
    destination_cursor = destination_connection.cursor()

    # Copie os dados da tabela de origem para uma tabela temporária no destino
    copy_query = "CREATE TEMPORARY TABLE temp_clientes AS SELECT * FROM clientes"
    destination_cursor.execute(copy_query)

    # Inserção de linhas únicas na tabela de destino final
    insert_query = "INSERT INTO clientes SELECT * FROM temp_clientes WHERE id NOT IN (SELECT id FROM clientes)"
    destination_cursor.execute(insert_query)

    # Faça commit das alterações no banco de dados de destino
    destination_connection.commit()

    print("Dados copiados com sucesso!")

except Error as e:
    print("Erro:", e)

finally:
    # Feche as conexões
    if source_connection.is_connected():
        source_cursor.close()
        source_connection.close()
    if destination_connection.is_connected():
        destination_cursor.close()
        destination_connection.close()
