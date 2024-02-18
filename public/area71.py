from msilib.text import tables
import sqlite3
import random
import string
from faker import Faker
fake = Faker()

def criar_tabelas():
    # Conectar ao banco de dados (criará o arquivo se não existir)
    conn = sqlite3.connect('database.db')

    # Criar um cursor para executar consultas SQL
    cursor = conn.cursor()

    # Criar tabela de clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        endereco TEXT,
                        cpf TEXT)''')

    # Criar tabela de medidas
    cursor.execute('''CREATE TABLE IF NOT EXISTS medidas_corporais (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cliente_id INTEGER,
                        peitoral REAL,
                        ombro_esquerdo REAL,
                        ombro_direito REAL,
                        bicep_direito_relaxado REAL,
                        bicep_direito_contraido REAL,
                        bicep_esquerdo_relaxado REAL,
                        bicep_esquerdo_contraido REAL,
                        tricep_direito_relaxado REAL,
                        tricep_direito_contraido REAL,
                        tricep_esquerdo_relaxado REAL,
                        tricep_esquerdo_contraido REAL,
                        coxa_direita REAL,
                        coxa_esquerda REAL,
                        panturrilha_direita REAL,
                        panturrilha_esquerda REAL,
                        FOREIGN KEY (cliente_id) REFERENCES clientes(id) 
                        ON DELETE CASCADE
                        )
        ''')

    # Salvar as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

# Chamar a função para criar as tabelas

def inserir_dados():
    try:
        #Conexão ao banco de dados
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        for _ in range(30):        
            nome_cliente = fake.name()
            endereco = fake.address()
            cpf = ''.join(random.choices(string.digits, k=11))
            print(nome_cliente,endereco,cpf)
            cur.execute("INSERT INTO clientes (nome, endereco, cpf) VALUES (?, ?, ?)", (nome_cliente, endereco, cpf))

        
        for n in range(30):           
            peitoral = round(random.uniform(80, 120), 2)
            ombro_esquerdo = round(random.uniform(30, 50), 2)
            ombro_direito = round(random.uniform(30, 50), 2)
            bicep_direito_relaxado = round(random.uniform(20, 40), 2)
            bicep_direito_contraido = round(random.uniform(25, 45), 2)
            bicep_esquerdo_relaxado = round(random.uniform(20, 40), 2)
            bicep_esquerdo_contraido = round(random.uniform(25, 45), 2)
            tricep_direito_relaxado = round(random.uniform(20, 40), 2)
            tricep_direito_contraido = round(random.uniform(25, 45), 2)
            tricep_esquerdo_relaxado = round(random.uniform(20, 40), 2)
            tricep_esquerdo_contraido = round(random.uniform(25, 45), 2)
            coxa_direita = round(random.uniform(30, 60), 2)
            coxa_esquerda = round(random.uniform(30, 60), 2)
            panturrilha_direita = round(random.uniform(25, 45), 2)
            panturrilha_esquerda = round(random.uniform(25, 45), 2)

            cur.execute("INSERT INTO medidas_corporais (cliente_id,peitoral, ombro_esquerdo, ombro_direito, bicep_direito_relaxado, bicep_direito_contraido, bicep_esquerdo_relaxado, bicep_esquerdo_contraido, tricep_direito_relaxado, tricep_direito_contraido, tricep_esquerdo_relaxado, tricep_esquerdo_contraido, coxa_direita, coxa_esquerda, panturrilha_direita, panturrilha_esquerda) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (n+1,peitoral, ombro_esquerdo, ombro_direito, bicep_direito_relaxado, bicep_direito_contraido, bicep_esquerdo_relaxado, bicep_esquerdo_contraido, tricep_direito_relaxado, tricep_direito_contraido, tricep_esquerdo_relaxado, tricep_esquerdo_contraido, coxa_direita, coxa_esquerda, panturrilha_direita, panturrilha_esquerda))



            #Commit e fechar conexão
        conn.commit()
        conn.close()

        print("Dados inseridos com sucesso!")

                
    except Exception as e:
        print("Erro ao inserir dados no PostgreSQL:", e)

# Chamando a função para inserir dados
def limpar_tabela():
    try:
        # Conexão ao banco de dados
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # Executar a instrução SQL para limpar os dados da tabela
        cur.execute("DELETE FROM medidas_corporais")
        cur.execute("DELETE FROM clientes")

        # Commit e fechar conexão
        conn.commit()
        conn.close()

        print("Dados da tabela limpos com sucesso!")

    except Exception as e:
        print("Erro ao limpar dados da tabela:", e)

# Chamando a função para limpar os dados da tabela


def consulta():
    try:
    # Conexão ao banco de dados
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # ID do cliente que você deseja consultar
        cliente_id = 1  # Substitua pelo ID do cliente desejado

        # Consulta para selecionar as informações do cliente e suas medidas corporais
        cur.execute("""
            SELECT c.*, m.*
            FROM clientes c
            JOIN medidas_corporais m ON c.id = m.cliente_id
            WHERE c.id = ?
        """, (cliente_id,))
        resultado = cur.fetchall()

        if resultado:
            # Exibindo as informações do cliente e suas medidas corporais
            print(resultado)
            resultado_lista = list(resultado[0])
            print(resultado_lista)
        else:
            print("Cliente não encontrado.")

        # Fechar conexão
        conn.close()

    except Exception as e:
        print("Erro ao consultar o banco de dados:", e)
        
        
def ultimo_id(nome_tabela, nome_coluna_id, nome_banco='database.db'):
    # Conectando ao banco de dados
    conexao = sqlite3.connect(nome_banco)
    cursor = conexao.cursor()

    # Executando a consulta SQL para obter o último ID
    cursor.execute(f"SELECT MAX({nome_coluna_id}) FROM {nome_tabela}")
    ultimo_id = cursor.fetchone()[0]

    # Fechando a conexão com o banco de dados
    conexao.close()

    return ultimo_id
