import sqlite3
import bcrypt
import os

def inicializar_banco():
    
    if os.path.exists('industrias_wayne.db'):
        print("Banco de dados já existe. Deseja recriá-lo? (s/n)")
        resposta = input().lower()
        if resposta == 's':
            os.remove('industrias_wayne.db')
        else:
            print("Usando banco de dados existente.")
            return

    print("Criando novo banco de dados...")
    
    conn = sqlite3.connect('industrias_wayne.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recursos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER,
        localizacao TEXT,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Email: bruce@wayne.com
    # Senha: batman123
    senha_admin = bcrypt.hashpw("batman123".encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('''
        INSERT INTO usuarios (email, senha, nome, nivel_acesso)
        VALUES (?, ?, ?, ?)
        ''', ('bruce@wayne.com', senha_admin, 'Bruce Wayne', 'admin'))
        print("Usuário admin criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Usuário admin já existe!")

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    inicializar_banco()